import PaperForm from '../components/PaperForm';
import React, { useState, useEffect } from 'react';
import axios from "axios";

function Papers () {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [papers, setPapers] = useState<any[]>([])
    const [error, setError] = useState<string | null>(null);
    const [reload, setReload] = useState<number>(0)
    const deleteClicked = (id:any) => {
        console.log("DELETING AT")
        console.log(`http://localhost:8000/api/papers/${id}/`)
        axios({
            url: `http://localhost:8000/api/papers/${id}/`,
            method: "DELETE",
            headers: {
                authorization: "placer auth token"
            }
        })
        .then(response => {
            setReload(reload + 1)
        })
    }
    
    useEffect(() => {
        axios({
            url: "http://localhost:8000/api/papers/",
            method: "GET",
            headers: {
                authorization: "placer auth token"
            }
        })
        .then((response:any) => {
            setPapers(response.data)
            console.log(papers)
        })
        .catch((error:any) => {
            console.log('Error fetching papers', error.response)
        })
    })

    //onFileChange:
    const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
          setSelectedFile(e.target.files[0]);
        }
      };

    const formSubmit = (event: React.FormEvent) => {
        
        if (!selectedFile) {
            setError("Please select a file.");
            return;
        }
        event.preventDefault();
        const now = new Date();
        const dateTime = now.toLocaleString();

        const formData = new FormData();

        formData.append("file", selectedFile)
            
        console.log([...formData.entries()])
        setError(null);

        axios({
            url: "http://localhost:8000/api/papers/",
            method: "POST",
            headers: {
                authorization: "placer auth"
            },
            data: formData
        })
        .then(response => {
            console.log('New paper created:', response.data)
            //set papers
            
        })
        .catch((Error) => {
            if (Error.response.data.error == "Lead name already exists.") {
                setError("Lead name already exists. Choose a different one.")
                console.error('Error creating new lead');
            }
            else {
                setError("Error:" + Error.response.data.error)
                console.error(Error.response)
            }

        })

        setError(null)
        setSelectedFile(null)
    }
    return (
        <div>
            <h3>Upload a new paper</h3>
            <PaperForm 
            file = {selectedFile}
            onFileChange={onFileChange}
            onSubmit={formSubmit}
            />

        <h3>Current papers</h3>
        <div className="list-group">
        {papers.map((paper) => (
            
            <div className="d-flex bd-highlight">
                <div className = "p-2 flex-fill bd-highlight">
                    <a 
                    href= {paper.file}
                    className="list-group-item list-group-item-action"
                    target="_blank"
                    >
                    Download {paper.name}
                    </a>
                </div>
                <div className = "p-2 flex-fill bd-highlight">
                <button type="button" className="btn btn-danger" onClick={() => deleteClicked(paper.id)}>Delete</button>
                </div>

            </div>
        ))}
        </div>
        </div>


        

    );
}

export default Papers;