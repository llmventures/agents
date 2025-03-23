interface PaperFormProps {
    file: File | null;
    onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onSubmit: (e: React.FormEvent) => void;
}


function PaperForm({onFileChange, onSubmit}: PaperFormProps) {
    return (
        <form onSubmit={onSubmit}>
        
        <div className="mb-3">
            <label htmlFor="file" className="form-label">Upload your paper's file as a pdf.</label>
            <input 
            className="form-control" 
            type="file" 
            id="formFile" 
            onChange={onFileChange}
            />
        </div>

        <button type="submit" className="btn btn-primary">Submit</button>
        </form>

        


    )
}

export default PaperForm; 