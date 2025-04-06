
import React, { useState, useEffect } from 'react';
import ReportForm from "../components/ReportForm"
import { useNavigate } from 'react-router-dom';
import { useLocation } from "react-router-dom"
import Instructions from "../components/Instructions"

function Home () {    
    const location = useLocation();
    const initData = location.state ?? {};

    const navigate = useNavigate();
    const [name, setName] = useState(initData.name || '')
    const [task, setTask] = useState(initData.task || '')
    const [description, setDescription] = useState(initData.description || '')
    const [expectations, setExpectations] = useState(initData.expectations || '')
    const [model, setModel] = useState(initData.model || '')
    const [context, setContext] = useState<File[]>(initData.context || []);
    const [cycles, setCycles] = useState(initData.cycles || '');
    const [reportGuidelines, setReportGuidelines] = useState(initData.reportGuidelines || '');
    const [method, setMethod] = useState(initData.method || '');
    const [temp, setTemp] = useState(initData.temp || '');
    const [engine, setEngine] = useState(initData.engine || '')
    const [lead, setLead] = useState(initData.lead || '');
    const [selectedInDBFiles, setSelectedInDBFiles] = useState<string[]>(initData.selectedInDBFiles || [])
    const [selectedAgents, setSelectedAgents] = useState<string[]>(initData.selectedAgents || [])
    const [error, setError] = useState<string | null>(null);
    const [showInstr] = useState<boolean>(() => {
        return localStorage.getItem("showInstr") === "true";
      });
    console.log(showInstr)
    const onSelectFileChange = (names: string[]) => {
        setSelectedInDBFiles(names)
    }
    const onSelectAgentChange = (names: string[]) => {
        setSelectedAgents(names)
        console.log("Seelcted agents:")
        console.log(selectedAgents)
    }
    const onContextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            console.log(e.target.files)
            const file_arr = Array.prototype.slice.call(e.target.files)
            
            const uploaded : any[] = [...context];
            file_arr.some((file) => {
                if (uploaded.findIndex((f) => f.name === file.name) === -1) {
                    uploaded.push(file)
                }
                
            })
          setContext(uploaded);
        }
    }
    useEffect(() => {
        localStorage.removeItem("showInstr");
      }, []);
      
    const formSubmit = (event: React.FormEvent) => {
        event.preventDefault()
        
        //reset all fields here
        navigate("/report_output", 
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

            <Instructions startingShow={showInstr}></Instructions>

            <h3>Generate a new report</h3>
            <ReportForm
                name = {name}
                onSelectFileChange={onSelectFileChange}
                onSelectAgentChange={onSelectAgentChange}
                task = {task}
                expectations = {expectations}
                uploadedFiles = {context}
                cycles = {cycles}
                description = {description}
                reportGuidelines = {reportGuidelines}
                method = {method}
                temperature = {temp}
                engine = {engine}
                model = {model}
                lead = {lead}
                onNameChange={(e:any) => setName(e.target.value)}
                onTaskChange={(e:any) => setTask(e.target.value)}
                onExpectationsChange={(e:any) => setExpectations(e.target.value)}
                onFilesChange={onContextChange}
                onDescriptionChange={(e:any) => setDescription(e.target.value)}
                onModelChange={(e:any) => setModel(e.target.value)}
                onCyclesChange={(e:any) => setCycles(e.target.value)}
                onReportGuidelinesChange = {(e:any) => setReportGuidelines(e.target.value)}
                onMethodChange = {(e:any) => setMethod(e.target.value)}
                onTemperatureChange = {(e:any) => setTemp(e.target.value)}
                onEngineChange = {(e:any) => setEngine(e.target.value)}
                onLeadChange = {(e:any) => setLead(e.target.value)}
                onSubmit = {formSubmit}
            />
            
            
        </div>
    )
}

export default Home;