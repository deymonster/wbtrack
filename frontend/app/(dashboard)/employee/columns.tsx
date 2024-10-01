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
import { MoreHorizontal } from "lucide-react"



export const columns: ColumnDef<IEmployeeRead>[] = [
   {
    accessorKey: "employee_id",
    header: "Employee ID"
   },
   {
    accessorKey: "first_name",
    header: "First name"
   },
   {
      accessorKey: "middle_name",
      header: "Middle name"
   },
   {
      accessorKey: "last_name",
      header: "Last name"
   },
   {
    accessorKey: "phones",
    header: "Phone"
   },
   {
      accessorKey: "create_date",
      header: "Create date",
      cell: ({row}) => {
         const date = new Date(row.getValue("create_date"))
         const formatted = date.toLocaleDateString("ru-RU")
         return <div className="font-medium">{formatted}</div>
      }
   },
   {
      accessorKey: "rating",
      header: "Rating"
   },
   {
      accessorKey: "shortages_sum",
      header: "Shortages sum"
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