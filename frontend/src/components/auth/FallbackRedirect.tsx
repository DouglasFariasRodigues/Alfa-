import { useEffect } from 'react';
import { apiClient } from '@/lib/api';

export const FallbackRedirect = () => {
  useEffect(() => {
    const redirectUser = async () => {
      try {
        const user = await apiClient.getCurrentUser();
        
        if (user.is_admin) {
          window.location.href = '/dashboard';
        } else if (user.cargo?.pode_gerenciar_eventos) {
          // Membro com permissão de eventos vai para dashboard administrativo
          window.location.href = '/dashboard';
        } else {
          window.location.href = '/member-dashboard';
        }
      } catch (error) {
        // Em caso de erro, redirecionar para dashboard por padrão
        window.location.href = '/dashboard';
      }
    };

    // Aguardar um pouco antes de redirecionar
    const timer = setTimeout(redirectUser, 1000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center space-y-4">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        <h2 className="text-xl font-semibold">Carregando...</h2>
        <p className="text-gray-600">Preparando sua experiência no sistema.</p>
        <p className="text-sm text-gray-500">Você será redirecionado em breve...</p>
      </div>
    </div>
  );
};
