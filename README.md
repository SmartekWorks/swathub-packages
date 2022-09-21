## SWATHub robot package repository

### package.json

```json
{
  "name": "engine",
  "version": "1.8.0",
  "packages": {
    "openjdk": "1.8.0", /* 缺省认为是目录，即 appdata/openjdk */
    "android-sdk": "33.0.3",
    "assets": "1.0.0",
    "addons/ahk": "1.0.0",
    "addons/autoit": "1.0.0",
    "addons/database": "1.0.0",
    "addons/excel": "1.0.0",
    "addons/mail": "1.0.0",
    "addons/system": "1.0.0",
    "drivers/selenium-server.jar": "3.141.59",  /* 含后缀名代表是文件 */
    "drivers/auto-server.jar": "1.0.0"
  },
  "repositories": [
    "http://download.swathub.com/packages",
    "http://10.0.0.100/downloads/packages",
    "file:///C:/Users/username/Downloads/packages"
  ]
}
```

### Sample package URLs:
* openjdk: http://download.swathub.com/packages/openjdk/1.8.0/openjdk-win32-x64.zip
* addon: http://download.swathub.com/packages/addons/excel/1.0.0/excel-win32-x64.zip
* driver: http://download.swathub.com/packages/drivers/chrome/100.0.4896/chromedriver-darwin-arm64.zip
