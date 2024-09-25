import React from 'react'
import { Home, Settings, LogOut, BriefcaseBusiness } from 'lucide-react';
import Link from 'next/link';
import { late } from 'zod';



const menuItems = [
    {
        title: "MENU",
        items: [
            {
                icon: <Home />,
                label: "Home",
                href: "/",
                visible: ["admin", "user"]

            },
            {
                icon: <BriefcaseBusiness />,
                label: "Company",
                href: "/company",
                visible: ["admin", "user"]

            },
            {
                icon: <Settings />,
                label: "Settings",
                href: "/settings",
                visible: ["admin", "user"]
            },
            {
                icon: <LogOut/>,
                label: "Logout",
                href: "/logout",
                visible: ["admin", "user"]
            }
        ]
    }
]

const Menu = () => {
  return (
    <div className='mt-4 text-sm'>
        {menuItems.map(i=>(
            <div className='flex flex-col gap-2' key={i.title}>
                <span className='hidden lg:block text-gray-400 font-light my-4'>{i.title}</span>
                {i.items.map(item=>(
                    <Link 
                    href={item.href} 
                    key={item.label} 
                    className='flex items-center justify-start lg:sjustify-start gap-4 text-gray-500 py-2'>
                        {item.icon}
                        <span className='hidden lg:block'>{item.label}</span>
                    </Link>
                ))}
            </div>
        ))}
    </div>
  )
}

export default Menu