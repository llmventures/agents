import React, { useState, useEffect } from 'react';
import MultiselectPapers from './MultiselectPapers';
import MultiselectAgents from './MultiselectAgents';
import api from '../components/api'
interface ReportFormProps {
    /*name = models.CharField(max_length = 50)
    date = models.DateTimeField()
    task= models.CharField(max_length = 1000)
    expectations=models.CharField(max_length = 1000)
    context=models.ManyToManyField(Paper, related_name='reports')
    cycles=models.IntegerField()
    report_guidelines=models.CharField(max_length = 1000)
    method=models.IntegerField(),
    temperature=models.FloatField(),
    engine = models.CharField(max_length = 50),
    lead = models.ForeignKey(TeamLead, on_delete=models.SET_NULL, null=True,related_name='reports')  */
    name: string;//char field
    task: string;//char field
    expectations: string;// char field
    reportGuidelines: string;//char field
    description : string;
    uploadedFiles : File[]//for context
    cycles: string;
    method: string; //from dropdown
    temperature: string; //bounded
    engine: string; //dropdown
    model: string; //dropdown
    lead: string; //dropdown
    
    onSelectFileChange: (names: string[]) => void;
    onSelectAgentChange: (names: string[]) => void;
    onNameChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onTaskChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onExpectationsChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onReportGuidelinesChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onDescriptionChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onFilesChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onCyclesChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onMethodChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
    onTemperatureChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onEngineChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
    onModelChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
    onLeadChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
    onSubmit: (e: React.FormEvent) => void;
}
function ReportForm({name, task, onSelectFileChange, onSelectAgentChange, expectations, description,reportGuidelines, uploadedFiles, cycles, temperature, onFilesChange,onNameChange, onTaskChange, onLeadChange,onCyclesChange, onExpectationsChange, onEngineChange, onReportGuidelinesChange, onModelChange, onDescriptionChange, onTemperatureChange,onSubmit}: ReportFormProps) {
    const [leadsList, setLeadsList] = useState<any[]>([])
    useEffect(() => {
        const getLeads = async() => {
            try {
                const response = await api.get('/leads/');
                setLeadsList(response.data)
            }
            catch(error: any) {
                console.log('Error fetching team leads', error.response)
            }
        }
        getLeads()
        
    })
    
    
    return (
        <form onSubmit={onSubmit}>
        <div className="mb-3">
            <label htmlFor="name" className="form-label">Name</label>
            <input 
            type="text" 
            className="form-control" 
            id="name"
            value={name}
            onChange={onNameChange}
            required
            />
        </div>
        <div className="mb-3">
            <label htmlFor="description" className="form-label">Description</label>
            <input 
            type="text" 
            className="form-control" 
            id="description"
            value={description}
            onChange={onDescriptionChange}
            required
            />
        </div>
        <div className="mb-3">
            <label htmlFor="task" className="form-label">Task</label>
            <input 
            type="text" 
            className="form-control input-lg" 
            id="description"
            value={task}
            onChange={onTaskChange}
            required
            />
        </div>
        <div className="mb-3">
            <label htmlFor="task" className="form-label">Expectations</label>
            <input 
            type="text" 
            className="form-control" 
            id="description"
            value={expectations}
            onChange={onExpectationsChange}
            required
            />
        </div>
        <div className="mb-3">
            <label htmlFor="reportGuidelines" className="form-label">Report Guidelines</label>
            <input 
            type="text" 
            className="form-control" 
            id="report guidelines"
            value={reportGuidelines}
            onChange={onReportGuidelinesChange}
            required
            />
        </div>

        <MultiselectAgents passNamesToParent={onSelectAgentChange}/>
        <MultiselectPapers passNamesToParent={onSelectFileChange}/>
        
        <div className="mb-3">
            <label htmlFor="file" className="form-label">Context files pdf</label>
            <input 
            className="form-control" 
            type="file" 
            id="formFile" 
            multiple
            onChange={onFilesChange}
            />
        </div>
        <div className="uploaded-files-list">
            {uploadedFiles.map(file => (
                <div>
                    {file.name}
                </div>
            ))} 
        </div>


        <div className="mb-3">
            <label htmlFor="reportGuidelines" className="form-label">Number of cycles (leave blank for 1)</label>
            <input 
            type="number" 
            className="form-control" 
            id="cycles"
            value={cycles}
            onChange={onCyclesChange}
            
            />
        </div>

        <div className="mb-3">
            <label htmlFor="reportGuidelines" className="form-label">Temperature (leave blank for 0.8)</label>
            <input 
            type="number" 
            className="form-control" 
            id="temp"
            value={temperature}
            onChange={onTemperatureChange}
            
            />
        </div>
        {/*
        <div className="select">
            <label htmlFor="method" className="form-label">Method</label>
            <select 
            className="form-select"
            onChange={onMethodChange}
            >
            <option selected>Choose conversation method</option>
            <option value="1">1. </option>
            <option value="2">2. </option>
            required
            </select>
            
        </div>
        */}
        <div className="select">
            <label htmlFor="method" className="form-label">Engine (leave blank for openai)</label>
            <select 
            className="form-select"
            onChange={onEngineChange}
            >
            <option selected>Choose engine</option>
            <option value="Ollama" disabled>Ollama </option>
            <option value="openai">OpenAI </option>
            </select>
           
        </div>
        <div className="select">
            <label htmlFor="method" className="form-label">Model (leave blank for gpt4o)</label>
            <select 
            className="form-select"
            onChange={onModelChange}
            >
            <option selected>Choose model</option>
            <option value="mistral" disabled>Ollama: mistral </option>
            <option value="gpt-4o">gpt-4o</option>
            </select>
           
        </div>
        
        <div className="select">
            <label htmlFor="method" className="form-label">Lead</label>
            <select 
            className="form-select"
            onChange={onLeadChange}
            required
            >
            <option selected value="">Choose lead</option>
            {leadsList.map((cur_lead) => (
                <option value={cur_lead.name}>{cur_lead.name} </option>
            ))}
            </select>
           
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
        </form>

    )
}

export default ReportForm; 