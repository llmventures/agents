import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import api from './api'
type OptionType = {
    value: string;
    label: string;
  }

type MultiSelectPapersProps = {
    passNamesToParent: (selectedNames: string[]) => void;
}

const MultiselectPapers: React.FC<MultiSelectPapersProps> =({passNamesToParent}) => {
    const [papersOptions, setOptions] = useState<OptionType[] | undefined>([])//Store options for multiselect
    
    const handleSelectPapersChange = (selectedFiles: readonly OptionType[] | null) => {
        const namesList = selectedFiles ? selectedFiles.map(file => file.value): [];
        passNamesToParent(namesList)
        

        
    }
    useEffect(() => {
        const getPapers = async() => {
            try {
                const response = await api.get('/papers/')
                const options = response.data.map((cur_paper : any) => ({
                    value: cur_paper.name,
                    label: cur_paper.name,
                }));
                setOptions(options)
            }
            catch (error:any) {
                console.log('Error fetching papers', error.response)
            }
        }
        getPapers()
    },[]);

    return (
        <div className="select">
            <label htmlFor="method" className="form-label">Choose from existing papers:</label>
            <Select 
            isMulti
            className="basic-multi-select"
            classNamePrefix="select"
            onChange={handleSelectPapersChange}
            options = {papersOptions}
            />
        </div>
    )
}

export default MultiselectPapers;