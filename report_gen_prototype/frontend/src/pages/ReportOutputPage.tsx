import React, { useState, useEffect } from 'react';
import axios from "axios";
import { useLocation } from "react-router-dom"
import { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Loader from '../components/Loader'


function ReportOutputPage () {
    const navigate = useNavigate();
    const [deleteDisabled, setDeleteDisabled] = useState(false);
    const [saveDisabled, setSaveDisabled] = useState(false);
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

    const deleteReport = (id:any) => {
        axios({
            url: `http://localhost:8000/api/reports/${id}/`,
            method: "DELETE",
            headers: {
                authorization: "placer auth token"
            }
        })
        .then(response => {
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
        })
    }

    const saveReportMemory = (reportId:any) => {
        axios({
            url: `http://localhost:8000/api/save_report_memory/${reportId}/`,
            method: "DELETE",
            headers: {
                authorization: "placer auth token"
            }
        })
        .then(response => {
            setSaveDisabled(true)
        })
    }
    if (!subData) return <p>No formdata</p>;
    useEffect(() => {       
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
        formData.append("model", model)
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
        formData.append("cycles", cycles)
        formData.append("reportGuidelines", reportGuidelines)
        formData.append("method", method)
        formData.append("temperature", temp)
        formData.append("engine", engine)
        formData.append("lead", lead)
        console.log("FORM DATA")
        console.log([...formData.entries()])
        setLoadStatus(true)
        axios({
            url: "http://localhost:8000/api/reports/",
            method: "POST",
            headers: {
                authorization: "placer auth"
            },
            data: formData
        })
        .then(response => {
            console.log('New report generated:', response.data)
            setReport(response.data)
            setLoadStatus(false)
            
            
        })
        .catch((Error) => {
            //setError("Error:" + Error.response.data.error)
            console.log("error catching")
            console.error(Error)
            setLoadStatus(false)
        })
    }, []);
    //what to do for report saving:
    //if not want to be saved, then delete the obj
    return (
        <div>{isLoading && <Loader />}
        {(report != null && isLoading != true) && 
                (
                <div>
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
                <button disabled={saveDisabled} type="button" className="btn btn-danger" onClick={() => saveReportMemory(name)}>Save report in lead memory</button>
                
                </div>
                )}
                </div>
    );
    //const [selectedFile, setSelectedFile] = useState<File | null>(null);
    
}
export default ReportOutputPage;