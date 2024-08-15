import React, { useState, useEffect } from 'react';
import Select from 'react-select';

import axios from "axios";


export const CrewForm = () => {
    const [name, setName] = useState('')    
    const [task, setTask] = useState('')
    const [input_format, setInput] = useState('')
    const [output_format, setOutput] = useState('')
    const [agents, setAgents] = useState([]);
    const [cur_agents, setSelectedAgents] = useState([]);
    const [crews, setCrews] = useState([]);
    useEffect(() => {
        axios({
            url: "http://localhost:8000/api/agents/",
            method: "GET",
            headers: {
                authorization: "placer auth token"
            },
        })
        .then(response => {
            const cleanedResponse = response.data.map(agent => ({
                value: agent.name,
                label:agent.name
            }));
            //console.log("AGENTS: ", response.data)
            setAgents(cleanedResponse)
        })
 
        .catch(error => {
            console.log('Errors fetching crew list:', error.response)
        });
    });
    const formSubmit = (event) => {
        event.preventDefault();
        const crew = {
            //
            agents:cur_agents.map(agent => agent.value),
            name:name, 
            task:task, 
            input_format: input_format, 
            output_format: output_format,
            crews: crews
        };

        axios({
            url: "http://localhost:8000/api/crews/",
            method: "POST",
            headers: {
                authorization: "placer auth token"
            },
            data:crew,
        })
        .then(response => {
            console.log('Crew created:', response.data)
            setCrews([...crews, response.data])
        })

        .catch(error => {
            console.log('Errors:', error.response)
        });
        

        setName('');
        setAgents('');
        setTask('');
        setOutput('');
        setInput('');

    };

    /*const deleteCrew = (id) => {
        console.log(`ID IS: http://localhost:8000/api/agents/${id}/`);
        axios.delete(`http://localhost:8000/api/agents/${id}/`)
        .then(response => {
            console.log('Agent deleted')
            setAgents(agents.filter(agent => agent.id !== id))
        })
        .catch(error => {
            console.log('Errors with deleting agents:', error.response)
        });
    */
    return (
        <div className="container">
          <h1>Create a New Agent</h1>
          <form onSubmit={formSubmit}>
            <label>Agents:
            <Select
                isMulti
                name="Agents"
                options={agents}
                className="basic-multi-select"
                classNamePrefix="select"
                onChange = {setSelectedAgents}
            />
            </label>
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
              <label htmlFor="task">Task</label>
              <input
                type="text"
                id="task"
                className="form-control"
                value={task}
                onChange={(e) => setTask(e.target.value)}
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
          
        </div>

      );
    };
//export default AgentForm;

