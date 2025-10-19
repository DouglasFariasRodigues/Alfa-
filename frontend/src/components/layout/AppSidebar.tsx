import { 
  Home, 
  Users, 
  Calendar, 
  DollarSign, 
  FileText, 
  Settings,
  Shield
} from "lucide-react";
import { NavLink, useLocation } from "react-router-dom";
import { usePermissions } from "@/hooks/usePermissions";
import logoAlfa from "@/assets/logo_alfa.png";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  useSidebar,
} from "@/components/ui/sidebar";

const mainItems = [
  { title: "Dashboard", url: "/dashboard", icon: Home, permission: null }, // Sempre visível para admins
  { title: "Minha Área", url: "/member-dashboard", icon: Home, permission: null }, // Para membros
  { title: "Membros", url: "/membros", icon: Users, permission: "membros" },
  { title: "Eventos", url: "/eventos", icon: Calendar, permission: "eventos" },
  { title: "Finanças", url: "/financas", icon: DollarSign, permission: "financas" },
];

const otherItems = [
  { title: "Cargos", url: "/cargos", icon: Shield, permission: "cargos" },
  { title: "Documentos", url: "/documentos", icon: FileText, permission: "documentos" },
  { title: "Configurações", url: "/configuracoes", icon: Settings, permission: null }, // Sempre visível
];

export function AppSidebar() {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  const location = useLocation();
  const currentPath = location.pathname;
  const { canAccess, isAdmin, isMember, user } = usePermissions();


  const isActive = (path: string) => {
    if (path === "/dashboard") return currentPath === "/dashboard";
    return currentPath.startsWith(path);
  };

  const getNavClass = (path: string) => {
    const baseClass = "w-full justify-start transition-smooth";
    return isActive(path) 
      ? `${baseClass} bg-primary text-primary-foreground shadow-sm`
      : `${baseClass} hover:bg-accent hover:text-accent-foreground`;
  };

  // Filtrar itens baseado em permissões
  const filteredMainItems = mainItems.filter(item => {
    // Dashboard sempre visível para admins
    if (item.url === '/dashboard') {
      return isAdmin();
    }
    // Minha Área sempre visível para membros
    if (item.url === '/member-dashboard') {
      return isMember();
    }
    // Para outros itens, verificar permissões
    return !item.permission || canAccess(item.permission) || isAdmin();
  });

  const filteredOtherItems = otherItems.filter(item => 
    !item.permission || canAccess(item.permission) || isAdmin()
  );

  return (
    <Sidebar className={collapsed ? "w-16" : "w-64"}>
      <SidebarHeader className="p-4 border-b">
        <div className="flex items-center gap-3">
          <img 
            src={logoAlfa} 
            alt="ALFA +" 
            className="h-8 w-8 object-contain"
          />
          {!collapsed && (
            <div>
              <h2 className="font-semibold text-sm">ALFA +</h2>
              <p className="text-xs text-muted-foreground">Sistema de Gestão</p>
            </div>
          )}
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Principal</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {filteredMainItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <NavLink 
                      to={item.url} 
                      className={getNavClass(item.url)}
                    >
                      <item.icon className="h-4 w-4" />
                      {!collapsed && <span>{item.title}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Outros</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {filteredOtherItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <NavLink 
                      to={item.url}
                      className={getNavClass(item.url)}
                    >
                      <item.icon className="h-4 w-4" />
                      {!collapsed && <span>{item.title}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}