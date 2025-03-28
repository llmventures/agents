import axios from "axios";

function UploadPapers(paper: File): string {
    const accessToken = localStorage.getItem("accessToken");

    axios({
        url: `${import.meta.env.VITE_BACKEND_URL}/api/papers/`,
        method: "POST",
        headers: {
            "Authorization":`Bearer ${accessToken}`
        },
        data: paper
    })
    .then(response => {
        console.log('New paper created:', response.data)
        return ("Success: paper added to djangbo backend")
        
        //set papers
        
    })
    .catch((Error) => {
        console.error(Error.response)
        return ("Error uploading paper:" + Error.response.data.error);
        

    })
    return "axios didn't catch";
}

export default UploadPapers;