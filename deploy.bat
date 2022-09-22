c:\ufile\filemgr-win64.exe --action sync --bucket swathub-download --dir .\packages --prefix packages/
aws s3 sync ./packages s3://download.swathub.com/packages