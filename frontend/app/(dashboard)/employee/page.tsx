
"use client";


import React, { useEffect } from 'react'
import { useState } from 'react';
import { AddCompany } from '@/components/modals/AddCompany';

import { Button } from "@/components/ui/button";
import { DataTable } from '@/components/tables/data-table';
import { columns } from "./columns";
import { EmployeeService, IResponsePaginated_IEmployeeRead_, IEmployeeRead } from '@/app/shared/api';
import { set } from 'react-hook-form';
import { EmployeeSearchForm } from '@/components/forms/EmployeeSearchForm';


async function getEmployees(limit: number, 
                            offset: number, 
                            searchParams?: { searchField: string, searchValue: string }): Promise<IResponsePaginated_IEmployeeRead_> {
  try {
    const response = await EmployeeService.employeeSearchEmployees({
      requestBody: {
        search_field: searchParams?.searchField || '',
        search_value: searchParams?.searchValue || '',
      },
      limit,
      offset,
    });
    return response;

  } catch (error) {
    console.error(error);
    throw error;
  }

}

export default async function EmployeePage() {
  const [employees, setEmployees] = useState<IEmployeeRead[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(50);
  const [totalCount, setTotalCount] = useState(0);
  const [searchParams, setSearchParams] = useState<{ searchField: string, searchValue: string }| null>(null);
  


  useEffect(() => {
    async function fetchEmployees() {
      setIsLoading(true);
      try {
        const data = await getEmployees(pageSize, page * pageSize, searchParams || undefined);
        setEmployees(data.items);
        setTotalCount(data.total || 0);
        setIsLoading(false);
      } catch (error) {
        setIsError(true);
        setIsLoading(false);
      }
    }
    fetchEmployees();
  }, [page, pageSize, searchParams]);

  const handleSearch = ( params: { searchField: string,searchValue:string }) => {
    setPage(0);
    setSearchParams(params);
  }

  return (
    <section className="py-1">
      <div className='px-1'>
        
        
        <h1 className='text-3xl font-bold mb-6'>Employees</h1>

        <EmployeeSearchForm onSearch={handleSearch}/>
        
        {isLoading ? (
          <p>Loading...</p>
        ) : isError ? (
          <p>Error loading companies.</p>
        ) : (
          <div>
              <DataTable 
              columns={columns} 
              data={employees}
              page={page} 
              pageSize={pageSize} 
              totalCount={totalCount}
              onPageChange={setPage}
              onPageSizeChange={setPageSize}
              />
          </div>
          
        )}
      </div>
      
    </section>
  )
}

