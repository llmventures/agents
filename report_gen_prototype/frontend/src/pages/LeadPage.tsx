import { useParams } from "react-router";
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import api from '../components/api'


function LeadPage() {
    const navigate = useNavigate();
    const deleteClicked = async () => {
        try {
            api.delete(`/leads/${name}/`)
            navigate('/leads')
        }
        catch (error: any) {
            console.log("error deleting lead")
        }
    }

    const { name } = useParams()

    console.log(name)
    const [description, setDescription] = useState('')
    const [reports, setReports] = useState<any[]>([])
    useEffect(() => {
        const getLead = async() => {
            try {
                const response = await api.get(`/leads/${name}/`)
                console.log(response)
                setDescription(response.data.description)
                setReports(response.data.reports)
            }
            catch (error:any)  {
                console.log('Error fetching team lead', error.response)
            }
        }
        getLead()
        
    })
    return (
        <div className="container my-4">
            <h3>{name}</h3>
            <div className="mb-3">
                <p><strong>Lead description:</strong> {description}</p>
            </div>
            <div className="mb-3">
                <h5 className="font-weight-bold">Reports generated with this lead:</h5>
                {reports.map((report) => (
                    <Link to={`/reports/${report.name}`} className="text-primary">
                        {report.name} (click to navigate to report page)
                    </Link>
                ))}

            </div>

            <div className="d-flex justify-content-start">
                <button type="button" className="btn btn-danger mr-2" onClick={deleteClicked}>Delete</button>
                
            </div>
        </div>
        
  )
}

export default LeadPage