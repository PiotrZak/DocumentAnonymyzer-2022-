import React, {useState} from 'react';

export const FileUpload = () =>{
	const [selectedFile, setSelectedFile] = useState();
    const [isSelected, setIsSelected] = useState();

	const changeHandler = (event) => {
		setSelectedFile(event.target.files[0]);
		setIsSelected(true);
	};

	const handleSubmission = () => {
		const formData = new FormData();

		formData.append('file', selectedFile);
		formData.append('filename', selectedFile.value);

		fetch(
			"http://localhost:5000/api/v1/pdfToText",
			{
				method: 'POST',
				body: formData,
			}
		)
			.then((response) => response.json())
			.then((result) => {
				console.log('Success:', result);
			})
			.catch((error) => {
				console.error('Error:', error);
			});
	};

	return(
   <div>
			<input className ="file-upload" type="file" name="file" onChange={changeHandler} />
			<div>
				<button  className="submit-feedback" onClick={handleSubmission}>Submit</button>
			</div>
		</div>
	)
}