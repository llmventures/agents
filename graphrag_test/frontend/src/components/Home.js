import { useState, useCallback } from 'react';
import axios from "axios";

import {
  ReactFlow,
  Controls,
  Background,
  applyNodeChanges,
  applyEdgeChanges,
  addEdge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes = [];
const initialEdges = [];

export const Home = () => {
    const [nodes, setNodes] = useState(initialNodes);
    const [edges, setEdges] = useState(initialEdges);
    const [name, setName] = useState('')
    const [role, setRole] = useState('')
    const [goal, setGoal] = useState('')
    const [backstory, setBackStory] = useState('')
    const [input_format, setInput] = useState('')
    const [output_format, setOutput] = useState('')




    const onNodesChange = useCallback(
        (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
        [],
      );
    const onEdgesChange = useCallback(
        (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
        [],
    );
    
    const onConnect = useCallback(
        
        (params) => setEdges((eds) => addEdge(params, eds)),
        [],
    );

    const nodeSubmit = (event) => {
        
        event.preventDefault()
        const node_id = `node_${nodes.length + 1}`;
        const newNode = {
            id: node_id,
            data: { 
                label: `Name:${name} Role:${role} Backstory:${backstory} Input format:${input_format} Output format:${output_format}`,
                Name: name,
                Role: role,
                Backstory: backstory,
                Goal: goal,
                input_format: input_format,
                output_format: output_format,
            },
            position: { x: Math.random() * 500, y: Math.random() * 500 }
        }
        setNodes((nds) => [...nds, newNode]);

        setName('');
        setRole('');
        setGoal('');
        setBackStory('');
        setOutput('');
        setInput('');


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
  return (
    <div>
    <h1>Create a New Agent</h1>
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
              <label htmlFor="role">Role</label>
              <input
                type="text"
                id="role"
                className="form-control"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="goal">Goal</label>
              <input
                type="text"
                id="goal"
                className="form-control"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="backstory">Backstory</label>
              <input
                type="text"
                id="backstory"
                className="form-control"
                value={backstory}
                onChange={(e) => setBackStory(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="input_format">Input format</label>
              <input
                type="text"
                id="input_format"
                className="form-control"
                value={input_format}
                onChange={(e) => setInput(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="output_format">Output format</label>
              <input
                type="text"
                id="output_format"
                className="form-control"
                value={output_format}
                onChange={(e) => setOutput(e.target.value)}
                required
              />
            </div>
            
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </form>
    
    <div style={{ width: '100%', height: '500px' }}>
    
      <ReactFlow
        nodes={nodes}
        onNodesChange={onNodesChange}
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
    </div>
  );
}

