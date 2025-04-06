import api from './api'

function UploadPapers(paper: File): string {

    const postPaper = async() => {
        try {
            const response = await api.post('/papers', paper)
            console.log('New paper created:', response.data)
            return ("Success: paper added to djangbo backend")
        }
        catch (error:any) {
            console.error(error.response)
            return ("Error uploading paper:" + error.response.data.error);
        }
    }
    postPaper();
    return ""
}

export default UploadPapers;