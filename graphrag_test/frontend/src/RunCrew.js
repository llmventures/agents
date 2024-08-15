import React, { useState, useEffect } from 'react';
import Select from 'react-select';

import axios from "axios";


export const RunCrew = () => {
    const [cur_crew, setCurCrew] = useState([]);
    const [crews, setCrews] = useState([]);
    useEffect(() => {
        axios({
            url: "http://localhost:8000/api/crews/",
            method: "GET",
            headers: {
                authorization: "placer auth token"
            },
        })
        .then(response => {
            const cleanedResponse = response.data.map(crews => ({
                value: crews.name,
                label:crews.name
            }));
            //console.log("AGENTS: ", response.data)
            setCrews(cleanedResponse)
        })
 
        .catch(error => {
            console.log('Errors fetching crew list:', error.response)
        });
    });
    const formSubmit = (event) => {
      const selected_crew = {
        crew_id: setCurCrew
      }
      axios({
          url: "http://localhost:8000/api/run-crew/",
          method: "POST",
          headers: {
              authorization: "placer auth token"
          },
          data:selected_crew
      })
      .then(response => {
        console.log('Crew Output:', response.data.output);
      })
      .catch(error => {
          console.error('Error running crew:', error);
      });

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
          <h1>Run a crew</h1>
          <form onSubmit={formSubmit}>
            <label>Crews:
            <Select
                name="Crews"
                options={crews}
                className="basic-single"
                classNamePrefix="select"
                onChange={setCurCrew}
            />
            </label>
            
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </form>
          
        </div>

      );
    };
//export default AgentForm;

