document.addEventListener('DOMContentLoaded', () => {
	const btn = document.getElementById('btn')
	const filePathElement = document.getElementById('filePath')
	const processBtn = document.getElementById('processBtn')
	const revertBtn = document.getElementById('revertBtn')
	const sortOption = document.getElementById('sortOption')
	const currentTree = document.getElementById('currentTree')
	const treeElement = document.getElementById('tree')

	let filePath = '';
	let treedict = null;

	btn.addEventListener('click', async () => {
		filePath = await window.electronAPI.openDirectory()
		if (filePath) {
			filePathElement.innerText = filePath
			//currentTree.innerText = displayTree(filePath);
		}
		
		treedict = await processFile(filePath); 
		treeElement.innerText = jsonToAsciiTree(treedict); 
		// need error handling of some sort
	
	})

	processBtn.addEventListener('click', async () => {
		if (!filePath || !treedict) {
			console.error('No file path or treedict specified');
			return;
		}
		await moveFiles(filePath, treedict);
	});

	revertBtn.addEventListener('click', async () => {
		if (!filePath || !treedict) {
			console.error('No file path or treedict specified');
			return;
		}
		await revert(filePath, treedict);
	});

	sortOption.addEventListener('click', async function() => {
		sortOption.classLIst.toggle('active');
		try {
			const response = await fetch("127.0.0.1/sort_files");
			const data = await repoonse.json();
		} catch (error) {
			console.error('Error: ', error);
		}




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
			treeElement.innerText = JSON.stringify(treedict);// jsonToAsciiTree(treedict);
		}
	});
});

async function processFile(filePath) {
	console.log('PROCESS');
	const requestData = {
		file_path: filePath,
		producer: 'ollama',
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
		return responseData.treedict;

	} catch (error) {
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

async function revert(filePath, treedict) {	
	try {
		const moveFilesResponse = await fetch('http://127.0.0.1:5000/revert', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ file_path: filePath, treedict: treedict})
		});

		if (moveFilesResponse.ok) {
			console.log('Files Moved Successfully');
		} else {
			console.error('Error reverting');
		}
	} catch (error) {
		console.error('Error moving files:', error);
		alert(`Failed to revert. Please try again. ${error}`);
	}
}
		
function jsonToAsciiTree(json, prefix = "", isLast = true) {
	let output = "";

	if (typeof json === "object" && json !== null) {
		const keys = Object.keys(json).sort();
		const lastIndex = keys.length - 1;
		output += `<div>${prefix}${isLast ? "└── " : "├── "}{</div>`;		

		for (let i = 0; i < keys.length; i++) {
			const key = keys[i];
			const value = json[key];
			const isLastChild = i === lastIndex;
			const childPrefix = prefix + (isLast ? "    " : "│   ");
			const newPrefix = childPrefix + (isLastChild ? "└─ " : "├─ ");

			output += `<div>${childPrefix}${isLastChild ? "└─ " : "├─ "}<span class="key">${key}</span>: `;
			if (typeof value === "object" && value !== null) {
				output += `</div>`;
				output += jsonToAsciiTree(value, childPrefix, isLastChild);
			} else {
				output += `<span class="value">${JSON.stringify(value)}</span>`;
			}
		}
		output += `<div>${prefix}${isLast ? "    " : "│   "}}</div>`;
	} else {
		output += `<span class="value">${JSON.stringify(json)}</span>`;
	}
	
	return output;
}

function displayTree(filePath) {
	const fs = require("fs");
	const path = require("path");
	let results = [];

	fs.readdirSync(filePath).forEach(function (file) {
		file = path.join(filePath, file);
		const stat = fs.statSync(file);
		
		if (stat && stat.isDirectory()) {
			results = results.concat(displayTree(file))
		} else {
			results.push(file);
		}
	});
	return results;
}


