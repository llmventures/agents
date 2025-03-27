import React, {useState} from "react"
import axios from "axios";
import { useNavigate } from 'react-router-dom';


function Register () {
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false)
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password1: "",
        password2: "",
    })
    const handleChange = (e:any) => {
        setFormData({
            ...formData,
            [e.target.name]:e.target.value
        })
    }
    const handleAxiosError = (error:any) => {
        if (error.response && error.response.data) {
            const firstErrorField:any = Object.keys(error.response.data)[0];
            const firstError:any = Object.values(error.response.data).flat()[0]; 
            setError(firstErrorField + ":" + firstError)
          } else {
            setError("Unknown error")
          }
    }
    const handleSubmit = async (e:any) => {
        e.preventDefault();
        if (isLoading) {
            return 
        }
        setIsLoading(true)
        setError(null);
        axios({
            url: "http://localhost:8000/api/register/",
            method: "POST",
            data: formData
        })
        .then(response => {
            console.log('New user registered:', response.data) 
        })
        .catch((Error) => {
            console.log("error catching")
            handleAxiosError(Error)
            console.error(Error)
        })
        setIsLoading(false)
        navigate("/login")

    }
    return (
        <div>
            {error && (
                <div className="alert alert-danger alert-dismissible fade show" role="alert">
                {error}
                <button
                    type="button"
                    className="btn-close"
                    data-bs-dismiss="alert"
                    aria-label="Close"
                    onClick={() => setError(null)}
                ></button>
                </div>
            )}
            <h2>Register</h2>
            <form>
                <label>username:</label><br/>
                <input type="text" name = "username" value={formData.username} onChange={handleChange}>
                </input>
                <br/>
                <label>email:</label><br/>
                <input type="text" name = "email" value={formData.email} onChange={handleChange}></input>
                <br/>
                <label>password:</label><br/>
                <input type="password" name = "password1" value={formData.password1} onChange={handleChange}></input>
                <br/>
                <label>confirm password:</label><br/>
                <input type="password" name = "password2" value={formData.password2} onChange={handleChange}></input>
                <br/>
                <button type="submit" disabled={isLoading} onClick={handleSubmit}>Register</button>
            </form>
        </div>
    )
}

export default Register;