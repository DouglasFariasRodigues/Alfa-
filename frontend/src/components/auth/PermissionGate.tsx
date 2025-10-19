import { ReactNode } from 'react';
import { usePermissions } from '@/hooks/usePermissions';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Shield, Lock } from 'lucide-react';

interface PermissionGateProps {
  children: ReactNode;
  permission?: string;
  module?: string;
  fallback?: ReactNode;
  requireAdmin?: boolean;
  requireMember?: boolean;
}

export const PermissionGate = ({
  children,
  permission,
  module,
  fallback,
  requireAdmin = false,
  requireMember = false
}: PermissionGateProps) => {
  const { hasPermission, canAccess, isAdmin, isMember, isLoading, user } = usePermissions();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Verificando permissões...</p>
        </div>
      </div>
    );
  }

  // Verificar se é admin quando necessário
  if (requireAdmin && !isAdmin()) {
    return fallback || (
      <Card className="border-amber-200 bg-amber-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-amber-800">
            <Shield className="h-5 w-5" />
            Acesso Restrito
          </CardTitle>
          <CardDescription className="text-amber-700">
            Apenas administradores podem acessar esta funcionalidade.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-amber-600">
            Entre em contato com o administrador do sistema para obter acesso.
          </p>
        </CardContent>
      </Card>
    );
  }

  // Verificar se é membro quando necessário
  if (requireMember && !isMember()) {
    return fallback || (
      <Card className="border-blue-200 bg-blue-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-blue-800">
            <Lock className="h-5 w-5" />
            Acesso de Membro
          </CardTitle>
          <CardDescription className="text-blue-700">
            Esta funcionalidade é exclusiva para membros da igreja.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-blue-600">
            Faça login como membro para acessar esta funcionalidade.
          </p>
        </CardContent>
      </Card>
    );
  }

  // Verificar permissão específica
  if (permission && !hasPermission(permission)) {
    return fallback || (
      <Card className="border-red-200 bg-red-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-red-800">
            <Lock className="h-5 w-5" />
            Sem Permissão
          </CardTitle>
          <CardDescription className="text-red-700">
            Você não tem permissão para acessar esta funcionalidade.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-red-600">
            Seu cargo atual ({user?.cargo?.nome || 'Sem cargo'}) não permite esta ação.
          </p>
        </CardContent>
      </Card>
    );
  }

  // Verificar acesso ao módulo
  if (module && !canAccess(module)) {
    return fallback || (
      <Card className="border-orange-200 bg-orange-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-orange-800">
            <Lock className="h-5 w-5" />
            Módulo Restrito
          </CardTitle>
          <CardDescription className="text-orange-700">
            Você não tem acesso a este módulo.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-orange-600">
            Entre em contato com o administrador para solicitar acesso.
          </p>
        </CardContent>
      </Card>
    );
  }

  // Se passou em todas as verificações, renderizar o conteúdo
  return <>{children}</>;
};
