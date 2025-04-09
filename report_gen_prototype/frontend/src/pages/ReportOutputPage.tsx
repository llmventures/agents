import { useState, useEffect } from 'react';
import { useLocation } from "react-router-dom"
import { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../components/api'

function ReportOutputPage () {
    const navigate = useNavigate();
    const bottomRef = useRef<HTMLDivElement>(null)
    const [curGenerating, setCurGenerating] = useState<string>("")
    const [moveOn, setMoveOn] = useState<boolean>(false)
    const [chosenTeam, setChosenTeam] = useState([])
    const [guidingQ, setGuidingQ] = useState([])
    const [chatLog, setChatLog] = useState<{ speaker: string; text: string }[]>([]);
    const [agentGoals, setAgentGoals] = useState<{ agent: string; goal: string }[]>([]);
    const [cycle, setCycle] = useState("0");
    const [deleteDisabled, setDeleteDisabled] = useState(false);
    const [savedToLead, setSavedToLead] = useState<boolean>(false)
    const location = useLocation();
    const subData = location.state || {};
    const [name, setName] = useState(subData.name || '')
    const [task] = useState(subData.task || '')
    const [description] = useState(subData.description || '')
    const [expectations] = useState(subData.expectations || '')
    const [model] = useState(subData.model || '')
    const [context] = useState<File[]>(subData.context || []);
    const [cycles] = useState(subData.cycles || '');
    const [reportGuidelines] = useState(subData.reportGuidelines || '');
    const [method] = useState('2');
    const [temp] = useState(subData.temp || '');
    const [engine] = useState(subData.engine || '')
    const [lead] = useState(subData.lead || '');
    const [selectedInDBFiles] = useState<string[]>(subData.selectedInDBFiles || [])
    const [selectedAgents] = useState<string[]>(subData.selectedAgents || [])
    


    const hasFetched = useRef(false);
    const [isLoading, setLoadStatus] = useState<boolean>(false)
    const [report, setReport] = useState<any>(null)
    const [error, setError] = useState<string | null>(null);

    const scrollToBottom = () => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    };
    const checkLoggedInUser = async () => {
        try {
            const token = localStorage.getItem("accessToken");
            if (!token) {
                if (location.pathname !== "/register") {
                    navigate("/login");
                }
                return
            }

            await api.get("/user/");
            //navigate("/")
        }
        catch(error) {
            if (location.pathname !== "/register") {
                navigate("/login");
            }

        }
    };
    
    const deleteReport = async(id:any) => {
        try {
            await api.delete(`/reports/${id}`)
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
    const getNewReport = async () => {
        
        //report should have been created in backend after done, so now fetch it
        try {
            const reportResponse = await api.get(`/reports/${name}/`)
            console.log('New report generated:', reportResponse.data)
            setReport(reportResponse.data)
        }
        catch (error:any) {
            console.log("error fetching newly created report")
        }
        setMoveOn(true)
    }
    const saveReportMemory = async (reportId:any) => {
        setLoadStatus(true)
        try {
            await api.post(`save_report_memory/${reportId}/`)
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
        formData.append("model", model || "gpt-4o");
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
        formData.append("engine", engine || 'openai')
        formData.append("lead", lead)
        console.log("FORM DATA")
        console.log([...formData.entries()])
        setLoadStatus(true)
        const postReport = async() => {
            try {
                const token = localStorage.getItem("accessToken");
                const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/reports/`, {
                    method: "POST",
                    headers: {
                      "Authorization": `Bearer ${token}`,
                    },
                    body: formData
                });
                console.log("RETURNED RESPONSE")
                console.log(response)
                if (!response.ok) {
                    throw new Error(`HTTP error: status: ${response.status}`);
                }
                if (!response.body) {
                    throw new Error("No response body found.");
                }

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let done = false;

                while (!done) {
                    const { done: chunkDone, value: chunk } = await reader.read();
                    done = chunkDone;
                    
                    const decodedChunk = decoder.decode(chunk, { stream: true }).trim();
                    
                    try {
                        console.log(`decoded chunk: ${decodedChunk}`)
                        const parsedChunk = JSON.parse(decodedChunk)
                        console.log(parsedChunk)
                        if (parsedChunk.status == "error") {
                            setError(parsedChunk.message)
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
                                    error: parsedChunk.message
                                } 
                            });
                            break;
                        }

                        if (parsedChunk === "END") {
                            setCurGenerating("END")
                            break;
                            
                        }
                        if (Array.isArray(parsedChunk)) {
                            //display logic
                            const responseType = parsedChunk[0]
                            if (responseType === "PROGRESS") {
                                if (parsedChunk[1] === "GENGOAL") {
                                    setCurGenerating(parsedChunk[2])
                                }
                                else {
                                    setCurGenerating(parsedChunk[1])
                                }
                            }
                            if (responseType === "CYCLE") {
                                setCycle(parsedChunk[1])
                            }
                            if (responseType === "TEAM") {

                                setChosenTeam(parsedChunk[1])
                            }
                            if (responseType === "GOAL") {
                                setAgentGoals((prevGoal) => [...prevGoal, { agent: parsedChunk[1], goal: parsedChunk[2] }])
                            }
                            if (responseType === "RESPONSE") {
                                setChatLog((prevLog) => [...prevLog, { speaker:parsedChunk[1], text:parsedChunk[2] }]);
                            }
                            if (responseType === "GUIDINGQ") {
                                const questions = parsedChunk[1].split(/\d+\.+/)
                                                                .map((q:string) => q.trim())
                                                                .filter((q:string) => q.length > 0);
                                setGuidingQ(questions)
                            }
                        }
                    }
                    catch (error:any){
                        console.error(error)
                    }
                }
                console.log(curGenerating)
                setLoadStatus(false)
                scrollToBottom()
            } 
            catch (error:any) {
                console.error("Error generating the report:", error);
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
                        error: error.response.data.error
                    } 
                });
            }
        }
        postReport();
    }, []);
    //what to do for report saving:
    //if not want to be saved, then delete the obj
    return (
        
        <div className="flex flex-col items-center p-4 space-y-4 w-full max-w-lg mx-auto">
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
            {(moveOn !== true) && (
                <div className="flex flex-col justify-center items-center h-screen space-y-6 p-6 bg-gray-50">
    

                    <div className="bg-white p-6 rounded-xl shadow-lg w-full max-w-2xl space-y-4">
                    <h2 className="text-xl font-bold text-gray-800 border-b pb-2">Report status</h2>
                    
                    <p className="text-md font-medium text-gray-700">
                        <strong>Chosen Team:</strong> 
                        {(curGenerating === "CHOOSETEAM" || curGenerating === "" || curGenerating === "SETUP") && (
                            <span className="loading">Generating</span>
                        )}
                        {chosenTeam.map((teamMember) => {
                            const goal = agentGoals.find((entry) => entry.agent === teamMember)?.goal;
                            return (
                                <div>
                                    {teamMember}
                                    {goal && (
                                        <span className="ml-2 text-gray-500">({goal})</span>
                                    )}
                                    {(curGenerating === teamMember) && (
                                        <span className="loading">Generating</span>
                                    )}
                                </div>
                            )
                        })}
                        
                    </p>
                    <p className="text-md font-medium text-gray-700">
                        <strong>Guiding Questions:</strong> 
                        {guidingQ.map((question, ind) => (
                            <p key={ind}>{question}</p>
                        ))}
                        {(curGenerating === "GUIDINGQ") && (
                            <span className="loading">Generating</span>
                        )}
                        </p>
                    </div>

                    <div className="p-6 w-full max-w-2xl bg-white rounded-xl shadow-lg">
                    <h2 className="text-xl font-bold text-gray-800 border-b pb-2">Chat Log</h2>
                    <div className="bg-gray-100 p-4 rounded-lg shadow-inner space-y-2 max-h-96 overflow-y-auto">
                        <p className="text-md font-medium text-gray-700">
                            <strong>Cycle:</strong>
                            {cycle}
                        </p>
                        {chatLog.map((entry, index) => (
                        <div
                            key={index}
                            className={`p-3 rounded-lg max-w-[80%] ${
                            entry.speaker === "l" 
                                ? "bg-blue-500 text-white self-end ml-auto" 
                                : "bg-gray-300 text-black self-start mr-auto"
                            }`}
                        >
                            <strong className="block font-semibold">{entry.speaker}:</strong>
                            <p>{entry.text}</p>
                            
                        </div>
                        ))}
                        {(curGenerating === "STARTCONVO") && (
                            <span className="loading">Generating</span>
                        )}
                        {(isLoading !== true) &&
                            <button type="button" className="btn btn-danger" onClick={() => getNewReport()}>View final report</button>
                        }  
                        <div ref={bottomRef}></div>
                    </div>
                    </div>
                </div>
                )}
        {(report != null && moveOn === true) && 
                (
                <div className="flex flex-col space-y-2">
                <div>
                    <a 
                    href= {report.output}
                    className="text-blue-500 underline block"
                    target="_blank"
                    >
                        View report
                    </a>
                </div>
                <div>
                    <a 
                    href= {report.chat_log}
                    className="text-blue-500 underline block"
                    target="_blank"
                    >
                    View chatlog
                    </a>
                </div>
                <button disabled={deleteDisabled} type="button" className="btn btn-danger" onClick={() => deleteReport(name)}>Discard report</button>
                <button disabled={savedToLead} type="button" className="btn btn-danger" onClick={() => saveReportMemory(name)}>Save report in lead memory</button>
                
                </div>
                )}
        </div>
    );
    //const [selectedFile, setSelectedFile] = useState<File | null>(null);
    
}
export default ReportOutputPage;