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


interface AddCompanyProps {
    isOpen: boolean;
    onClose: () => void;
  }


export function AddCompany({isOpen, onClose}: AddCompanyProps) {
    
    const [phone, setPhone] = useState("");

    const handlePhoneSubmit = async () => {

        try {
            
            const response =  await CompanyService.companyCreate({
                requestBody: {
                    phone: phone
                }
            });
            if (response.id) {
                console.log("Company created successfully:", response);
                onClose();
                
            } else {
                console.log("Failed to create company, status:", response);
            }
            
        } catch (error) {
            console.error('Error submitting phone:', JSON.stringify(error));
            handleApiError(error as ApiError);
        }
        
        console.log("Phone submitted:", phone);
    }

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                        <DialogTitle>Add Company</DialogTitle>
                        <DialogDescription>
                            Please enter your phone number to add company
                        </DialogDescription>
                    </DialogHeader>
                <div className='space-y-4'>
                <Input
                                id="phone"
                                value={phone}
                                onChange={(e) => setPhone(e.target.value)}
                                placeholder="phone"
                                className="w-full rounded-md"
                                />  
                <Button className='block w-full rounded-md' onClick={handlePhoneSubmit}>
                                Send Phone
                </Button>
                </div>
            </DialogContent>
        </Dialog>
    )
}