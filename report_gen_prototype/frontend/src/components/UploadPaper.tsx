import axios from "axios";

function UploadPapers(paper: File): string {
    axios({
        url: "http://localhost:8000/api/papers/",
        method: "POST",
        headers: {
            authorization: "placer auth"
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
        return ("Error:" + Error.response.data.error);
        

    })
    return "axios didn't catch";
}

export default UploadPapers;