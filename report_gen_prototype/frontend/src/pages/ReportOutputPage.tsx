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
    const subData = location.state;
    const hasFetched = useRef(false);
    const [isLoading, setLoadStatus] = useState<boolean>(false)
    const [report, setReport] = useState<any>(null)
    const [error, setError] = useState<string | null>(null);
    const [name, setName] = useState<string>("")

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
            navigate("/home")
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
        setName(subData?.name)
        //guard to make sure axios is only called once
        if (hasFetched.current) return;
        hasFetched.current = true;
        console.log("About to run an axios call")
        const formData = new FormData();
        formData.append("name", subData?.name)
        console.log(subData)
        console.log(subData?.name)
        console.log(subData?.selectedInDBFiles)
        formData.append("task", subData?.task)
        formData.append("description", subData?.description)
        formData.append("expectations", subData?.expectations)
        formData.append("model", subData?.model)
        for (let i=0; i < subData?.context.length; i++) {
            formData.append("context_files", subData?.context[i])
        }
        for (let i=0; i < subData?.selectedInDBFiles.length; i++) {
            formData.append("selFiles", subData?.selectedInDBFiles[i])
        }
        if (subData?.selectedAgents.length == 0) {
            formData.append("selAgents", "all")
        }
        else {
            for (let i=0; i < subData?.selectedAgents.length; i++) {
                formData.append("selAgents", subData?.selectedAgents[i])
            }
        }
        subData?.selectedAgents
        formData.append("cycles", subData?.cycles)
        formData.append("reportGuidelines", subData?.reportGuidelines)
        formData.append("method", subData?.method)
        formData.append("temperature", subData?.temp)
        formData.append("engine", subData?.engine)
        formData.append("lead", subData?.lead)
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
                <>
                <a 
                href= {report.output}
                className="list-group-item list-group-item-action"
                target="_blank"
                >
                View report
                </a>
                
                <a 
                href= {report.chat_log}
                className="list-group-item list-group-item-action"
                target="_blank"
                >
                View chatlog
                </a>
                
                </>
                )}
                
                
                <button disabled={deleteDisabled} type="button" className="btn btn-danger" onClick={() => deleteReport(name)}>Discard report</button>
                <button disabled={saveDisabled} type="button" className="btn btn-danger" onClick={() => saveReportMemory(name)}>Save report in lead memory</button>
                
                </div>
    );
    //const [selectedFile, setSelectedFile] = useState<File | null>(null);
    
}
export default ReportOutputPage;