import {useState} from "react"
import axios from "axios";
import { useNavigate } from 'react-router-dom';


function Login () {
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false)
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    })
    const handleChange = (e:any) => {
        setFormData({
            ...formData,
            [e.target.name]:e.target.value
        })
    }
    const handleAxiosError = (error:any) => {
        //check if network error
        if (error.message === "Network Error") {
            setError("Network error: backend is down.")
        }
        else if (error.response && error.response.data) {
            const firstErrorField:any = Object.keys(error.response.data)[0];
            const firstError:any = Object.values(error.response.data).flat()[0]; 
            setError(firstErrorField + ":" + firstError)
          } 
        else {
            setError("Unknown error")
        }
    }
    const handleNav = () => {
        navigate('/register');
    }
    const handleSubmit = async (e:any) => {
      e.preventDefault();
          if(isLoading){
              return
          }
    
          setIsLoading(true);
          setError(null);
          try{
                console.log(formData)
                const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/api/login/`, formData)
                console.log("Success!", response.data)
                localStorage.setItem("accessToken", response.data.tokens.access);
                localStorage.setItem("refreshToken", response.data.tokens.refresh)
                const decoded = JSON.parse(atob(response.data.tokens.access.split('.')[1])); // Decode JWT payload
                const expirationTime = decoded.exp * 1000; // Convert from seconds to milliseconds
                localStorage.setItem('tokenExpiration', String(expirationTime)); // Store expiration time

                navigate('/');
                window.location.reload();
              
          }
          catch(error){
            console.log("error catching")
            handleAxiosError(error)
            console.error(error)
          }
          finally{
              setIsLoading(false)
          }
    
    };
    
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
            <h2>Login</h2>
            <form>
                
                <input type="text" name = "email" value={formData.email} onChange={handleChange}></input>
                <br/>            
                <label>password:</label><br/>
                <input type="password" name = "password" value={formData.password} onChange={handleChange}></input>
                <br/>
                <div>
                    <button type="submit" disabled={isLoading} onClick={handleSubmit}>Login</button>
                    <button onClick={handleNav} style={{ color: 'blue', background: 'none', border: 'none' }}>Register</button>
                </div>
            </form>
        </div>
    )
}

export default Login;