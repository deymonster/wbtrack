"use client";

import { createContext, useState, useContext, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { ApiError, AuthService, IUserRead, OpenAPI, UserService } from '../shared/api';
import Cookies from 'js-cookie';



interface AuthContextType {
    user: IUserRead | null;
    isAuthenticated: boolean;
    login: (username: string, password: string) => Promise<void>;
    logout: () => void;
    get_user: () => Promise<void>;
}

const defaultAuthContext: AuthContextType = {
    
    user: null,
    isAuthenticated: false,
    login: async () => { /* пустая функция по умолчанию */ },
    logout: () => { /* пустая функция по умолчанию */ },
    get_user: async () => { /* пустая функция по умолчанию */ },
};

const AppContext = createContext<AuthContextType>(defaultAuthContext);

export function AppWrapper( {children } : { children: React.ReactNode}) {
    
    
    const [user, setUser] = useState<any>(null);
    const [isAuthenticated, setisAuthenticated] = useState(false);
    const router = useRouter();

    useEffect(()=>{
        const storedAccessToken = Cookies.get('access_token');
        const storedRefreshToken = Cookies.get('refresh_token');

        if (storedRefreshToken) {
            if (!storedAccessToken) {
                refreshToken().then(newAccessToken => {
                    if (newAccessToken) {
                        get_user();
                        router.push('/admin');
                    } else {
                        router.push('/');
                    }
                });
            } else {
                OpenAPI.TOKEN = storedAccessToken;            
                setisAuthenticated(true);
                get_user();
                router.push('/panel');
            }
           

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

            // сохраняем токены в куки
            Cookies.set('access_token', access_token, {
                expires: 7,
                // secure: true,
                sameSite: 'Strict',
                // httpOnly: true
            })

            Cookies.set('refresh_token', refresh_token, {
                expires: 30,
                // secure: true,
                sameSite: 'Strict',
                // httpOnly: true
            })


            OpenAPI.TOKEN = access_token;
            const userData = await UserService.usersCurrentUserApiV1UserMeGet();
            
            setUser(userData);
            setisAuthenticated(true);
            
            router.push('/panel')

        } catch (error) {
            console.error('Error login', error);
        }
    };

    const logout = () => {
        Cookies.remove('access_token');
        Cookies.remove('refresh_token');
        setUser(null);
        setisAuthenticated(false);
        router.push('/')
    };

    const refreshToken = async () => {

        const refreshToken = Cookies.get('refresh_token');
        if (!refreshToken) {
            logout();
            return null;
        }

        try {
            const response = await AuthService.refreshTokenApiV1AuthRefreshTokenPost({
                requestBody: {
                    refresh_token: refreshToken,
                }
            });
            const { access_token } =  response.access_token;
            OpenAPI.TOKEN = access_token;
            Cookies.set('access_token', access_token, {
                expires: 7,
                // secure: true,
                sameSite: 'Strict',
                // httpOnly: true
            })
            return access_token;
        } catch (error) {
            console.error('Error refreshing token', error);
            logout();
            return null;
        
        }
    };

    const get_user = async () =>{


        try{
            const userData = await UserService.usersCurrentUserApiV1UserMeGet();
            setUser(userData);
        } catch (error) {
            {
                console.error('Error fetching user data', error);
                logout();
            }
            
        }
        
    }


    return (
        <AppContext.Provider value={{
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

