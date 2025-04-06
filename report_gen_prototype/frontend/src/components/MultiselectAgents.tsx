import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import api from './api'
type OptionType = {
    value: string;
    label: string;
  }

type MultiSelectAgentsProps = {
    passNamesToParent: (selectedNames: string[]) => void;
}

const MultiselectPapers: React.FC<MultiSelectAgentsProps> =({passNamesToParent}) => {
    const [agentOptions, setOptions] = useState<OptionType[] | undefined>([])//Store options for multiselect
    
    const handleSelectAgentsChange = (selectedAgents: readonly OptionType[] | null) => {
        const namesList = selectedAgents ? selectedAgents.map(file => file.value): [];
        passNamesToParent(namesList)
        

        
    }
    useEffect(() => {
        const getAgents = async() => {
            try {
                const response = await api.get('/agents/')
                const options = response.data.map((cur_agent : any) => ({
                    value: cur_agent.name,
                    label: cur_agent.name,
                }));
                setOptions(options)
            }
            catch (error:any) {
                console.log('Error fetching agents', error.response)
            }
        }
        getAgents()
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