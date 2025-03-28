import LeadForm from "../components/LeadForm";
import React, { useState, useEffect } from 'react';
import axios from "axios";

function Leads () {
    const [name, setName] = useState('')
    const [description, setDescription] = useState('')
    const [leads, setLeads] = useState<any[]>([])
    const [error, setError] = useState<string | null>(null);
    const accessToken = localStorage.getItem("accessToken");

    useEffect(() => {
        axios({
            url: "http://localhost:8000/api/leads/",
            method: "GET",
            headers: {
                "Authorization":`Bearer ${accessToken}`
            }
        })
        .then((response:any) => {
            setLeads(response.data)
            //console.log(leads)
        })
        .catch((error:any) => {
            console.log('Error fetching team leads', error.response)
        })
    })
    
    const formSubmit = (event: React.FormEvent) => {
        
        event.preventDefault();
        const lead = {
            name: name,
            description: description
        }

        setError(null);
        axios({
            url: "http://localhost:8000/api/leads/",
            method: "POST",
            headers: {
                "Authorization":`Bearer ${accessToken}`
            },
            data: lead
        })
        .then(response => {
            console.log('New lead created:', response.data)
            setLeads([...leads, response.data]);
            
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
        setName('')
        setDescription('')
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
            <h3>Create a new Team Lead</h3>
            <LeadForm 
            name={name}
            description={description}
            onNameChange={(e) => setName(e.target.value)}
            onDescriptionChange={(e) => setDescription(e.target.value)}
            onSubmit={formSubmit}
            />
            <h3>Current team leads</h3>
            <div className="list-group">
            {leads.map((lead) => (
                <a href={`/leads/${lead.name}/`} className="list-group-item list-group-item-action">{lead.name}</a>
            ))}
            
            </div>
        </div>


        

    );
}

export default Leads;