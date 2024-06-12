const btn = document.getElementById('btn')
const filePathElement = document.getElementById('filePath')

btn.addEventListener('click', async () => {
	const filePath = await window.electronAPI.openFile()
	filePathElement.innerText = filePath
})

document.addEventListener('dragover', (e) => {
    	e.preventDefault();
    	e.stopPropagation();
});

document.addEventListener('drop', (event) => {
    	event.preventDefault();
	event.stopPropagation();

    	let pathArr = [];
    	for (const f of event.dataTransfer.files) {
        // Using the path attribute to get absolute file path
        	console.log('File Path of dragged files: ', f.path)
        	pathArr.push(f.path); // assemble array for main.js
		filePath.innerText = f.path
    	}
    	console.log(pathArr);
    	const ret = ipcRenderer.sendSync('dropped-file', pathArr);
    	console.log(ret);
});
