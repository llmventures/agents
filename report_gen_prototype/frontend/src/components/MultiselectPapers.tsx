import React, { useState, useEffect } from 'react';
import axios from "axios";
import Select from 'react-select';

type OptionType = {
    value: string;
    label: string;
  }

type MultiSelectPapersProps = {
    passNamesToParent: (selectedNames: string[]) => void;
}

const MultiselectPapers: React.FC<MultiSelectPapersProps> =({passNamesToParent}) => {
    const [papersOptions, setOptions] = useState<OptionType[] | undefined>([])//Store options for multiselect
    const [selectedFiles, setSelectedFiles] = useState<readonly OptionType[] | null>(null);
    
    const handleSelectPapersChange = (selectedFiles: readonly OptionType[] | null) => {
        setSelectedFiles(selectedFiles);
        const namesList = selectedFiles ? selectedFiles.map(file => file.value): [];
        passNamesToParent(namesList)
        

        
    }
    useEffect(() => {
        axios({
            url: "http://localhost:8000/api/papers/",
            method: "GET",
            headers: {
                authorization: "placer auth token"
            }
        } )
        .then((response:any) => {
            const options = response.data.map((cur_paper : any) => ({
                value: cur_paper.name,
                label: cur_paper.name,
            }));
            setOptions(options)
        })
        .catch((error:any) => {
            console.log('Error fetching papers', error.response)
        })
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