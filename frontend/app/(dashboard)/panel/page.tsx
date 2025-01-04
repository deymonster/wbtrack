import React from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import { CpuIcon, CircuitBoard, MemoryStick, HardDriveIcon } from 'lucide-react';
import Image from 'next/image';

import CpuTemperatureFetcher from '@/components/monitoring/cputempFetcher'

const PanelPage = () => {
  return (
    <div>
      <h1>Panel Page</h1>
        <Card className='w-[380px]'>
      <CardHeader>
        <CardTitle>Computer</CardTitle>
        <CardDescription>UUID 1234</CardDescription>
      </CardHeader>
      <CardContent>
        {/* Fan */}
        <div className="flex items-center justify-center mb-4">
                
              <div className="flex items-center justify-center mb-4">
                <Image
                src="/assets/svg/fan-icon.svg"
                alt="fan"
                className="spin"
                width={200}
                height={200}
                />
              </div>
        </div>
        <div className="flex justify-between">
          Specs
        </div>
        
      </CardContent>
      
    </Card>
    <CpuTemperatureFetcher/>
    </div>

    
  )
}

export default PanelPage