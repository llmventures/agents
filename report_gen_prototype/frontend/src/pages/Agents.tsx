import AgentForm from "../components/AgentForm";
import React, { useState, useEffect } from 'react';
import Loader from "../components/Loader"
import api from '../components/api'
//Multi file upload: files should be a list of files
//OnFilesChange: setSelectedFiles to an array of file objs
//FormSubmit: map(for i in SelectedFiles): generate list that can represent 
//papers: cur_date, File
//Axios: post array of paper objs to /api/papers
//Create agent obj, rel key
//SEARCH FOR MORE EFFICIENT WAY TO DO THIS
function Agents () {
    const [isLoading, setLoadStatus] = useState<boolean>(false)
    const [name, setName] = useState('')
    const [role, setRole] = useState('')
    const [expertise, setExpertise] = useState('')
    const [error, setError] = useState<string | null>(null);
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]) 
    const [selectedInDBFiles, setSelectedInDBFiles] = useState<string[]>([])
    //selectedInDBFiles is a string: strings on paper objs should be unique
    //workflow:
    //On multiselect change: setSelectedFiles([string [] of file names selected])
    //Axios: selectedFiles[string] sent to backend
    //Backend" filter through papers db for selectedFiles, get paper obj and link
    //Note: need to check that papers aren't already linked
    //Also need to check that newly uploaded files are not already there

    //Check by name: already exists within papers db, instead of 
    //creating a new paper obj, just link existing one to agent
    //TODO: check if need options struct: can I instead just pass a list of
    //strings to the options param?
    //Then there would be no need to unpack here either
    const [agents, setAgents] = useState<any[]>([])

    useEffect(() => {
        const getAgents = async () => {
            try {
                const response = await api.get('/agents/')
                setAgents(response.data)
            }
            catch (error: any) {
                console.log('Error fetching agents', error.response)
            }
        }
        getAgents()
    })
    //handles change in the multiselect for papers in db
    const onSelectFileChange = (names: string[]) => {
        setSelectedInDBFiles(names)
    }
    const onFilesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            console.log(e.target.files)
            const file_arr = Array.prototype.slice.call(e.target.files)
            
            const uploaded : any[] = [...selectedFiles];
            file_arr.some((file) => {
                if (uploaded.findIndex((f) => f.name === file.name) === -1) {
                    uploaded.push(file)
                }
                
            })
          setSelectedFiles(uploaded);
          console.log("SEELCTED FILES:", selectedFiles)
        }
    };
    const formSubmit = (event: React.FormEvent) => {
        event.preventDefault()
        //create agent obj to be parsed on backend
        const formData = new FormData();
        
        formData.append("name", name)
        formData.append("role", role)
        formData.append("expertise", expertise)
        for (let i=0; i < selectedFiles.length; i++) {
            formData.append("files", selectedFiles[i])
            //console.log("File name before upload:", selectedFiles[i].name);

        }
        for (let i=0; i < selectedInDBFiles.length; i++) {
            formData.append("selFiles", selectedInDBFiles[i])
        }
        

        //post form data
        console.log("FORM DATA")
        console.log([...formData.entries()])
        setLoadStatus(true)
        const createAgent = async() => {
            try {
                const response = await api.post('/agents/', formData)
                console.log('New agent created:', response.data)
                setLoadStatus(false)
            }
            catch (Error: any) {
                setError("Error:" + Error.response.data.error)
                console.error(Error.response)
                setLoadStatus(false)
            }
        }
        createAgent()

        setName('')
        setRole('')
        setExpertise('')
        setSelectedFiles([])
        setError(null)
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
            <AgentForm 
            name={name}
            role={role}
            expertise={expertise}
            onSelectFileChange={onSelectFileChange}//On some amount in multiselect selected, setSelPapers to that list
            onNameChange={(e) => setName(e.target.value)}
            onExpertiseChange={(e) => setExpertise(e.target.value)}
            onRoleChange={(e) => setRole(e.target.value)}
            onFileChange={onFilesChange}
            uploadedFiles = {selectedFiles}
            onSubmit={formSubmit}
            />

            <div className="uploaded-files-list">
                {selectedFiles.map(file => (
                    <div>
                        {file.name}
                    </div>
                ))} 
            </div>
            {isLoading && <Loader />}
            <h3>Current agents</h3>
                <div className="list-group">
                {agents.map((agent) => (
                    <a href={`/agents/${agent.name}/`} className="list-group-item list-group-item-action">{agent.name}</a>
                ))}
                
                </div>
        </div>

    );
}

export default Agents;