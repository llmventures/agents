import React, { useState, useEffect } from 'react';
import axios from "axios";
import ReactMarkdown from 'react-markdown';
import { useParams } from "react-router-dom";


export const SpecificPaper = () => {
    let {doi} = useParams()
    console.log(doi)
    
    const [paper, setPaper] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        axios({
            url: `http://localhost:8000/api/papers/${doi}`,
            method: "GET",
            headers: {
                authorization: "placer auth token"
            },

        })
        .then(response => {
            setPaper(response.data)
            setLoading(false)
        })
        .catch(error => {
            console.log('Errors fetching specific papers:', error.response)
            setLoading(false)
        })
        
    })
    if (loading) {
        return <div>Loading</div>;
    }

    if (!paper) {
        return <div> Item not found</div>;
    }
    return (
        <div className="container" style = {{whiteSpace: 'pre-line'}}>
            <h1></h1>
            
            <p><strong>Title:</strong> {paper.title}</p>
            <p><strong>DOI:</strong> {paper.doi}</p>
            <p><strong>Authors:</strong> {paper.authors}</p>
            <p><strong>Pub date:</strong> {paper.date}</p>
            <p><strong>Date Accessed:</strong> {paper.date_accessed}</p>
            
        </div>
    )

}
