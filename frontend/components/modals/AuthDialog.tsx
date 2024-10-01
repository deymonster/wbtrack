"use client";

import React from 'react'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog"

import { Button } from "@/components/ui/button"
import { Input } from '../ui/input'
import { useState } from "react";
import { handleApiError } from "@/lib/errorHandler";
import { ApiError, CompanyService } from '@/app/shared/api';



interface AuthDialogProps {
    isOpen: boolean;
    onClose: () => void;
  }

export function AuthDialog({isOpen, onClose}: AuthDialogProps) {
    const [isPhoneInput, setIsPhoneInput] = useState(true);
    const [phone, setPhone] = useState("");
    const [code, setCode] = useState("");
    // const [isOpen, setIsOpen] = useState(true);

    const handlePhoneSubmit = async () => {

        // Send phone via api to wb here
        try {
            // const response = true;
            const response =  await CompanyService.companyRequestCode({
                phone: phone
            });
            if (response.isSuccess) {
                setIsPhoneInput(false);
                console.log("Code sent successfully:", response);
            } else {
                console.log("Code request failed:", response);
            }
            
        } catch (error) {
            console.error('Error submitting phone:', error);
            handleApiError(error as ApiError);
        }
        
        console.log("Phone submitted:", phone);
    }

    const handleCodeSubmit = async () => {
        try{
            console.log("Access code submitted:", code);
            const response = await CompanyService.companyVerifyCode({
                phone: phone,
                code: code
            });
            console.log("Response verify code:", response);
            setIsPhoneInput(true);
            onClose();
        } catch (error) {
            console.error('Error submitting access code:', error);
            handleApiError(error as ApiError);
        }
    }


    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            {/* <DialogTrigger>
                <div className="cursor-pointer">Auth</div>
            </DialogTrigger> */}

            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Authenticate</DialogTitle>
                    <DialogDescription>
                        Please enter your phone number or access code
                    </DialogDescription>
                </DialogHeader>
                <div className='space-y-4'>
                    {/* Поле для ввода номера телефона в зависимости от состояния */}
                    {isPhoneInput ? (
                        <Input
                            id="phone"
                            value={phone}
                            onChange={(e) => setPhone(e.target.value)}
                            placeholder="phone"
                            className="w-full rounded-md"
                            />  
                        ): (
                        <Input
                            id="code"
                            value={code}
                            onChange={(e) => setCode(e.target.value)}
                            placeholder="access code"
                            className="w-full rounded-md"
                        />
                    )}
                    {/* Кнопка отправки номера телефона или кода доступа */}
                    {isPhoneInput ? (
                        <Button className='block w-full rounded-md' onClick={handlePhoneSubmit}>
                            Send Phone
                        </Button>
                    ): (
                        <Button className='block w-full rounded-md' onClick={handleCodeSubmit}>
                            Verify Code
                        </Button>
                    )}
                </div>
                {/* <DialogFooter>
                    <DialogTrigger asChild>
                        <Button type='button'>Close</Button>
                    </DialogTrigger>
                </DialogFooter> */}
            </DialogContent>
        </Dialog>
    )
}
