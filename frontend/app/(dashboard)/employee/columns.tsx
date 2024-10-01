"use client";

import { IEmployeeRead } from "@/app/shared/api";
import { Button } from "@/components/ui/button";
import { 
   DropdownMenu, 
   DropdownMenuContent, 
   DropdownMenuItem, 
   DropdownMenuLabel, 
   DropdownMenuSeparator, 
   DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu";
import { ColumnDef } from "@tanstack/react-table";
import { MoreHorizontal, ArrowUpDown } from "lucide-react"





export const columns: ColumnDef<IEmployeeRead>[] = [
   {
    accessorKey: "employee_id",
    header: ({ column }) =>{
      return (
         <Button
           variant='ghost'
           onClick={()=> column.toggleSorting(column.getIsSorted() === "asc")}
         >
            Employee ID
            <ArrowUpDown className="ml-2 h-4 w-4" />
         </Button>
      )
    }
   },
   {
    accessorKey: "first_name",
    header: ({ column }) =>{
      return (
         <Button
           variant='ghost'
           onClick={()=> column.toggleSorting(column.getIsSorted() === "asc")}
         >
            First Name
            <ArrowUpDown className="ml-2 h-4 w-4" />
         </Button>
      )
    } 
   },
   {
      accessorKey: "middle_name",
      header: ({ column }) =>{
         return (
            <Button
              variant='ghost'
              onClick={()=> column.toggleSorting(column.getIsSorted() === "asc")}
            >
               Middle Name
               <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
         )
       }
   },
   {
      accessorKey: "last_name",
      header: ({ column }) =>{
         return (
            <Button
              variant='ghost'
              onClick={()=> column.toggleSorting(column.getIsSorted() === "asc")}
            >
               Last Name
               <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
         )
       }
   },
   {
    accessorKey: "phones",
    header: ({ column }) =>{
      return (
         <Button
           variant='ghost'
           onClick={()=> column.toggleSorting(column.getIsSorted() === "asc")}
         >
            Phone
            <ArrowUpDown className="ml-2 h-4 w-4" />
         </Button>
      )
    }
   },
   {
      accessorKey: "create_date",
      header: ({ column }) =>{
         return (
            <Button
              variant='ghost'
              onClick={()=> column.toggleSorting(column.getIsSorted() === "asc")}
            >
               Create Date
               <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
         )
       },
      cell: ({row}) => {
         const date = new Date(row.getValue("create_date"))
         const formatted = date.toLocaleDateString("ru-RU")
         return <div className="font-medium">{formatted}</div>
      }
   },
   {
      accessorKey: "rating",
      header: ({ column }) =>{
         return (
            <Button
              variant='ghost'
              onClick={()=> column.toggleSorting(column.getIsSorted() === "asc")}
            >
               Rating
               <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
         )
       }
   },
   {
      accessorKey: "shortages_sum",
      header: ({ column }) =>{
         return (
            <Button
              variant='ghost'
              onClick={()=> column.toggleSorting(column.getIsSorted() === "asc")}
            >
               Shortage Sum
               <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
         )
       }
   },
   // {
   //    accessorKey: "tg_id",
   //    header: "Telegram ID"
   // },

   {
      id: "actions",
      cell: ({ row }) => {
        const employee = row.original
   
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <span className="sr-only">Open menu</span>
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuItem
                onClick={() => navigator.clipboard.writeText(String(employee.employee_id))}
              >
                Copy User ID
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>View customer</DropdownMenuItem>
              <DropdownMenuItem>View payment details</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },

   
]