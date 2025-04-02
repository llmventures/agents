import PaperForm from '../components/PaperForm';
import React, { useState, useEffect } from 'react';
import axios from "axios";
import api from "../components/api"

function Reports () {
    const [reports, setReports] = useState<any[]>([])
    const [error, setError] = useState<string | null>(null);
    const [reload, setReload] = useState<number>(0)
    const accessToken = localStorage.getItem("accessToken");
    const deleteClicked = async (id:any) => {
        try {
            const response = api.delete(`/reports/${id}/`)
            setReload(reload + 1)
        }
        catch (error:any) {
            console.log("error deleting report")
        }
    }
    
    useEffect(() => {
        const getReports = async() => {
            try {
                const response = await api.get('/report/')
                setReports(response.data)
                console.log(reports)
            }
            catch (error: any) {
                console.log('Error fetching reports', error.response)
            }
        }
        getReports();
    })

    
    return (
        <div>

        <h3>Current reports</h3>
        <div className="list-group">
        {reports.map((report) => (
            
            <div className="d-flex bd-highlight">
                <div className = "p-2 flex-fill bd-highlight">
                    <a 
                    href= {`/reports/${report.name}/`}
                    className="list-group-item list-group-item-action"
                    >
                    {report.name}
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