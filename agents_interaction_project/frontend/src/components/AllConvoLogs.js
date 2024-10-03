import React, { useState, useEffect } from 'react';
import axios from "axios";
import { Link } from "react-router-dom";


export const AllConvoLogs = () => {
    const [allCurConvos, setAllCurConvos] = useState([])

    useEffect(() => {
        axios({
            url: "http://localhost:8000/api/get-all-logs/",
            method: "GET",
            headers: {
                authorization: "placer auth token"
            },

        })
        .then(response => {
            setAllCurConvos(response.data)
            console.log('Received convo list:', allCurConvos)
        })
        .catch(error => {
            console.log('Errors fetching all convos list:', error.response)
        })
        
    })

  
    
    return (
        <div className="container" style = {{whiteSpace: 'pre-line'}}>
            <p><strong>All logs</strong></p>
            <ul>
            {allCurConvos.map(curConvo => (
                <li key={curConvo.date}>
                    <Link to= {`/convolog/${curConvo.date}`}>{curConvo.date}</Link>
                </li>
            ))}
          </ul>
            
            
        </div>
    )
}

