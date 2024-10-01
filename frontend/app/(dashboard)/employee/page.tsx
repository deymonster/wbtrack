
"use client";


import React, { useEffect } from 'react'
import { useState } from 'react';
import { AddCompany } from '@/components/modals/AddCompany';

import { Button } from "@/components/ui/button";
import { DataTable } from '@/components/tables/data-table';
import { columns } from "./columns";
import { EmployeeService, IResponsePaginated_IEmployeeRead_, IEmployeeRead } from '@/app/shared/api';


async function getEmployees(limit: number, offset: number): Promise<IResponsePaginated_IEmployeeRead_> {
  try {
    const response = await EmployeeService.employeeGetList({
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
  


  useEffect(() => {
    async function fetchEmployees() {
      setIsLoading(true);
      try {
        const data = await getEmployees(pageSize, page * pageSize);
        setEmployees(data.items);
        setTotalCount(data.total || 0);
        setIsLoading(false);
      } catch (error) {
        setIsError(true);
        setIsLoading(false);
      }
    }
    fetchEmployees();
  }, [page, pageSize]);

  return (
    <section className="py-1">
      <div className='px-1'>
        
        
        <h1 className='text-3xl font-bold mb-6'>Employees</h1>
        
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

