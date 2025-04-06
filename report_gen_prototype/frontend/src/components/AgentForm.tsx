import MultiselectPapers from './MultiselectPapers';
  
interface AgentFormProps {
    name: string;
    role: string;
    expertise: string
    uploadedFiles : File[]
    onNameChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onRoleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onExpertiseChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onSelectFileChange: (names: string[]) => void;
    onSubmit: (e: React.FormEvent) => void;
}
function LeadForm({name, role, expertise, onNameChange, onRoleChange, onExpertiseChange,onSelectFileChange, onFileChange, onSubmit}: AgentFormProps) {    

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
            <label htmlFor="role" className="form-label">Role</label>
            <input 
            type="text" 
            className="form-control" 
            id="role"
            value={role}
            onChange={onRoleChange}
            required
            />
        </div>
        <div className="mb-3">
            <label htmlFor="expertise" className="form-label">Expertise</label>
            <input 
            type="text" 
            className="form-control" 
            id="expertise"
            value={expertise}
            onChange={onExpertiseChange}
            required
            />
        </div>
        <MultiselectPapers passNamesToParent={onSelectFileChange}/>
        <div className="mb-3">
            <label htmlFor="file" className="form-label">Or Upload new paper's file as a pdf.</label>
            <input 
            className="form-control" 
            type="file" 
            id="formFile" 
            multiple
            onChange={onFileChange}
            />
        </div>
        
        
        <button type="submit" className="btn btn-primary">Submit</button>
        </form>

    )
}

export default LeadForm; 