import PaperForm from '../components/PaperForm';
import React, { useState, useEffect } from 'react';
import axios from "axios";
import api from '../components/api'


function Papers () {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [papers, setPapers] = useState<any[]>([])
    const [error, setError] = useState<string | null>(null);
    const [reload, setReload] = useState<number>(0)
    const accessToken = localStorage.getItem("accessToken");
    const deleteClicked = async(id:any) => {
        try {
            api.delete(`/papers/${id}/`)
            setReload(reload + 1)
        }
        catch (error:any) {
            console.log("error deleting paper")
        }
    }
    
    useEffect(() => {
        const getPapers = async() => {
            try {
                const response = await api.get('/papers/')
                setPapers(response.data)
            }
            catch (error:any) {
                console.log('Error fetching papers', error.response)
            }
        }
        getPapers();
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

        const formData = new FormData();

        formData.append("file", selectedFile)
            
        //console.log([...formData.entries()])
        setError(null);

        axios({
            url: `${import.meta.env.VITE_BACKEND_URL}/api/papers/`,
            method: "POST",
            headers: {
                "Authorization":`Bearer ${accessToken}`
            },
            data: formData
        })
        .then(response => {
            console.log('New paper created:', response.data)
            //set papers
            
        })
        .catch((Error) => {
            if (Error.response.data.error == "paper name already exists.") {
                setError("paper name already exists. Choose a different one.")
                console.error('Error creating new paper');
            }
            else {
                setError("Error creating paper:" + Error.response.data.error)
                console.error(Error.response)
            }

        })

        setError(null)
        setSelectedFile(null)
    }
    return (
        
        <div>
        {error && (
            <div className="alert alert-danger alert-dismissible fade show" role="alert">
            {error}
            <button
                type="button"
                className="btn-close"
                data-bs-dismiss="alert"
                aria-label="Close"
                onClick={() => setError(null)}
            ></button>
            </div>
        )}
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