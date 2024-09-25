import React, { createContext, useContext, useState,  useEffect } from "react";
import { AuthService } from "../shared/api";

interface AuthContextType {
    handleLogin: (username: string, password: string) => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);


export const AuthProvider = ({ children }) =>{
    const [user, setUser] = useState(null);


    const handleLogin = async (username, password) =>{
        try{
            const {access_token, refresh_token} = await AuthService.loginApiV1AuthLoginPost({formData: {username, password}});
            localStorage.setItem("access_token", access_token);
            localStorage.setItem("refresh_token", refresh_token);
            console.log("Login response:", access_token, refresh_token);
        } catch (error) {
            console.error('Error login', error);
        }
    };

    return (
        <AuthContext.Provider value={{ handleLogin }}>
        {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}