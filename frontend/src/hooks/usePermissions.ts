import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';

export interface UserPermissions {
  id: number;
  nome: string;
  email: string;
  cargo?: {
    id: number;
    nome: string;
    pode_registrar_dizimos: boolean;
    pode_registrar_ofertas: boolean;
    pode_gerenciar_membros: boolean;
    pode_gerenciar_eventos: boolean;
    pode_gerenciar_financas: boolean;
    pode_gerenciar_cargos: boolean;
    pode_gerenciar_documentos: boolean;
    pode_visualizar_relatorios: boolean;
  };
  is_admin: boolean;
  user_type: 'admin' | 'membro';
  status?: string;
}

export const usePermissions = () => {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user'],
    queryFn: () => apiClient.getCurrentUser(),
    enabled: true, // Sempre habilitar a query
    staleTime: 5 * 60 * 1000, // 5 minutos
    retry: 1, // Tentar apenas 1 vez em caso de erro
  });

  const hasPermission = (permission: string): boolean => {
    if (!user) return false;
    
    // Admin tem todas as permissões
    if (user.is_admin) return true;
    
    // Se não tem cargo, não tem permissões
    if (!user.cargo) return false;
    
    // Verificar permissão específica
    switch (permission) {
      case 'dizimos':
        return user.cargo.pode_registrar_dizimos;
      case 'ofertas':
        return user.cargo.pode_registrar_ofertas;
      case 'membros':
        return user.cargo.pode_gerenciar_membros;
      case 'eventos':
        return user.cargo.pode_gerenciar_eventos;
      case 'financas':
        return user.cargo.pode_gerenciar_financas;
      case 'cargos':
        return user.cargo.pode_gerenciar_cargos;
      case 'documentos':
        return user.cargo.pode_gerenciar_documentos;
      case 'relatorios':
        return user.cargo.pode_visualizar_relatorios;
      default:
        return false;
    }
  };

  const canAccess = (module: string): boolean => {
    if (!user) return false;
    
    // Admin pode acessar tudo
    if (user.is_admin) return true;
    
    // Para membros, verificar se podem visualizar (não gerenciar)
    switch (module) {
      case 'dashboard':
        return false; // Membros não veem dashboard
      case 'membros':
        return user.cargo?.pode_gerenciar_membros || false;
      case 'eventos':
        return true; // Todos os membros podem acessar eventos (mas com interfaces diferentes)
      case 'financas':
        return true; // Todos os membros podem visualizar finanças
      case 'cargos':
        return user.cargo?.pode_gerenciar_cargos || false;
      case 'documentos':
        return user.cargo?.pode_gerenciar_documentos || false;
      case 'relatorios':
        return user.cargo?.pode_visualizar_relatorios || false;
      default:
        return false;
    }
  };

  const isAdmin = (): boolean => {
    return user?.is_admin || false;
  };

  const isMember = (): boolean => {
    return user && user.user_type === 'membro';
  };

  const getUserRole = (): string => {
    if (!user) return 'guest';
    if (user.is_admin) return 'admin';
    if (user.cargo) return user.cargo.nome;
    return 'member';
  };

  return {
    user,
    isLoading,
    error,
    hasPermission,
    canAccess,
    isAdmin,
    isMember,
    getUserRole
  };
};
