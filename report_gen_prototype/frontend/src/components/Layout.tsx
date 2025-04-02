import NavBar from "./NavBar";
import { ReactNode } from "react";
import { useState, useEffect } from 'react'
import axios from "axios"
import { useNavigate } from 'react-router-dom';
import { useLocation } from "react-router-dom";
import api from "./api"

interface Props {
    children?: ReactNode
}

export default function Layout({ children, ...props }: Props) {
    const [isLoggedIn, setLoggedIn] = useState<boolean | null>(false)
    const [username, setUsername] = useState("")
    const navigate = useNavigate();
    const handleLogout = async () => {
        try{
          const accessToken = localStorage.getItem("accessToken");
          const refreshToken = localStorage.getItem("refreshToken");
    
          if(accessToken && refreshToken) {
            
            await api.post(`/logout/`, {"refresh":refreshToken})
            localStorage.removeItem("accessToken");
            localStorage.removeItem("refreshToken");
            setLoggedIn(false);
            setUsername("");
            console.log("Log out successful!")
            navigate("/login")
          }
        }
        catch(error:any){
          console.error("Failed to logout", error.response?.data || error.message)
        }
      }
    useEffect (()=>{
        const checkLoggedInUser = async () => {
            try {
                console.log("checking if user is still logged in ")
                const token = localStorage.getItem("accessToken");
                if (!token) {
                    setLoggedIn(false)
                    if (location.pathname !== "/register") {
                        navigate("/login");
                    }
                    return
                }
                
                const response = await api.get("http://localhost:8000/api/user/");
                
                setLoggedIn(true)
                setUsername(response.data.username)
                //navigate("/")
            }
            catch(error) {
                setLoggedIn(false)
                setUsername("")
                if (location.pathname !== "/register") {
                    navigate("/login");
                }

            }
        };
        checkLoggedInUser()
        console.log(username)
    }, [isLoggedIn])

    if (isLoggedIn === null) {
        // While the login check is happening, render a loading state (or nothing)
        return <div>Loading...</div>;
    }
    return (
        <div key = {isLoggedIn ? "loggedIn": "loggedOut"} {...props}>
            {isLoggedIn ? (<NavBar handleLogout={handleLogout}/>) :<></> }
            {children}
        </div>
    )
}