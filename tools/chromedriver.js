const fs = require('fs')
const path = require('path')
const dir = path.join('..', 'packages/drivers/chrome/')

// rename directories
let folders = fs.readdirSync(dir)
folders.forEach(folder => {
    const parts = folder.split('.')
    if (parts.length > 3) {
        const oldPath = path.join(dir, folder)
        const newPath = path.join(dir, parts.slice(0, 3).join('.'))
        console.log(`oldPath: ${oldPath}, newPath: ${newPath}`)
        fs.renameSync(oldPath, newPath)
    }
})

// rename files
folders = fs.readdirSync(dir)
folders.forEach(folder => {
    ['win32', 'mac64', 'mac64_m1'].forEach(arch => {
        const oldPath = path.join(dir, folder, `chromedriver_${arch}.zip`)
        const os = arch === 'win32' ? arch : 'darwin'
        let arc = 'x64'
        if (arch.includes('mac')) {
            arc = arch === 'mac64' ? 'x64' : 'arm64'
        }
        const newPath = path.join(dir, folder, `chromedriver-${os}-${arc}.zip`)
        console.log(`oldPath: ${oldPath}, newPath: ${newPath}`)
        if (fs.existsSync(oldPath)) {
            fs.renameSync(oldPath, newPath)
        }
    })
    // ['_darwin_arm64', '_darwin_x64', '_win32_x64'].forEach(arch => {
    //     const oldPath = path.join(dir, folder, `chromedriver${arch}.zip`)
    //     const newPath = path.join(dir, folder, `chromedriver${arch.replace(/_/g, '-')}.zip`)
    //     console.log(`oldPath: ${oldPath}, newPath: ${newPath}`)
    //      if (fs.existsSync(oldPath)) {
    //         fs.renameSync(oldPath, newPath)
    //     }       
    // })
    const oldPath = path.join(dir, folder, `chromedriver_mac32.zip`)
    const newPath = path.join(dir, folder, `chromedriver-darwin-x64.zip`)
    console.log(`oldPath: ${oldPath}, newPath: ${newPath}`)
    if (fs.existsSync(oldPath)) {
        fs.renameSync(oldPath, newPath)
    }    
})
