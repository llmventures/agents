
import React, { useState, useEffect, Component } from 'react';
import ReportForm from "../components/ReportForm"
import { useNavigate } from 'react-router-dom';



function Home () {
    const navigate = useNavigate();
    const [name, setName] = useState('')
    const [task, setTask] = useState('')
    const [description, setDescription] = useState('')
    const [expectations, setExpectations] = useState('')
    const [model, setModel] = useState('')
    const [context, setContext] = useState<File[]>([]);
    const [cycles, setCycles] = useState('');
    const [reportGuidelines, setReportGuidelines] = useState('');
    const [method, setMethod] = useState('');
    const [temp, setTemp] = useState('');
    const [engine, setEngine] = useState('')
    const [lead, setLead] = useState('');
    const [selectedInDBFiles, setSelectedInDBFiles] = useState<string[]>([])
    const [selectedAgents, setSelectedAgents] = useState<string[]>([])
    
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