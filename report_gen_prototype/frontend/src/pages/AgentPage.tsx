import axios from "axios";
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useParams } from "react-router";



function AgentPage() {
    const { name } = useParams()
    const [role, setRole] = useState('')
    const [expertise, setExpertise] = useState('')
    const [files, setFiles] = useState<any[]>([]) 
    const accessToken = localStorage.getItem("accessToken");
    useEffect(() => {
        
        axios({
            url: `${import.meta.env.VITE_BACKEND_URL}/api/agents/${name}/`,
            method: "GET",
            headers: {
                "Authorization":`Bearer ${accessToken}`
            }
        })
        .then((response:any) => {
            setRole(response.data.role)
            setExpertise(response.data.expertise)
            setFiles(response.data.stored_papers)
            //console.log(files)
        })
        .catch((error:any) => {
            console.log('Error fetching agents', error.response)
        })
    })

    const navigate = useNavigate();
    const deleteClicked = () => {
        axios({
            url: `http://localhost:8000/api/agents/${name}/`,
            method: "DELETE",
            headers: {
                "Authorization":`Bearer ${accessToken}`
            }
        })
        .then(response => {
            navigate('/agents')
        })
    }
    return (
        <div className="card" style={{width: "18rem"}}>
        <div className="card-body">
        <h5 className="card-title">{name}</h5>
        <p className="card-text">{role}</p>
        <button type="button" className="btn btn-danger" onClick={deleteClicked}>Delete</button>
        {files.map((file) => (
            <a href={file.file} className="list-group-item list-group-item-action" target="_blank">{file.name}</a>
        ))}
        </div>
    </div>
  )
}

export default AgentPage