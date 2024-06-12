const { contextBridge, ipcRenderer } = require('electron/renderer')

contextBridge.exposeInMainWorld('electronAPI', {
	openDirectory: () => ipcRenderer.invoke('dialog:openDirectory'),
	sendDroppedFiles: (filePaths) => ipcRenderer.sendSync('dropped-file', filePaths)
});
