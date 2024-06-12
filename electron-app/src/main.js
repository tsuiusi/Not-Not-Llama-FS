const { app, BrowserWindow, ipcMain, dialog } = require('electron/main'); 
const path = require('node:path')

async function handleFileOpen () {
	const { canceled, filePaths } = await dialog.showOpenDialog()
	if (!canceled) {
		return filePaths[0]
	}
}

const createWindow = () => {
	const mainWindow = new BrowserWindow({
		webPreferences: {
			contextIsolation: true,
			nodeIntegration: true,
			preload: path.join(__dirname, 'preload.js')
		}
	})
	mainWindow.loadFile('index.html')
}

ipcMain.on('dropped-file', (event, arg) => {
    console.log('Dropped File(s):', arg);
    event.returnValue = `Received ${arg.length} paths.`; // Synchronous reply
})

// Create a window when there isn't a window
app.whenReady().then(() => {
	ipcMain.handle('dialog:openFile', handleFileOpen)
	createWindow()

	app.on('activate', () => {
		if (BrowserWindow.getAllWindows().length === 0) {
			createWindow()
		}
	})
})

// If all windows are closed, quit the app
app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit()
	}
})


