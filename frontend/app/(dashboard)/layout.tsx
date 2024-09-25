import MainContent from "@/components/MainContent";
import Menu from "@/components/Menu";
import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";

import { ThemeProvider } from "@/components/theme-provider";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ThemeProvider attribute="class" defaultTheme="light">
      <div className="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[280px_1fr]">
        <Sidebar />
        <div className="flex flex-col">
          <Navbar />
          <MainContent>{children}</MainContent>
        </div>
      </div>
    </ThemeProvider>
  );
}
