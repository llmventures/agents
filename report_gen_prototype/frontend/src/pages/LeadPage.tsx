import { useParams } from "react-router";
import axios from "axios";
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';



function LeadPage() {
    const accessToken = localStorage.getItem("accessToken");
    const navigate = useNavigate();
    const deleteClicked = () => {
        axios({
            url: `${import.meta.env.VITE_BACKEND_URL}/api/leads/${name}/`,
            method: "DELETE",
            headers: {
                "Authorization":`Bearer ${accessToken}`
            }
        })
        .then(response => {
            navigate('/leads')
        })
    }

    const { name } = useParams()
    console.log(name)
    const [description, setDescription] = useState('')
    useEffect(() => {
        console.log("URL: ")
        axios({
            url: `${import.meta.env.VITE_BACKEND_URL}/api/leads/${name}/`,
            method: "GET",
            headers: {
                "Authorization":`Bearer ${accessToken}`
            }
        })
        .then((response:any) => {
            setDescription(response.data.description)
        })
        .catch((error:any) => {
            console.log('Error fetching team lead', error.response)
            
        })
    })
    return (
        <div className="card" style={{width: "18rem"}}>
        <div className="card-body">
        <h5 className="card-title">{name}</h5>
        <p className="card-text">{description}</p>
        <button type="button" className="btn btn-danger" onClick={deleteClicked}>Delete</button>
        <a href="#" className="card-link">Another link</a>
        </div>
    </div>
  )
}

export default LeadPage