import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { usePermissions } from "@/hooks/usePermissions";
import { PermissionGate } from "@/components/auth/PermissionGate";
import { Shield, Users, Calendar, DollarSign, FileText, Settings } from "lucide-react";

export default function PermissionTest() {
  const { user, hasPermission, canAccess, isAdmin, isMember, getUserRole } = usePermissions();

  const permissions = [
    { key: 'dizimos', label: 'Registrar Dízimos', icon: DollarSign },
    { key: 'ofertas', label: 'Registrar Ofertas', icon: DollarSign },
    { key: 'membros', label: 'Gerenciar Membros', icon: Users },
    { key: 'eventos', label: 'Gerenciar Eventos', icon: Calendar },
    { key: 'financas', label: 'Gerenciar Finanças', icon: DollarSign },
    { key: 'cargos', label: 'Gerenciar Cargos', icon: Shield },
    { key: 'documentos', label: 'Gerenciar Documentos', icon: FileText },
    { key: 'relatorios', label: 'Visualizar Relatórios', icon: FileText },
  ];

  const modules = [
    { key: 'dashboard', label: 'Dashboard' },
    { key: 'membros', label: 'Membros' },
    { key: 'eventos', label: 'Eventos' },
    { key: 'financas', label: 'Finanças' },
    { key: 'cargos', label: 'Cargos' },
    { key: 'documentos', label: 'Documentos' },
    { key: 'relatorios', label: 'Relatórios' },
  ];

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Teste de Permissões</h1>
        <p className="text-muted-foreground">
          Verificação do sistema de permissões avançado
        </p>
      </div>

      {/* Informações do Usuário */}
      <Card>
        <CardHeader>
          <CardTitle>Informações do Usuário</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <p><strong>Nome:</strong> {user?.nome || 'N/A'}</p>
              <p><strong>Email:</strong> {user?.email || 'N/A'}</p>
              <p><strong>Tipo:</strong> {user?.user_type || 'N/A'}</p>
              <p><strong>É Admin:</strong> {isAdmin() ? 'Sim' : 'Não'}</p>
              <p><strong>É Membro:</strong> {isMember() ? 'Sim' : 'Não'}</p>
              <p><strong>Cargo:</strong> {user?.cargo?.nome || 'Sem cargo'}</p>
            </div>
            <div>
              <p><strong>Role:</strong> {getUserRole()}</p>
              <p><strong>Status:</strong> {user?.status || 'N/A'}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Teste de Permissões Específicas */}
      <Card>
        <CardHeader>
          <CardTitle>Permissões Específicas</CardTitle>
          <CardDescription>
            Verificação de permissões baseadas no cargo
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {permissions.map((permission) => {
              const hasPerm = hasPermission(permission.key);
              const Icon = permission.icon;
              return (
                <div key={permission.key} className="flex items-center gap-3 p-3 border rounded-lg">
                  <Icon className={`h-5 w-5 ${hasPerm ? 'text-green-600' : 'text-red-600'}`} />
                  <div>
                    <p className="font-medium">{permission.label}</p>
                    <p className={`text-sm ${hasPerm ? 'text-green-600' : 'text-red-600'}`}>
                      {hasPerm ? 'Permitido' : 'Negado'}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Teste de Acesso a Módulos */}
      <Card>
        <CardHeader>
          <CardTitle>Acesso a Módulos</CardTitle>
          <CardDescription>
            Verificação de acesso baseado em módulos
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {modules.map((module) => {
              const canAccessModule = canAccess(module.key);
              return (
                <div key={module.key} className="flex items-center gap-3 p-3 border rounded-lg">
                  <div className={`w-3 h-3 rounded-full ${canAccessModule ? 'bg-green-500' : 'bg-red-500'}`} />
                  <div>
                    <p className="font-medium">{module.label}</p>
                    <p className={`text-sm ${canAccessModule ? 'text-green-600' : 'text-red-600'}`}>
                      {canAccessModule ? 'Acesso Permitido' : 'Acesso Negado'}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Teste do PermissionGate */}
      <Card>
        <CardHeader>
          <CardTitle>Teste do PermissionGate</CardTitle>
          <CardDescription>
            Componente de proteção de rotas
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h4 className="font-medium mb-2">Acesso Admin (requireAdmin=true)</h4>
            <PermissionGate requireAdmin={true}>
              <div className="p-4 bg-green-100 border border-green-300 rounded-lg">
                <p className="text-green-800">✅ Você é um administrador!</p>
              </div>
            </PermissionGate>
          </div>

          <div>
            <h4 className="font-medium mb-2">Acesso Membro (requireMember=true)</h4>
            <PermissionGate requireMember={true}>
              <div className="p-4 bg-blue-100 border border-blue-300 rounded-lg">
                <p className="text-blue-800">✅ Você é um membro!</p>
              </div>
            </PermissionGate>
          </div>

          <div>
            <h4 className="font-medium mb-2">Permissão para Gerenciar Eventos</h4>
            <PermissionGate permission="eventos">
              <div className="p-4 bg-green-100 border border-green-300 rounded-lg">
                <p className="text-green-800">✅ Você pode gerenciar eventos!</p>
              </div>
            </PermissionGate>
          </div>

          <div>
            <h4 className="font-medium mb-2">Permissão para Gerenciar Cargos</h4>
            <PermissionGate permission="cargos">
              <div className="p-4 bg-green-100 border border-green-300 rounded-lg">
                <p className="text-green-800">✅ Você pode gerenciar cargos!</p>
              </div>
            </PermissionGate>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
