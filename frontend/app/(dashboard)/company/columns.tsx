"use client";

import { ICompanyRead } from "@/app/shared/api";
import { ColumnDef } from "@tanstack/react-table";

export type Company = {
    id: number;
    supplier_id: number;
    name: string;
    phone: string;
}

export const columns: ColumnDef<ICompanyRead>[] = [
   {
    accessorKey: "supplier_id",
    header: "Supplier ID"
   },
   {
    accessorKey: "name",
    header: "Name"
   },
   {
    accessorKey: "phone",
    header: "Phone"
   }
   
]