import React, { useState, useEffect } from 'react';
import axios from "axios";

export const AgentForm = () => {
    const [name, setName] = useState('')
    const [role, setRole] = useState('')
    const [goal, setGoal] = useState('')
    const [backstory, setBackStory] = useState('')
    const [input_format, setInput] = useState('')
    const [output_format, setOutput] = useState('')
    const [agents, setAgents] = useState([]);


    useEffect(() => {
        axios({
            url: "http://localhost:8000/api/agents/",
            method: "GET",
            headers: {
                authorization: "placer auth token"
            },
        })
        .then(response => {
            setAgents(response.data)
        })
 
        .catch(error => {
            console.log('Errors fetching agent list:', error.response)
        });
    });
    const formSubmit = (event) => {
        event.preventDefault();

        const agent = {
            name:name, 
            role:role, 
            goal:goal,
            backstory:backstory,
            input_format: input_format, 
            output_format: output_format
        };

        axios({
            url: "http://localhost:8000/api/agents/",
            method: "POST",
            headers: {
                authorization: "placer auth token"
            },
            data:agent,
        })
        .then(response => {
            console.log('Agent created:', response.data)
            setAgents([...agents, response.data])
        })

        .catch(error => {
            console.log('Errors:', error.response)
        });
        

        setName('');
        setRole('');
        setGoal('');
        setBackStory('');
        setOutput('');
        setInput('');

    };

    const deleteAgent = (id) => {
        //Check first if the agent is in a crew, if so do not execute and give a notice to remove it first
        console.log(`ID IS: http://localhost:8000/api/agents/${id}/`);
        axios.delete(`http://localhost:8000/api/agents/${id}/`)
        .then(response => {
            console.log('Agent deleted')
            setAgents(agents.filter(agent => agent.id !== id))
        })
        .catch(error => {
            console.log('Errors with deleting agents:', error.response)
        });
    }

    return (
        <div className="container">
          <h1>Create a New Agent</h1>
          <form onSubmit={formSubmit}>
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
          <h2>Current Agents</h2>
          <ul>
            {agents.map(agent => (
                <li key={agent.name}>
                    {agent.name} - {agent.role} 
                    <button onClick={() => deleteAgent(agent.name)}>Delete</button>
                </li>
            ))}
          </ul>
        </div>

      );
    };
//export default AgentForm;

