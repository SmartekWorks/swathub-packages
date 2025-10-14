import os
import sys
import zipfile
import shutil
from pathlib import Path
import re
from datetime import datetime


def find_packages_directory(start_dir="."):
    """
    Recursively search for packages directory starting from start_dir
    
    Args:
        start_dir: Directory to start searching from
        
    Returns:
        Path to packages directory if found, None otherwise
    """
    start_path = os.path.abspath(start_dir)
    
    # First check if packages exists in current directory
    packages_path = os.path.join(start_path, "packages")
    if os.path.exists(packages_path) and os.path.isdir(packages_path):
        return packages_path
    
    # Search parent directories
    current_path = start_path
    while True:
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:  # Reached root
            break
            
        packages_path = os.path.join(parent_path, "packages")
        if os.path.exists(packages_path) and os.path.isdir(packages_path):
            return packages_path
            
        current_path = parent_path
    
    return None


def parse_version(version_string):
    """
    Parse semantic version string into comparable tuple
    
    Args:
        version_string: Version string like '1.0.1' or '2.10.3'
        
    Returns:
        Tuple of integers for comparison, or original string if parsing fails
    """
    try:
        # Extract version numbers using regex
        version_parts = re.findall(r'\d+', version_string)
        if version_parts:
            return tuple(int(part) for part in version_parts)
    except:
        pass
    
    # Fallback to string comparison
    return version_string


def get_latest_version_dirs(packages_dir):
    """
    Get the latest version directory for each package
    
    Args:
        packages_dir: Path to the packages directory
        
    Returns:
        Dictionary mapping package names to their latest version directory paths
    """
    latest_dirs = {}
    
    if not os.path.exists(packages_dir):
        print(f"Packages directory not found: {packages_dir}")
        return latest_dirs
    
    for package_name in os.listdir(packages_dir):
        package_path = os.path.join(packages_dir, package_name)
        if not os.path.isdir(package_path):
            continue
        
        # Special handling for drivers directory structure
        if package_name.lower() == 'drivers':
            # For drivers: packages/drivers/[browser]/[version]
            for browser_name in os.listdir(package_path):
                browser_path = os.path.join(package_path, browser_name)
                if not os.path.isdir(browser_path):
                    continue
                
                # Get all version directories for this browser
                version_dirs = []
                for item in os.listdir(browser_path):
                    item_path = os.path.join(browser_path, item)
                    if os.path.isdir(item_path):
                        version_dirs.append(item)
                
                if version_dirs:
                    # Sort versions using semantic version parsing
                    try:
                        version_dirs.sort(key=parse_version, reverse=True)
                    except:
                        # Fallback to string sorting
                        version_dirs.sort(reverse=True)
                    
                    latest_version = version_dirs[0]
                    # Use browser_name as key for drivers
                    driver_key = f"drivers/{browser_name}"
                    latest_dirs[driver_key] = os.path.join(browser_path, latest_version)
        else:
            # Normal package structure: packages/[package]/[version]
            # Get all version directories
            version_dirs = []
            for item in os.listdir(package_path):
                item_path = os.path.join(package_path, item)
                if os.path.isdir(item_path):
                    version_dirs.append(item)
            
            if version_dirs:
                # Sort versions using semantic version parsing
                try:
                    version_dirs.sort(key=parse_version, reverse=True)
                except:
                    # Fallback to string sorting
                    version_dirs.sort(reverse=True)
                
                latest_version = version_dirs[0]
                latest_dirs[package_name] = os.path.join(package_path, latest_version)
    
    return latest_dirs


def find_platform_files(directory, platform):
    """
    Find all files matching the platform in a directory
    
    Args:
        directory: Directory to search in
        platform: Platform string (e.g., 'win32-x64')
        
    Returns:
        List of file paths that match the platform
    """
    platform_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if platform in file:
                file_path = os.path.join(root, file)
                platform_files.append(file_path)
    
    return platform_files


def extract_platform_files(platform, packages_dir="packages", output_dir="."):
    """
    Extract all platform-specific files from latest version directories
    
    Args:
        platform: Target platform (e.g., 'win32-x64')
        packages_dir: Path to packages directory or search hint
        output_dir: Directory to save output files
    """
    # Find packages directory if not found directly
    if not os.path.exists(packages_dir):
        found_packages = find_packages_directory()
        if found_packages:
            packages_path = found_packages
            print(f"Found packages directory at: {packages_path}")
        else:
            print(f"Packages directory not found. Searched from: {os.path.abspath('.')}")
            return
    else:
        packages_path = os.path.abspath(packages_dir)
    
    output_path = os.path.abspath(output_dir)
    
    print(f"Searching for platform '{platform}' files in: {packages_path}")
    
    # Get latest version directories
    latest_dirs = get_latest_version_dirs(packages_path)
    
    if not latest_dirs:
        print("No package directories found!")
        return
    
    print(f"Found {len(latest_dirs)} packages with latest versions:")
    for package, version_dir in latest_dirs.items():
        print(f"  - {package}: {os.path.basename(version_dir)}")
    
    # Create temporary extraction directory
    temp_extract_dir = os.path.join(output_path, f"temp_extract_{platform}")
    if os.path.exists(temp_extract_dir):
        shutil.rmtree(temp_extract_dir)
    os.makedirs(temp_extract_dir)
    
    total_files = 0
    
    # Process each package's latest version
    for package_name, version_dir in latest_dirs.items():
        print(f"\nProcessing {package_name}...")
        
        # Find platform-specific files
        platform_files = find_platform_files(version_dir, platform)
        
        if not platform_files:
            print(f"  No {platform} files found in {package_name}")
            continue
        
        print(f"  Found {len(platform_files)} {platform} files")
        
        # Create package directory in temp extraction
        package_extract_dir = os.path.join(temp_extract_dir, package_name, os.path.basename(version_dir))
        os.makedirs(package_extract_dir, exist_ok=True)
        
        # Copy files preserving relative structure
        for file_path in platform_files:
            # Get relative path from version directory
            rel_path = os.path.relpath(file_path, version_dir)
            dest_path = os.path.join(package_extract_dir, rel_path)
            
            # Create destination directory if needed
            dest_dir = os.path.dirname(dest_path)
            os.makedirs(dest_dir, exist_ok=True)
            
            # Copy file
            shutil.copy2(file_path, dest_path)
            print(f"    Copied: {rel_path}")
            total_files += 1
    
    if total_files == 0:
        print(f"\nNo files found for platform '{platform}'")
        shutil.rmtree(temp_extract_dir)
        return
    
    # Create compressed archive with new naming convention
    archive_name = f"swathub-packages_{platform}.zip"
    archive_path = os.path.join(packages_path, archive_name)
    
    print(f"\nCreating archive: {archive_name}")
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_extract_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Get path relative to temp directory for archive
                arcname = os.path.relpath(file_path, temp_extract_dir)
                zipf.write(file_path, arcname)
    
    # Clean up temporary directory
    shutil.rmtree(temp_extract_dir)
    
    print(f"\nCompleted! Created {archive_path} with {total_files} files")
    return archive_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python extractPlatformFiles.py <platform> [packages_dir] [output_dir]")
        print("Example: python extractPlatformFiles.py win32-x64")
        print("         python extractPlatformFiles.py darwin-arm64 packages .")
        sys.exit(1)
    
    platform = sys.argv[1]
    packages_dir = sys.argv[2] if len(sys.argv) > 2 else "packages"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
    
    try:
        extract_platform_files(platform, packages_dir, output_dir)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
