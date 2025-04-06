import { useState, useEffect } from 'react';
import api from "../components/api"

function Reports () {
    const [reports, setReports] = useState<any[]>([])
    const [error, setError] = useState<string | null>(null);
    
    useEffect(() => {
        const getReports = async() => {
            try {
                const response = await api.get('/reports/')
                setReports(response.data)
            }
            catch (error: any) {
                console.log('Error fetching reports', error.response)
            }
        }
        getReports();
    })

    
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
                </div>

            </div>
        ))}
        </div>
        </div>


        

    );
}

export default Reports;