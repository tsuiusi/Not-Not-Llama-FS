document.addEventListener('DOMContentLoaded', () => {
	const btn = document.getElementById('btn')
	const filePathElement = document.getElementById('filePath')
	const processBtn = document.getElementById('processBtn')

	let filePath = '';

	btn.addEventListener('click', async () => {
		filePath = await window.electronAPI.openDirectory()
		if (filePath) {
			filePathElement.innerText = filePath
		}
	})

	processBtn.addEventListener('click', async () => {
		if (!filePath) {
			console.error('No file path specified');
			return;
		}

		console.log('PROCESS');
		const requestData = {
			file_path: filePath,
			producer: 'groq',
			preference: null,
			ignore: null,
			apikey: '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',
		};

		try {
			const response = await fetch('http://localhost:5000/process_file', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(requestData)
			});

			if (!response.ok) {
				throw new Error(`Server error: ${response.status}`);
			}
			const responseData = await response.json();
			console.log('Server response:', responseData);
			alert(responseData.message);
		} catch (error) {
			console.error('Error processing file:', error);
			alert(`Failed to process the file. Please try again. ${error}`);
		}
	});

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
		}
		if (pathArr.length > 0) {
			filePath = pathArr[pathArr.length - 1]
			filePathElement.InnerElement = filePath

			const ret = ipcRenderer.sendSync('dropped-file', pathArr);
			console.log(ret);
		}
	});
});
