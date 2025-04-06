import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useParams } from "react-router";
import { Link } from 'react-router-dom';
import Loader from '../components/Loader'
import api from '../components/api'

function ReportPage() {
    
    const { name } = useParams()
    const [chat_log, setChatLog] = useState()
    const [context, setContext] = useState<any[]>([]) 
    //const [cycles, setCycles] = useState() 
    //const [date, setDate] = useState()
    const [engine, setEngine] = useState()
    const [expectations, setExpectation] = useState()
    const [lead_name, setLeadName] = useState()
    //const [method, setMethod] = useState()
    const [model, setModel] = useState()
    const [output, setOutput] = useState()
    //const [potentialAgents, setPotentialAgents] = useState()
    const [task, setTask] = useState()
    //const [temperature, setTemp] = useState()
    const [chosenTeam, setChosenTeam] = useState<any[]>([])
    const [savedToLead, setSavedToLead] = useState<boolean>()
    const [isLoading, setLoadStatus] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null);

    const saveReportMemory = async (reportId:any) => {
        setLoadStatus(true)
        try {
            await api.post(`/save_report_memory/${reportId}/`)
            setSavedToLead(true)
            setLoadStatus(false)
        }
        catch (error:any) {
            console.log('Error fetching agents', error.response)
            setLoadStatus(false)
        }
    }
    useEffect(() => {
        const getReport = async() => {
            try {
                
                const response = await api.get(`/reports/${name}/`)
                setChatLog(response.data.chat_log)
                setContext(response.data.context)
                //setCycles(response.data.cycles)
                //setTemp(response.data.temperature)
                setTask(response.data.task)
                setOutput(response.data.output)
                setModel(response.data.model)
                setLeadName(response.data.lead_name)
                setExpectation(response.data.expectations)
                //setCycles(response.data.cycles)
                setEngine(response.data.engine)
                //setDate(response.data.date)
                setSavedToLead(response.data.savedToLead)
                setChosenTeam(response.data.chosen_team)
            }
            catch(error:any) {
                console.log('Error fetching agents', error.response)
            }
        }
        getReport()
        
        
    })

    const navigate = useNavigate();
    
    const deleteClicked = async () => {
        try {
            api.delete(`/reports/${name}/`)
            navigate('/reports')
        }
        catch(error:any) {
            console.log("error deleting report")
        }
    }

    return (
        <div className="container my-4">
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
            <h3>{name}</h3>
            
            <div className="mb-3">
                <h5 className="font-weight-bold">Links:</h5>
                <ul>
                    <li><a href={output} className="text-primary" target="_blank">Report text</a></li>
                    <li><a href={chat_log} className="text-primary" target="_blank">Chat log</a></li>
                </ul>
            </div>

            <div className="mb-3">
                <h5 className="font-weight-bold">Lead Information:</h5>
                <p><strong>Lead name:</strong> {lead_name}</p>
                <p><strong>Task:</strong> {task}</p>
            </div>

            <div className="mb-3">
                <h5 className="font-weight-bold">Chosen Agents:</h5>
                {chosenTeam.map((agent) => (
                    <Link to={`/agents/${agent.name}`} className="text-primary">
                        {agent.name} (click to navigate to agent page)
                    </Link>
                ))}

            </div>

            <div className="mb-3">
                <h5 className="font-weight-bold">Provided Context Files:</h5>
                <ul className="list-unstyled">
                    {context.map((file, index) => (
                        <li key={index}>
                            <a href={file.file} target="_blank" className="text-secondary">
                                {file.name}
                            </a>
                        </li>
                    ))}
                </ul>
            </div>

            <div className="mb-3">
                <p><strong>Engine:</strong> {engine}</p>
                <p><strong>Model:</strong> {model}</p>
                <p><strong>Expectations:</strong> {expectations}</p>
            </div>

            <div className="d-flex justify-content-start">
                <button type="button" className="btn btn-danger mr-2" onClick={deleteClicked}>Delete</button>
                <button disabled={savedToLead} type="button" className="btn btn-warning" onClick={() => saveReportMemory(name)}>
                    Save report in lead memory
                </button>
                {isLoading && <div>
                    <Loader />
                </div>}
            </div>
        </div>
  )
}

export default ReportPage