import React from "react";

interface LeadFormProps {
    name: string;
    description: string;
    onNameChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onDescriptionChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onSubmit: (e: React.FormEvent) => void;
}
function LeadForm({name, description, onNameChange, onDescriptionChange, onSubmit}: LeadFormProps) {
    return (
        <form onSubmit={onSubmit}>
        <div className="mb-3">
            <label htmlFor="name" className="form-label">Name</label>
            <input 
            type="text" 
            className="form-control" 
            id="name"
            value={name}
            onChange={onNameChange}
            required
            />
        </div>
        <div className="mb-3">
            <label htmlFor="description" className="form-label">Description</label>
            <input 
            type="text" 
            className="form-control" 
            id="description"
            value={description}
            onChange={onDescriptionChange}
            required
            />
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
        </form>

    )
}

export default LeadForm; 