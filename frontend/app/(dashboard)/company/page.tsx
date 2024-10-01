"use client";

import React, { useEffect } from 'react'
import { useState } from 'react';
import { AddCompany } from '@/components/modals/AddCompany';

import { Button } from "@/components/ui/button";
import { DataTable } from '@/components/tables/data-table';
import { Company, columns } from "./columns";
import { CompanyService, IResponsePaginated_ICompanyRead_, ICompanyRead } from '@/app/shared/api';


async function getCompanies(): Promise<IResponsePaginated_ICompanyRead_> {
    try {
      const response = await CompanyService.companyGetList({});
      return response;

    } catch (error) {
      console.error(error);
      throw error;
    }
  
}

export default async function CompanyPage() {
  const [companies, setCompanies] = useState<ICompanyRead[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  

  const handleDialogOpen = () => setIsDialogOpen(true);
  const handleDialogClose = () => setIsDialogOpen(false);

  useEffect(() => {
    async function fetchCompanies() {
      try {
        const data = await getCompanies();
        setCompanies(data.items);
        setIsLoading(false);
      } catch (error) {
        setIsError(true);
        setIsLoading(false);
      }
    }
    fetchCompanies();
  }, []);
  return (
    <section className="py-1">
      <div className='w-full'>
        <div className='flex items-center justify-between py-4'>        
            <h1 className='text-3xl font-bold'>Companies</h1>
              <Button onClick={handleDialogOpen} className='ml-auto'>
                Add Company
              </Button>
        </div>
              <AddCompany isOpen={isDialogOpen} onClose={handleDialogClose} />
            
            {isLoading ? (
              <p>Loading...</p>
            ) : isError ? (
              <p>Error loading companies.</p>
            ) : (
              <DataTable columns={columns} data={companies} />
            )}
        
      </div>
      
    </section>
  )
}



