import { useState, useCallback } from 'react';
import axios from "axios";
import TaskNode from './TaskNode'

import {
  ReactFlow,
  Controls,
  Background,
  applyNodeChanges,
  applyEdgeChanges,
  SmoothStepEdge,
  addEdge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes = [
];
const nodeTypes = {
    taskNode: TaskNode,
};

const edgeTypes = {
    smoothstep: SmoothStepEdge,
}

const initialEdges = [];


const ContextForms = ({ nodeData={}, handleFieldChange, setName, name, nodeSubmit}) => (
    <div>
        <form onSubmit = {nodeSubmit}>
            <div className = "form-group">
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input
                type="text"
                id="name"
                className="form-control"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="Context links">Context links: (paste in each link, followed by a comma and no space)</label>
              <input
                type="text"
                id="links"
                name="links"
                className="form-control"
                value={nodeData.links}
                onChange={handleFieldChange}
                required
              />
            </div>
            </div>
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
        </form>
    </div>
)

const InputForms = ({ nodeData={}, handleFieldChange, setName, name, nodeSubmit}) => (
    <div>
        <form onSubmit = {nodeSubmit}>
            <div className = "form-group">
            <div className="form-group">
              <label htmlFor="links">Links: type n/a if using other field</label>
              <input
                type="text"
                id="links"
                name="links"
                className="form-control"
                value={nodeData.links}
                onChange={handleFieldChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="Context links">Text input: type n/a if using other field </label>
              <input
                type="text"
                id="text"
                name="text"
                className="form-control"
                value={nodeData.text}
                onChange={handleFieldChange}
                required
              />
            </div>
            </div>
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
        </form>
    </div>
)

const TaskForms = ({ nodeData={}, handleFieldChange, setName, name, nodeSubmit}) => (
    <div>
        <form onSubmit={nodeSubmit}>
            <div className="form-group">
                <label htmlFor="name">Name</label>
                <input
                    type="text"
                    id="name"
                    className="form-control"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
            </div>
            <div className="form-group">
                <label htmlFor="RunOrder">task run order</label>
                <input
                    type="number"
                    id="task_time"
                    name="task_time"
                    className="form-control"
                    value={nodeData.task_time}
                    onChange={handleFieldChange}
                    required
                />
            </div>
            <div className="form-group">
                <label htmlFor="Description">Description</label>
                <input
                    type="text"
                    id="description"
                    name="description"
                    className="form-control"
                    value={nodeData.description}
                    onChange={handleFieldChange}
                    required
                />
            </div>
            <div className="form-group">
              <label htmlFor="input_format">Input format</label>
              <input
                type="text"
                id="input_format"
                name="input_format"
                className="form-control"
                value={nodeData.input_format}
                onChange={handleFieldChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="output_format">Output format</label>
              <input
                type="text"
                id="output_format"
                name="output_format"
                className="form-control"
                value={nodeData.output_format}
                onChange={handleFieldChange}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
            </form>
    </div>
)


const AgentForms = ({ nodeData={}, handleFieldChange, setName, name, nodeSubmit}) => (
    <div>
        <form onSubmit={nodeSubmit}>
          <div className = "form-group">
                <select value={nodeData.agent_type} name = "agent_type" onChange = {handleFieldChange}>
                    <option value="basic_apicall">Basic api call</option>
                    <option value="graph_rag">Graph rag</option>
                </select>
            </div>
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input
                type="text"
                id="name"
                className="form-control"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="role">Role</label>
              <input
                type="text"
                id="role"
                name="role"
                className="form-control"
                value={nodeData.role}
                onChange={handleFieldChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="goal">Goal</label>
              <input
                type="text"
                id="goal"
                className="form-control"
                name="goal"
                value={nodeData.goal}
                onChange={handleFieldChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="backstory">Backstory</label>
              <input
                type="text"
                id="backstory"
                className="form-control"
                name="backstory"
                value={nodeData.backstory}
                onChange={handleFieldChange}
                required
              />
            </div>
            
            
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </form>
    </div>
    
)




export const Home = () => {
    const [nodes, setNodes] = useState(initialNodes);
    const [edges, setEdges] = useState(initialEdges);
    const [nodetype, setNodeType] = useState('agent')
    const [nodeData, setNodeData] = useState({});
    const [name, setName] = useState('')
    const [cur_edge_type, setCurEdgeType] = useState('output->input')
    /*
    const [role, setRole] = useState('')
    const [goal, setGoal] = useState('')
    const [agent_type, setAgentType] = useState('basic_apicall')
    
    const [backstory, setBackStory] = useState('')
    const [input_format, setInput] = useState('')
    const [output_format, setOutput] = useState('')
*/


    const handleFieldChange = useCallback( async (e) => {
        console.log("REFRESH REFRESH")
        const {name, value} = e.target;
        setNodeData((prev_data) => ({
            ...prev_data,
            [name]: value,

        }));
    })
    const onNodesChange = useCallback(
        async (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
        [],
      );
    const onEdgesChange = useCallback(
        async (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
        [],
    );
    
    const onConnect = useCallback(
        
        (params) => {
            
            const source = params.source;
            const target = params.target;
            
            console.log("SOURCE:",source)
            console.log("NODES:", nodes)
            const source_name = nodes.find(node=>node.id == source)
            const target_name = nodes.find(node=>node.id == target)

            console.log("SOURCE NAME",source_name)
            const source_type = source_name.data.Type
            const target_type = target_name.data.Type
            const edgeInst = {
                ...params,
                relation_type: `${source_type} -> ${target_type}`,
                
            }
            setEdges((eds) => addEdge(edgeInst, eds));
        },   
        [cur_edge_type, nodes],
    );
    
    const nodeSubmit = async (event) => {
        
        event.preventDefault()
        const node_id = `node_${nodes.length + 1}`;
        const newNode = {
            type: 'taskNode',
            id: node_id,
            data: { 
                label: `Name:${name}, Type:${nodetype} - ${Object.entries(nodeData)
                    .map(([key, value]) => `${key}:${value}`)
                    .join(' ')}`,
                Name: name,
                Type: nodetype,
                ...nodeData,
            },
            position: { x: Math.random() * 500, y: Math.random() * 500 }
        }
        setNodes((nds) => [...nds, newNode]);
        console.log("SETTING A NODE")
        console.log(nodes)
        setName('');
        setNodeData({});
        

    }

    
    const handleSubmit = () => {

        const idToName = nodes.reduce((named, node) => {
            named[node.id] = node.data.Name;
            return named;
        }, {});

        const fixedEdges = edges.map(edge => ({
            ...edge,
            source: idToName[edge.source],
            target: idToName[edge.target],
        }));
        
        const data = { nodes, fixedEdges };
        console.log("DATA TO BE SENT TO BACKEND: ", data)
        axios({
            url: "http://localhost:8000/api/crew-graphes/",
            method: "POST",
            headers: {
                authorization: "placer auth token"
            },
            data:data,
        })
        .then(response => {
            console.log("Graph created:", response.data)
        })
    
        .catch(error => {
            console.log('Errors creating graph:', error.response)
        });
    }
    const handleRun = (event) => {
        event.preventDefault();
        axios.post("http://localhost:8000/api/run-crew/")
        .then(response => {
            console.log("Crew running output created:", response.data)
        })
    
        .catch(error => {
            console.log('Errors running crew:', error.response)
        });
    }

  return (
    
    <div>
    
    <h1>Create a New Node</h1>
    <div className = "form-group">
            <select value={cur_edge_type} onChange = {(e) => setCurEdgeType(e.target.value)}>
                <option value="task output->task input">Output to input</option>
                <option value="context->agent">context to agent</option>
                <option value="agent->task">agent to task</option>
                <option value="collaborator<->collaborator">Collaborator to collaborator</option>
                <option value="supervisor->subordinate">Supervisor to subordinate</option>
                <option value="self->self(prompt optimization loop)">self to self</option>
            </select>
        </div>
        <div>
        <div className = "form-group">
            <label htmlFor="nodeType">Choose node type:</label>
            <select value = {nodetype} onChange = {(e) => setNodeType(e.target.value)}>
                <option value="agent">Agent</option>
                <option value="context">Context</option>
                <option value="initial_input">Initial input</option>
                <option value="task">Task</option>
            </select>

            {nodetype && (
                <div>
                    {nodetype === 'agent' && <AgentForms nodeData={nodeData} handleFieldChange={handleFieldChange} setName={setName} name={name} nodeSubmit={nodeSubmit}/>}
                    {nodetype === 'context' && <ContextForms nodeData={nodeData} handleFieldChange={handleFieldChange} setName={setName} name={name} nodeSubmit={nodeSubmit}/>}
                    {nodetype === 'task' && <TaskForms nodeData={nodeData} handleFieldChange={handleFieldChange} setName={setName} name={name} nodeSubmit={nodeSubmit}/>}
                    {nodetype === 'initial_input' && <InputForms nodeData={nodeData} handleFieldChange={handleFieldChange} setName={setName} name={name} nodeSubmit={nodeSubmit}/>}
                </div>
            )}
        </div>
          
        </div>

    COMMENT
    <div style={{ width: '100%', height: '500px' }}>
    
      <ReactFlow
        nodes={nodes}
        nodeTypes = {nodeTypes}
        onNodesChange={onNodesChange}
        edgeTypes={edgeTypes}
        edges={edges}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
      >
        <Background />
        <Controls />
      </ReactFlow>
      
    </div>
    <button onClick={handleSubmit}>Save Changes</button>
    <button onClick={handleRun}>Run current crew</button>

    </div>
  );
}

