"use client";

import { createContext, useState, useContext, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AuthService, IUserRead, OpenAPI, UserService } from '../shared/api';



interface AuthContextType {
    accessToken: string | null;
    refreshToken: string | null;
    user: IUserRead | null;
    isAuthenticated: boolean;
    login: (username: string, password: string) => Promise<void>;
    logout: () => void;
    get_user: () => Promise<void>;
}

const defaultAuthContext: AuthContextType = {
    accessToken: null,
    refreshToken: null,
    user: null,
    isAuthenticated: false,
    login: async () => { /* пустая функция по умолчанию */ },
    logout: () => { /* пустая функция по умолчанию */ },
    get_user: async () => { /* пустая функция по умолчанию */ },
};

const AppContext = createContext<AuthContextType>(defaultAuthContext);

export function AppWrapper( {children } : { children: React.ReactNode}) {
    let [name, setName] = useState('Dima')
    const [accessToken, setAccessToken] = useState<string | null>(null);
    const [refreshToken, setRefreshToken] = useState<string | null>(null);
    const [user, setUser] = useState<any>(null);
    const [isAuthenticated, setisAuthenticated] = useState(false);
    const router = useRouter();

    useEffect(()=>{
        const storedAccessToken = localStorage.getItem('access_token');
        const storedRefreshToken = localStorage.getItem('refresh_token');

        if (storedAccessToken && storedRefreshToken) {
            setAccessToken(storedAccessToken);
            setRefreshToken(storedRefreshToken);
            setisAuthenticated(true);
            get_user();
        }  else {
            router.push('/');
        }
    }, []);


    const login = async (username: string, password: string) => {
        try{
            const { access_token, refresh_token } = await AuthService.loginApiV1AuthLoginPost({
                formData: { 
                  username: username,
                  password: password,
                },

            })
            OpenAPI.TOKEN = access_token;
            const userData = await UserService.usersCurrentUserApiV1UserMeGet();
            
            setAccessToken(access_token);
            setRefreshToken(refresh_token);
            setUser(userData);
            setisAuthenticated(true);
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);
            router.push('/admin')

        } catch (error) {
            console.error('Error login', error);
        }
    }

    const logout = () => {
        setAccessToken(null);
        setRefreshToken(null);
        setUser(null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        router.push('/')
    }

    const get_user = async () =>{
        if (accessToken) {
            OpenAPI.TOKEN = accessToken;
            try{
                const userData = await UserService.usersCurrentUserApiV1UserMeGet();
                setUser(userData);
            } catch (error) {
                console.error('Error fetching user data', error);
            }
        } else {
            console.warn('No access token available');
            router.push('/')
        }
        
    }


    return (
        <AppContext.Provider value={{
            accessToken, 
            refreshToken, 
            user, 
            isAuthenticated,
            login,
            logout,
            get_user
        }}>
            {children}
        </AppContext.Provider>

    )
}

export function useAppContext() {
    return useContext(AppContext);
}

