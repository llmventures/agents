import React, { useState, useEffect } from 'react';
import axios from "axios";
import ReactMarkdown from 'react-markdown';
import { useParams } from "react-router-dom";


export const SpecificConvo = () => {
    let {date} = useParams();
    console.log(date)
    const [log, setLog] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        axios({
            url: `http://localhost:8000/api/convo-logs/${date}`,
            method: "GET",
            headers: {
                authorization: "placer auth token"
            },

        })
        .then(response => {
            setLog(response.data)
            setLoading(false)
        })
        .catch(error => {
            console.log('Errors fetching specific convo:', error.response)
            setLoading(false)
        })
        
    })
    if (loading) {
        return <div>Loading</div>;
    }

    if (!log) {
        return <div> Item not found</div>;
    }
    return (
        <div className="container" style = {{whiteSpace: 'pre-line'}}>
            <h1>Conversation log at date</h1>
            <p><strong>ID in knowledge base:</strong> {log.topic_id}</p>
            <p><strong>Topic text:</strong> {log.topic_text}</p>
            <p><strong>Topic text from:</strong> {log.title}</p>
            <p><strong>Created At:</strong> {log.date}</p>
            <p><strong>Engine:</strong> {log.engine}</p>
            <p><strong>Agent participants:</strong> {log.agents}</p>
            
            <p><strong>Conversation Log:</strong> 
            <ReactMarkdown>{log.log_text}</ReactMarkdown>
            </p>
        </div>
    )

}
