import React, { useState, useEffect } from 'react';
import axios from "axios";
import { useLocation } from "react-router-dom"
import { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Loader from '../components/Loader'
import api from '../components/api'

function ReportOutputPage () {
    const navigate = useNavigate();
    const [deleteDisabled, setDeleteDisabled] = useState(false);
    const [savedToLead, setSavedToLead] = useState<boolean>(false)
    const location = useLocation();
    const subData = location.state || {};
    const [name, setName] = useState(subData.name || '')
    const [task, setTask] = useState(subData.task || '')
    const [description, setDescription] = useState(subData.description || '')
    const [expectations, setExpectations] = useState(subData.expectations || '')
    const [model, setModel] = useState(subData.model || '')
    const [context, setContext] = useState<File[]>(subData.context || []);
    const [cycles, setCycles] = useState(subData.cycles || '');
    const [reportGuidelines, setReportGuidelines] = useState(subData.reportGuidelines || '');
    const [method, setMethod] = useState('2');
    const [temp, setTemp] = useState(subData.temp || '');
    const [engine, setEngine] = useState(subData.engine || '')
    const [lead, setLead] = useState(subData.lead || '');
    const [selectedInDBFiles, setSelectedInDBFiles] = useState<string[]>(subData.selectedInDBFiles || [])
    const [selectedAgents, setSelectedAgents] = useState<string[]>(subData.selectedAgents || [])
    


    const hasFetched = useRef(false);
    const [isLoading, setLoadStatus] = useState<boolean>(false)
    const [report, setReport] = useState<any>(null)
    const [error, setError] = useState<string | null>(null);
    const accessToken = localStorage.getItem("accessToken");
    const [isLoggedIn, setLoggedIn] = useState<boolean | null>(false)
    const [username, setUsername] = useState("")

    const checkLoggedInUser = async () => {
        try {
            const token = localStorage.getItem("accessToken");
            if (!token) {
                setLoggedIn(false)
                if (location.pathname !== "/register") {
                    navigate("/login");
                }
                return
            }

            const response = await api.get("/user/");
            
            setLoggedIn(true)
            setUsername(response.data.username)
            //navigate("/")
        }
        catch(error) {
            setLoggedIn(false)
            setUsername("")
            if (location.pathname !== "/register") {
                navigate("/login");
            }

        }
    };
    
    const deleteReport = async(id:any) => {
        try {
            const response = await api.delete(`/reports/${id}`)
            setDeleteDisabled(true)
            console.log("navigating")
            navigate("/", 
                { state: { 
                    name:name,
                    task: task,
                    description: description,
                    expectation: expectations,
                    model: model,
                    context: context,
                    selectedInDBFiles: selectedInDBFiles,
                    selectedAgents: selectedAgents,
                    cycles: cycles,
                    reportGuidelines: reportGuidelines,
                    method: method,
                    temp: temp,
                    engine: engine,
                    lead: lead,
                } 
            });
        }
        catch (error: any) {
            console.log("errror deleting report")
        }
        
    }

    const saveReportMemory = async (reportId:any) => {
        setLoadStatus(true)
        try {
            const response = await api.post(`save_report_memory/${reportId}/`)
            setSavedToLead(true)
            setLoadStatus(false)
        }
        catch (error: any) {
            console.log('Error fetching agents', error.response)
            setLoadStatus(false)
        }
    }
    if (!subData) return <p>No formdata</p>;
    useEffect(() => {    
        checkLoggedInUser()   
        console.log(deleteDisabled)
        setName(subData?.name)
        //guard to make sure axios is only called once
        if (hasFetched.current) return;
        hasFetched.current = true;
        console.log("About to run an axios call")
        const formData = new FormData();
        formData.append("name", name)
        formData.append("task", task)
        formData.append("description", description)
        formData.append("expectations", expectations)
        formData.append("model", model || "mistral");
        for (let i=0; i < context.length; i++) {
            formData.append("context_files", context[i])
        }
        for (let i=0; i < selectedInDBFiles.length; i++) {
            formData.append("selFiles", selectedInDBFiles[i])
        }
        if (selectedAgents.length == 0) {
            formData.append("selAgents", "all")
        }
        else {
            for (let i=0; i < selectedAgents.length; i++) {
                formData.append("selAgents", selectedAgents[i])
            }
        }
        selectedAgents
        formData.append("cycles", cycles || '1')
        formData.append("reportGuidelines", reportGuidelines)
        formData.append("method", method)
        formData.append("temperature", temp || '0.8')
        formData.append("engine", engine || 'Ollama')
        formData.append("lead", lead)
        console.log("FORM DATA")
        console.log([...formData.entries()])
        setLoadStatus(true)
        const postReport = async() => {
            try {
                const response = await api.post('/reports', formData)
                console.log('New report generated:', response.data)
                setReport(response.data)
                setLoadStatus(false)
            }
            catch (Error:any) {
                console.log("error catching")
                console.error(Error)
                setLoadStatus(false)
                navigate("/", 
                    { state: { 
                        name:name,
                        task: task,
                        description: description,
                        expectations: expectations,
                        model: model,
                        context: context,
                        selectedInDBFiles: selectedInDBFiles,
                        selectedAgents: selectedAgents,
                        cycles: cycles,
                        reportGuidelines: reportGuidelines,
                        method: method,
                        temp: temp,
                        engine: engine,
                        lead: lead,
                        error: Error.response.data.error
                    } 
                });
            }
        }
        postReport();
    }, []);
    //what to do for report saving:
    //if not want to be saved, then delete the obj
    return (
        <div className="flex items-center justify-center h-screen">
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
            {isLoading && <div className="flex justify-center items-center h-screen">
                <Loader />
                Generating report...
            </div>}
        {(report != null && isLoading != true) && 
                (
                <div className="flex flex-col space-y-2">
                <a 
                href= {report.output}
                className="text-blue-500 underline block"
                target="_blank"
                >
                    View report
                </a>
                
                <a 
                href= {report.chat_log}
                className="text-blue-500 underline block"
                target="_blank"
                >
                View chatlog
                </a>
                <button disabled={deleteDisabled} type="button" className="btn btn-danger" onClick={() => deleteReport(name)}>Discard report</button>
                <button disabled={savedToLead} type="button" className="btn btn-danger" onClick={() => saveReportMemory(name)}>Save report in lead memory</button>
                
                </div>
                )}
                </div>
    );
    //const [selectedFile, setSelectedFile] = useState<File | null>(null);
    
}
export default ReportOutputPage;