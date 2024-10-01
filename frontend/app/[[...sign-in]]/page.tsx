"use client";

import Image from "next/image"
import Link from "next/link"
import React, { useState } from 'react';
import { useContext, useEffect } from "react";
import { useAppContext } from "../context";
import { useRouter } from "next/navigation";
import Spinner from "@/components/Spinner";
import LoginForm from "@/components/forms/LoginForm";
import RegisterAdminForm from "@/components/forms/RegisterForm";



const LoginPage = () => {
  
  const { login, isAuthenticated } = useAppContext();
  const [loading, setLoading] = useState(false); 
  const [isRegister, setIsRegister] = useState(false);

  const router = useRouter();

 
 
  useEffect(() => {
    if (isAuthenticated) {
      setLoading(true);
      const timeoutId = setTimeout(()=>{
        router.push("/panel");
      }, 200);

      return () => clearTimeout(timeoutId);
    }
  }, [isAuthenticated, router]);
        


  return (

      <main className="bg-[#26313c] h-screen flex  items-center justify-center p-10 ">
        
        <div className="grid box-animate w-full h-full grid-cols-1 bg-white md:grid-cols-2">
          <div className="bg-[#16202a] text-white flex items-center justify-center flex-col">
              <div className="my-4">

                  <h1 className="text-3xl font-semibold ">
                    { isRegister ? 'Регистрация' : 'Вход в личный кабинет '}
                    {/* Вход в личный кабинет */}
                  </h1>
                  
                  <p className="mt-2 text-xs text-slate-400">
                    { isRegister ? 'Введите данные для регистрации' : 'Введите данные для входа' }
                    {/* {' '}
                    Введите данные для входа */}
                  </p>
              </div>

              { loading ? (
                <div className="flex items-center h-full">
                  <Spinner />
                </div>
              ) : isRegister ? (
                  <RegisterAdminForm onRegistrationSuccess={() => setIsRegister(false)}/>
              ) : (
                  <LoginForm />
              )}
              
              <p className="mt-4 text-xs text-slate-200">
                {isRegister ? (
                  <>
                   Зарегистрированы? {" "}
                   <span 
                    onClick={() => setIsRegister(false)}
                    className="underline ml-2 cursor-pointer"
                   >Войти</span>
                  </>
                ): (
                  <>
                  Нет аккаунта? {" "}
                  <span
                    onClick={() => setIsRegister(true)}
                    className="underline ml-2 cursor-pointer"
                  >Регистрация</span>
                  </>
                )}
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