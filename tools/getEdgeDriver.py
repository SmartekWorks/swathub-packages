import os
import sys
import requests
import zipfile
import shutil
from pathlib import Path


def download_edgedriver(version, platform, output_dir="."):
    """
    Download Microsoft Edge WebDriver for the specified version and platform
    
    Args:
        version: EdgeDriver version (e.g., '115.0.1901.203')
        platform: Platform identifier ('mac-arm64', 'mac-x64', 'win64')
        output_dir: Directory to save the output files
    """
    # Map platform to download filename format
    platform_map = {
        'mac-arm64': 'mac64_m1',
        'mac-x64': 'mac64',
        'win64': 'win64'
    }
    
    # Map platform to output filename format
    output_platform_map = {
        'mac-arm64': 'darwin-arm64',
        'mac-x64': 'darwin-x64',
        'win64': 'win32-x64'
    }
    
    if platform not in platform_map:
        raise ValueError(f"Unsupported platform: {platform}")
        
    download_platform = platform_map[platform]
    base_url = f"https://msedgedriver.azureedge.net/{version}/"
    filename = f"edgedriver_{download_platform}.zip"
    url = base_url + filename
    
    # Create temporary directory
    temp_dir = os.path.join(output_dir, f"temp_edge_{platform}")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Download the file
    print(f"Downloading {url}...")
    download_path = os.path.join(temp_dir, filename)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(download_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            
    # Extract the driver
    print(f"Extracting {filename}...")
    extract_path = os.path.join(temp_dir, "extracted")
    os.makedirs(extract_path, exist_ok=True)
    
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Get the EdgeDriver executable path
    if platform == 'win64':
        driver_name = "msedgedriver.exe"
    else:
        driver_name = "msedgedriver"
    
    driver_path = os.path.join(extract_path, driver_name)
    
    # Compress the driver with renamed output
    print(f"Compressing {driver_name}...")
    output_platform = output_platform_map[platform]
    output_filename = f"edgedriver-{output_platform}.zip"
    output_path = os.path.join(output_dir, output_filename)
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(driver_path, arcname=driver_name)
    
    # Clean up
    print(f"Cleaning up temporary files...")
    shutil.rmtree(temp_dir)
    
    print(f"Created {output_path}")
    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python getEdgeDriver.py <version> [output_directory]")
        print("Example: python getEdgeDriver.py 115.0.1901.203")
        sys.exit(1)
    
    version = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    platforms = ['mac-arm64', 'mac-x64', 'win64']
    
    for platform in platforms:
        try:
            print(f"\nProcessing EdgeDriver for {platform}...")
            download_edgedriver(version, platform, output_dir)
        except Exception as e:
            print(f"Error processing {platform}: {e}")
    
    print("\nAll processing completed!")


if __name__ == "__main__":
    main()
