"use client";

import Image from "next/image"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import React, { useState } from 'react';
import { FcUnlock } from "react-icons/fc";
import { useContext, useEffect } from "react";
import { useAppContext } from "../context";
import { OpenAPI } from "../shared/api/core/OpenAPI";
import { useRouter } from "next/navigation";
import Spinner from "@/components/Spinner";
import LoginForm from "@/components/forms/LoginForm";


const LoginPage = () => {
  
  const { login, isAuthenticated } = useAppContext();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState(""); 
  const [loading, setLoading] = useState(false); 

  const router = useRouter();
 
  useEffect(() => {
    if (isAuthenticated) {
      setLoading(true);
      const timeoutId = setTimeout(()=>{
        router.push("/admin");
      }, 1000);

      return () => clearTimeout(timeoutId);
    }
  }, [isAuthenticated, router]);

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    await login(username, password);
    setLoading(false);
    
  }
        


  return (

      <main className="bg-[#26313c] h-screen flex  items-center justify-center p-10 ">
        
        <div className="grid box-animate w-full h-full grid-cols-1 bg-white md:grid-cols-2">
          <div className="bg-[#16202a] text-white flex items-center justify-center flex-col">
              <div className="my-4">
                  <h1 className="text-3xl font-semibold ">Вход в личный кабинет</h1>
                  <p className="mt-2 text-xs text-slate-400">
                    {' '}
                    Введите данные для входа</p>
              </div>

              { loading ? (
                <div className="flex items-center h-full">
                  <Spinner />
                </div>
              ) : (
                  <LoginForm/>
              )}
              
              <p className="mt-4 text-xs text-slate-200">
                Нет аккаунта? <Link href="/sign-up" className="underline ml-2">Плоти</Link>
              </p>
          </div>
          <div className="relative hidden md:block">
            <Image 
              className="object-cover" fill={true}
              src="/assets/images/bg.jpg"
              alt="background Image"

            />
          </div>
        </div>
      </main>
    )
  }

export default LoginPage