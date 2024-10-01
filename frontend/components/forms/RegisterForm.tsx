"use client";

import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

import { useAppContext } from "@/app/context";
import { FcUnlock } from "react-icons/fc";
import { AiFillEye, AiFillEyeInvisible } from "react-icons/ai";
import { IUserCreate, AuthService, ApiError } from '@/app/shared/api';
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { RegisterAdminFormValidation } from "@/lib/validation";
import { AdminFormDefaultValues } from "@/constants";
import { handleApiError } from "@/lib/errorHandler";
import { toast } from 'react-toastify';


interface RegisterAdminFormProps {
    onRegistrationSuccess: () => void;
  }


const RegisterAdminForm: React.FC<RegisterAdminFormProps> = ({ onRegistrationSuccess }) => {

  
  const [isPasswordVisible, setIsPasswordVisible] = useState(false);
  const [isConfirmPasswordVisible, setIsConfirmPasswordVisible] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const togglePasswordVisibility = () => {
    setIsPasswordVisible(!isPasswordVisible);
  };

  const toggleConfirmPasswordVisibility = () => {
    setIsConfirmPasswordVisible(!isConfirmPasswordVisible);
  };

  const form = useForm<z.infer<typeof RegisterAdminFormValidation>>({
    resolver: zodResolver(RegisterAdminFormValidation),
    defaultValues: AdminFormDefaultValues
  });

  const { register, handleSubmit, formState: { errors } } = form;

  

  const onSubmit = async (values: z.infer<typeof RegisterAdminFormValidation>) => {
    console.log('Form submitted with values:', values);
    setIsLoading(true);

    try {
        const requestBody: IUserCreate = {
            email: values.email,
            password: values.password,
            first_name: values.first_name,
            middle_name: values.middle_name,
            last_name: values.last_name,
            phone: values.phone
        };
        const response = await AuthService.registerRegisterApiV1AuthRegisterPost({
            requestBody,
        });
        toast.success("Регистрация успешна!");
        onRegistrationSuccess();
    } catch (error) {
        handleApiError(error as ApiError);
        console.error("Error during registration:");
    } finally {
        setIsLoading(false);
    }
  };


  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
    <div className="mb-4">          
        <Label htmlFor="email">Email</Label>
            <Input 
            {...form.register("email")}
            className={`mt-2 mb-4 bg-transparent rounded-full ${errors.email ? 'border-red-500' : 'border-gray-300'}`}
            type="email" 
            id="email"
            placeholder="Email"
        />
        {errors.email && <span className="text-red-500 text-sm flex items-center gap-2 mt-1">{errors.email.message}</span>}
    </div>
    <div className="mb-4">                
        <div className="relative">
            <Input
            {...form.register("password")}
            className={`mt-2 mb-4 bg-transparent rounded-full ${errors.password ? 'border-red-500' : 'border-gray-300'}`}
            type="password" 
            id="password" 
            
            placeholder="Пароль"
        />
        
        </div>
        {errors.password && 
        <span className="text-red-500 text-sm flex items-center gap-2 mt-1">{errors.password.message}</span>}
    </div>
        
    <div className="mb-4">
        
            <Input
            {...form.register("confirmPassword")}
            className={`mt-2 mb-4 bg-transparent rounded-full ${errors.confirmPassword ? 'border-red-500' : 'border-gray-300'}`}
            type="password" 
            id="confirmPassword" 
            
            placeholder="Подтверждение пароля"
        />
        { errors.confirmPassword && <span className="text-red-500 text-sm flex items-center gap-2 mt-1">{errors.confirmPassword.message}</span>}
    </div>
        

        <Label htmlFor="first_name">Имя</Label>
            <Input 
            {...form.register("first_name")}
            className="mt-2 mb-4 bg-transparent rounded-full"
            type="text" 
            id="first_name"
            
            placeholder="Имя"
        />

        <Label htmlFor="first_name">Отчество</Label>
            <Input 
            {...form.register("middle_name")}
            className="mt-2 mb-4 bg-transparent rounded-full"
            type="text" 
            id="middle_name"
            
            placeholder="Отчество"
        />

        <Label htmlFor="last_name">Фамилия</Label>
            <Input 
            {...form.register("last_name")}
            className="mt-2 mb-4 bg-transparent rounded-full"
            type="text" 
            id="last_name"
            
            placeholder="Фамилия"
        />


      
      <Button 
        type="submit" 
        className="flex items-center gap-4 px-12 w-full mt-6 mb-6 bg-indigo-600 rounded-full hover:bg-indigo-700"
        variant="outline"
        >
            <FcUnlock size={26}/>
            Зарегистрироваться
      </Button>
      
    </form>
  )
}

export default RegisterAdminForm