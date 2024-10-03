import React, { useState, useEffect } from 'react';
import axios from "axios";
import { Link } from "react-router-dom";


export const AllStoredPapers = () => {
    const [allStoredPapers, setAllStoredPapers] = useState([])

    useEffect(() => {
        axios({
            url: "http://localhost:8000/api/get-all-papers/",
            method: "GET",
            headers: {
                authorization: "placer auth token"
            },

        })
        .then(response => {
            setAllStoredPapers(response.data)
            console.log('Received papers list:', allStoredPapers)
        })
        .catch(error => {
            console.log('Errors fetching all papers list:', error.response)
        })
        
    })

  
    
    return (
        <div className="container" style = {{whiteSpace: 'pre-line'}}>
            <p><strong>All Papers</strong></p>
            <ul>
            {allStoredPapers.map(storedPaper => (
                <li key={storedPaper.title}>
                    <Link to= {`/storedpaper/${storedPaper.doi.replace(/\//g, '-')}`}>{storedPaper.title} {storedPaper.doi}</Link>
                </li>
            ))}
          </ul>
            
            
        </div>
    )
}

