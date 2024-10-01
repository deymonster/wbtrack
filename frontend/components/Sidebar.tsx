import Link from "next/link";
import { Package2, Home, ShoppingCart, Users, LineChart, BriefcaseBusiness, Building } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const Sidebar = () => {
  return (
    <div className="hidden border-r bg-muted/40 md:block">
      <div className="flex h-full max-h-screen flex-col gap-2">
        <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
          <Link href="/" className="flex items-center gap-2 font-semibold">
            <Package2 className="h-6 w-6" />
            <span className="hidden lg:inline">App</span>
          </Link>
        </div>
        <nav className="grid items-start px-2 text-sm font-medium lg:px-4">
          <Link href="/panel" className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
            <Home className="h-4 w-4" />
            <span className="hidden lg:inline">Dashboard</span>
          </Link>
          <Link href="/company" className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
            <BriefcaseBusiness className="h-4 w-4" />
            <span className="hidden lg:inline">Компании</span>
            {/* <Badge className="ml-auto flex h-6 w-6 shrink-0 items-center justify-center rounded-full">6</Badge> */}
          </Link>
          <Link href="/employee" className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
            <Users className="h-4 w-4" />
            <span className="hidden lg:inline">Сотрудники</span>
          </Link>
          {/* <Link href="/office" className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
            <Building className="h-4 w-4" />
            <span className="hidden lg:inline">Офисы</span>
          </Link> */}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
