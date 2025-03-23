import React, { useState, useEffect } from 'react';
import axios from "axios";
import Select from 'react-select';

type OptionType = {
    value: string;
    label: string;
  }

type MultiSelectAgentsProps = {
    passNamesToParent: (selectedNames: string[]) => void;
}

const MultiselectPapers: React.FC<MultiSelectAgentsProps> =({passNamesToParent}) => {
    const [agentOptions, setOptions] = useState<OptionType[] | undefined>([])//Store options for multiselect
    const [selectedAgents, setSelectedAgents] = useState<readonly OptionType[] | null>(null);
    
    const handleSelectAgentsChange = (selectedAgents: readonly OptionType[] | null) => {
        setSelectedAgents(selectedAgents);
        const namesList = selectedAgents ? selectedAgents.map(file => file.value): [];
        passNamesToParent(namesList)
        

        
    }
    useEffect(() => {
        axios({
            url: "http://localhost:8000/api/agents/",
            method: "GET",
            headers: {
                authorization: "placer auth token"
            }
        } )
        .then((response:any) => {
            const options = response.data.map((cur_agent : any) => ({
                value: cur_agent.name,
                label: cur_agent.name,
            }));
            setOptions(options)
        })
        .catch((error:any) => {
            console.log('Error fetching agents', error.response)
        })
    },[]);

    return (
        <div className="select">
            <label htmlFor="method" className="form-label">Choose Potential Agents(or leave empty to allow choosing all) </label>
            <Select 
            isMulti
            className="basic-multi-select"
            classNamePrefix="select"
            onChange={handleSelectAgentsChange}
            options = {agentOptions}
            />
        </div>
    )
}

export default MultiselectPapers;