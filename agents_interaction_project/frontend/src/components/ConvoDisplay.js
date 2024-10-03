import React, { useState, useEffect } from 'react';
import axios from "axios";
import ReactMarkdown from 'react-markdown';



export const ConvoDisplay = () => {
    const [convoInfo, setConvoInfo] = useState([])

    useEffect(() => {
        axios({
            url: "http://localhost:8000/api/get-latest-convo-log/",
            method: "GET",
            headers: {
                authorization: "placer auth token"
            },

        })
        .then(response => {
            setConvoInfo(response.data)
        })
        .catch(error => {
            console.log('Errors fetching convo_info list:', error.response)
        })
        
    })

  
    
    return (
        <div className="container" style = {{whiteSpace: 'pre-line'}}>
            <h1>Conversation log from today</h1>
            <p><strong>ID in knowledge base:</strong> {convoInfo.topic_id}</p>
            <p><strong>Topic text:</strong> {convoInfo.topic_text}</p>
            <p><strong>Topic text from:</strong> {convoInfo.title}</p>
            <p><strong>Created At:</strong> {convoInfo.date}</p>
            <p><strong>Engine:</strong> {convoInfo.engine}</p>
            <p><strong>Agent participants:</strong> {convoInfo.agents}</p>
            
            <p><strong>Conversation Log:</strong> 
            <ReactMarkdown>{convoInfo.log_text}</ReactMarkdown>
            </p>
        </div>
    )
}

