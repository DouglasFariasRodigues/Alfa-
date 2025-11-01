import { useEffect, useState } from 'react';
import { usePermissions } from '@/hooks/usePermissions';
import { TokenManager } from '@/lib/api';

export const SmartRedirect = () => {
  const { isAdmin, isMember, isLoading, user, error } = usePermissions();
  const [redirectAttempted, setRedirectAttempted] = useState(false);

  useEffect(() => {
    console.log('SmartRedirect - Estado:', { isLoading, user, error, isAdmin: isAdmin(), isMember: isMember(), redirectAttempted });
    
    // Se já tentou redirecionar, não tentar novamente
    if (redirectAttempted) return;

    // Se ainda está carregando, aguardar
    if (isLoading) return;

    // Se há erro ou não conseguiu carregar dados do usuário
    if (error || !user) {
      console.error('Erro ao carregar dados do usuário ou usuário não encontrado:', error);
      setRedirectAttempted(true);
      // Em caso de erro, redirecionar para dashboard por padrão
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 1000);
      return;
    }

    // Marcar que tentou redirecionar
    setRedirectAttempted(true);

    // Redirecionar baseado no tipo de usuário
    if (isAdmin()) {
      console.log('Redirecionando admin para dashboard');
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 1000);
    } else if (isMember()) {
      console.log('Redirecionando membro para eventos');
      setTimeout(() => {
        window.location.href = '/eventos';
      }, 1000);
    } else {
      console.log('Usuário sem tipo definido, redirecionando para dashboard');
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 1000);
    }
  }, [isAdmin, isMember, isLoading, user, error, redirectAttempted]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center space-y-4">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        <h2 className="text-xl font-semibold">Redirecionando...</h2>
        <p className="text-gray-600">Carregando suas informações e direcionando para a página apropriada.</p>
        {error && (
          <p className="text-red-600 text-sm">Erro ao carregar dados. Redirecionando para o dashboard...</p>
        )}
        {isLoading && (
          <p className="text-blue-600 text-sm">Carregando dados do usuário...</p>
        )}
      </div>
    </div>
  );
};
