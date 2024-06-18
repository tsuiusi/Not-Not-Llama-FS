document.addEventListener('DOMContentLoaded', () => {
	const btn = document.getElementById('btn')
	const filePathElement = document.getElementById('filePath')
	const processBtn = document.getElementById('processBtn')
	const treeElement = document.getElementById('tree') // Add this to the index.html later 

	let filePath = '';
	let treedict = null;
	let trees = new Array(2)

	btn.addEventListener('click', async () => {
		filePath = await window.electronAPI.openDirectory()
		if (filePath) {
			filePathElement.innerText = filePath
		}

		// add error handling here
		treedict = await processFile(filePath); 
		treeElement.innerText = jsonToAsciiTree(treedict); 
	})

	processBtn.addEventListener('click', async () => {
		if (!filePath || !treedict) {
			console.error('No file path or treedict specified');
			return;
		}
		await moveFiles(filePath, treedict);
	});

	document.addEventListener('dragover', (e) => {
		e.preventDefault();
		e.stopPropagation();
	});

	document.addEventListener('drop', async (event) => {
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
			filePathElement.innerText = filePath // InnerElement worked though

			// add error handling here
			treedict = await processFile(filePath); 
			treeElement.innerText = "1" //jsonToAsciiTree(treedict);
		}
	});
});

async function processFile(filePath) {
	console.log('PROCESS');
	const requestData = {
		file_path: filePath,
		producer: 'groq',
		preference: null,
		ignore: null,
		apikey: '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',
	};

	try {
		const response = await fetch('http://127.0.0.1:5000/process_file', {
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

		return responseData.treedict;

	} catch (error) {
		console.error('Error processing file:', error);
		alert(`Failed to process the file. Please try again. ${error}`);
	}
}

async function moveFiles(filePath, treedict) {
	try {
		const moveFilesResponse = await fetch('http://127.0.0.1:5000/move_files', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ file_path: filePath, treedict: treedict})
		});

		if (moveFilesResponse.ok) {
			console.log('Files Moved Successfully');
		} else {
			console.error('Error moving files');
		}
	} catch (error) {
		console.error('Error moving files:', error);
		alert(`Failed to move files. Please try again. ${error}`);
	}
}

function jsonToAsciiTree(json, prefix = "", isLast = true) {
	let output = "";

	if (typeof json === "object" && json !== null) {
		const keys = Object.keys(json);
		const lastIndex = keys.length - 1;

		output += `<div>${prefix}${isLast ? "└─ " : "├─ "}${"{"}`;

		for (let i = 0; i < keys.length; i++) {
			const key = keys[i];
			const value = json[key];
			const isLastChild = i === lastIndex;
			const childPrefix = prefix + (isLast ? "&nbsp;&nbsp;&nbsp;" : "│&nbsp;&nbsp;");

			output += `<div>${childPrefix}${isLastChild ? "└─ " : "├─ "}<span class="key">${key}</span>: `;

			if (typeof value === "object" && value !== null) {
				output += jsonToAsciiTree(value, childPrefix, isLastChild);
			} else {
				output += `<span class="value">${JSON.stringify(value)}</span>`;
			}

			output += "</div>";
		}
		output += `<div>${prefix}${isLast ? "&nbsp;&nbsp;&nbsp;" : "│&nbsp;&nbsp;"}${"}"}</div></div>`;
	} else {
		output += `<span class="value">${JSON.stringify(json)}</span>`;
	}
	
	return output;
}



