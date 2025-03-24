import PaperForm from '../components/PaperForm';
import React, { useState, useEffect } from 'react';
import axios from "axios";

function Reports () {
    const [reports, setReports] = useState<any[]>([])
    const [error, setError] = useState<string | null>(null);
    const [reload, setReload] = useState<number>(0)
    const deleteClicked = (id:any) => {
        console.log("DELETING AT")
        console.log(`http://localhost:8000/api/reports/${id}/`)
        axios({
            url: `http://localhost:8000/api/reports/${id}/`,
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
            url: "http://localhost:8000/api/reports/",
            method: "GET",
            headers: {
                authorization: "placer auth token"
            }
        })
        .then((response:any) => {
            setReports(response.data)
            console.log(reports)
        })
        .catch((error:any) => {
            console.log('Error fetching reports', error.response)
        })
    })

    
    return (
        <div>

        <h3>Current papers</h3>
        <div className="list-group">
        {reports.map((report) => (
            
            <div className="d-flex bd-highlight">
                <div className = "p-2 flex-fill bd-highlight">
                    <a 
                    href= {report.file}
                    className="list-group-item list-group-item-action"
                    target="_blank"
                    >
                    Download {report.name}
                    </a>
                </div>
                <div className = "p-2 flex-fill bd-highlight">
                <button type="button" className="btn btn-danger" onClick={() => deleteClicked(report.id)}>Delete</button>
                </div>

            </div>
        ))}
        </div>
        </div>


        

    );
}

export default Reports;