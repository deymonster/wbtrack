"use client";

import { useEffect, useState } from "react";
import getCpuTemperature from "@/app/shared/prometheus_api/getCpuTemperature";



const CpuTemperatureFetcher = () => {
    const [ temperatureData, setTemperatureData ] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(()=>{
        const fetchData = async () => {
            try {
                
                setError(null);
                console.log("Begin Fetching temperature data...");
                const data = await getCpuTemperature()
                if (data && data.length > 0) {
                    const tempValue = parseFloat(data[0].value[1]);
                    setTemperatureData((prev) => (prev !== tempValue ? tempValue : prev)); 
                    console.log("Temperature data fetched successfully:", tempValue);
                } else {
                    setError("No temperature data found.");
                }
                
            } catch (error) {
                setError("An error occurred while fetching temperature data.");
                console.log(error)
            } 
        };
        fetchData();
        const interval = setInterval(() => {
            fetchData();
        }, 5000);

        return () => clearInterval(interval);
    }, []);


    return (
        <div className="relative h-[50px]">
            <h2>CPU Temp</h2>
            {loading && <p>Loading...</p>}
            {error && <p className="text-red-500">{error}</p>}
            {temperatureData !== null && (
                <p 
                className={`transition-opacity transform duration-500 ${
                    loading ? 'opacity-0 translate-y-[-10px]': 'opacity-100 translate-y-0'
                }`}
                
                
                >Current CPU Temperature: {temperatureData}</p>
            )}
            
        </div>
    )
    
}

export default CpuTemperatureFetcher;