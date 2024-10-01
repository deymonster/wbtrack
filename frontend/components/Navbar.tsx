"use client";

import React from 'react';
import { Search, Bell, CircleUser } from 'lucide-react';
import { Input } from "@/components/ui/input";
import { DropdownMenu, DropdownMenuContent, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { AuthDialog } from './modals/AuthDialog';
import { useState } from "react";

const Navbar = () => {

  const [isAuthDialogOpen, setIsDialogOpen] = useState(false);

  const handleAuthDialogOpen = () => setIsDialogOpen(true);
  const handleAuthDialogClose = () => setIsDialogOpen(false);

  return (
    <header className="flex h-14 items-center gap-4 border-b bg-muted/40 px-4 lg:h-[60px] lg:px-6">
      <form className="w-full flex-1">
        <div className="relative">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input type="search" placeholder="Search products..." className="w-full appearance-none bg-background pl-8 shadow-none md:w-2/3 lg:w-1/3" />
        </div>
      </form>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <button className="rounded-full">
            <CircleUser className="h-5 w-5" />
            <span className="sr-only">Toggle user menu</span>
          </button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <div>My Account</div>
          <div>Settings</div>
          <div>Logout</div>
          <div onClick={handleAuthDialogOpen} className='cursor-pointer'>Auth</div>
        </DropdownMenuContent>
      </DropdownMenu>
      <AuthDialog isOpen={isAuthDialogOpen} onClose={handleAuthDialogClose} />
    </header>
  );
};

export default Navbar;
