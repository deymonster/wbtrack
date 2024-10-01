import type { Metadata } from "next";
import { Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";

import { cn } from "@/lib/utils";
// import { ThemeProvider } from "@/components/theme-provider";
import { AppWrapper } from "./context/index";
import { ToastContainer } from 'react-toastify';
import dynamic from 'next/dynamic';

const ThemeProvider = dynamic(
  () => import('@/components/theme-provider').then((mod) => mod.ThemeProvider), 
  { ssr: false }
);


const fontSans = Plus_Jakarta_Sans(
  { subsets: ["cyrillic-ext", "latin"],
    weight: ["400", "500", "600", "700"],
    variable: "--font-sans",
  }
);


export const metadata: Metadata = {
  title: "App",
  description: "Web UI for WB Track",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    
    <html lang="en">
      <body
        className={cn('min-h-screen font-sans antialiased', fontSans.variable)}
      >
        <ThemeProvider attribute="class" defaultTheme="dark">
        <AppWrapper>
          {children}
          <ToastContainer />    
        </AppWrapper>
        </ThemeProvider>
        
      </body>
    </html>
    
  );
}
