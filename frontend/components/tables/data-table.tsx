import React, { useState } from 'react'

import {
  ChevronLeftIcon,
  ChevronRightIcon,
  DoubleArrowLeftIcon,
  DoubleArrowRightIcon,
  
} from "@radix-ui/react-icons"

import {
    ColumnDef,
    flexRender,
    getCoreRowModel,
    useReactTable,
    getPaginationRowModel,
    getSortedRowModel,
    SortingState,
    ColumnFiltersState,
    getFilteredRowModel
} from '@tanstack/react-table';

import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table';

import { Button} from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Input } from '../ui/input';

interface DataTableProps<TData, TValue>{
    columns: ColumnDef<TData, TValue>[]
    data: TData[],
    page: number,
    pageSize: number,
    totalCount: number,
    onPageChange: (page: number) => void,
    onPageSizeChange: (pageSize: number) => void

}

export function DataTable<TData, TValue>({
    columns,
    data,
    page,
    pageSize,
    totalCount,
    onPageChange,
    onPageSizeChange
}: DataTableProps<TData, TValue>){

    const [sorting, setSorting] = useState<SortingState>([])
    // const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
    const [searchField, setSearchField] = useState<string>('')
    const [searchValue, setSearchValue] = useState<string>('')

    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        onSortingChange: setSorting,
        getSortedRowModel: getSortedRowModel(),
        
        manualPagination: true,
        pageCount: Math.ceil(totalCount / pageSize),
        state: {
            pagination: {
              pageIndex: page,
              pageSize: pageSize,
            },
            sorting
        },
        onPaginationChange: (updater) => {
          const newPagination = typeof updater === 'function' ? updater(table.getState().pagination) : updater;
          onPageChange(newPagination.pageIndex);
          onPageSizeChange(newPagination.pageSize);
        }
    });

    const handleSearchChange = async (value: string) => {
      setSearchValue(value);
      try {
          // const result = await UserService.search({ field: searchField, value }); // Вызов метода на сервере
          console.log('Результат поиска:', value);
      } catch (error) {
          console.error('Ошибка поиска:', error);
      }
  }


    return (
    <>
    
     {/* Filter by last name */}
    <div>
      <div className="flex items-center py-4 space-x-4">

        {/* <Input
          placeholder="Filter last name"
          value={(table.getColumn("last_name")?.getFilterValue() as string) ?? ""}
          onChange={(event)=>
            table.getColumn("last_name")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        /> */}

        <Select
          value={searchField}
          onValueChange={(value)=>setSearchField(value)}
        >
          <SelectTrigger className="w-[150px]">
            <SelectValue placeholder="Filter by"/>
          </SelectTrigger>
          <SelectContent side="top">
            <SelectItem value="last_name">Фамилия</SelectItem>
            <SelectItem value="phone">Телефон</SelectItem>
          </SelectContent>
        </Select>

        {/* Input for search value */}
        <Input
          placeholder={
            searchField === "last_name"
            ? "Поиск по фамилии"
            : "Поиск по телефону"
          }
          value={searchValue}
          onChange={(event)=>handleSearchChange(event.target.value)}
          className="max-w-sm"
        />
      </div>
    </div>

    {/* Table */}
    <div className="rounded-md border overflow-x-auto w-full">
      
      <Table className='w-full'>
      <TableCaption>A list of employees.</TableCaption>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return (
                  <TableHead key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </TableHead>
                )
              })}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                data-state={row.getIsSelected() && "selected"}
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center">
                No results.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
        {/* Pagination  */}
        <div className="flex items-center justify-end space-x-2 py-4">
          {/* Rows per page */}
          <div className="flex items-center space-x-2">
          <p className="text-sm font-medium">Кол-во строк</p>
          <Select
             value={`${table.getState().pagination.pageSize}`}
             onValueChange={(value) => {
              onPageSizeChange(Number(value));
             }}
          >
            <SelectTrigger className="h-8 w-[70px]">
              <SelectValue placeholder={table.getState().pagination.pageSize} />
            </SelectTrigger>
            <SelectContent side="top">
              {
                [10, 20, 30, 40, 50].map((pagesize)=>(
                  <SelectItem key={pagesize} value={`${pagesize}`}>
                    {pagesize}
                  </SelectItem>
                ))
              }
            </SelectContent>
          </Select>
          </div>

          {/* Page info*/}
          <div className='flex w-[100px] items-center justify-center text-sm font-medium'>
            Стр. {table.getState().pagination.pageIndex + 1} из {table.getPageCount()}
          </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(0)}
          disabled={page === 0}
        >
          <span className="sr-only">Go to first page</span>
          <DoubleArrowLeftIcon className="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          <span className="sr-only">Go to previous page</span>
          <ChevronLeftIcon className="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          <span className="sr-only">Go to next page</span>
          <ChevronRightIcon className="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => onPageChange(table.getPageCount() - 1)}
          disabled={page >= table.getPageCount() - 1}
        >
          <span className="sr-only">Go to last page</span>
          <DoubleArrowRightIcon className="h-4 w-4" />
        </Button>
        </div>
    </>


    )

}


