import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useParams } from "react-router";
import api from "../components/api"


function AgentPage() {
    const { name } = useParams()
    const [role, setRole] = useState('')
    const [expertise, setExpertise] = useState('')
    const [files, setFiles] = useState<any[]>([]) 
    useEffect(() => {
        const getAgents = async () => {
            try {
                const response = await api.get(`/agents/${name}/`)
                setRole(response.data.role)
                setExpertise(response.data.expertise)
                setFiles(response.data.stored_papers)
            }
            catch (error: any) {
                console.log('Error fetching agents', error.response)
            }
        }
        getAgents()
    })

    const navigate = useNavigate();
    const deleteClicked = async () => {
        try {
            await api.delete(`agents/${name}/`)
            navigate('/agents')
        }
        catch (error: any) {
            console.log("error deleting agent")
        }
    }
    return (
        <div className="container my-4">
            <h3>{name}</h3>
            <div className="mb-3">
                <p><strong>Lead role:</strong> {role}</p>
                <p><strong>Lead expertise:</strong> {expertise}</p>
            </div>
            <div className="mb-3">
                <h5 className="font-weight-bold">Files:</h5>
                {files.map((file) => (
                    <a 
                    href= {file.file}
                    className="text-primary"
                    target="_blank"
                    >
                    Download {file.name}
                    </a>
                ))}

            </div>

            <div className="d-flex justify-content-start">
                <button type="button" className="btn btn-danger mr-2" onClick={deleteClicked}>Delete</button>
                
            </div>
        </div>
    )
}

export default AgentPage