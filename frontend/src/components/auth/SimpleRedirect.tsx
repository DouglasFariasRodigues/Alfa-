import { useEffect, useState } from 'react';
import { TokenManager } from '@/lib/api';

export const SimpleRedirect = () => {
  const [isRedirecting, setIsRedirecting] = useState(false);

  useEffect(() => {
    const redirectUser = async () => {
      if (isRedirecting) return;
      
      setIsRedirecting(true);
      
      try {
        // Verificar se há token
        const token = TokenManager.getAccessToken();
        if (!token) {
          console.log('Sem token, redirecionando para login');
          window.location.href = '/login';
          return;
        }

        // Tentar buscar dados do usuário
        const response = await fetch('http://localhost:8000/api/auth/me/', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          console.log('Erro ao buscar dados do usuário, redirecionando para login');
          TokenManager.clearTokens();
          window.location.href = '/login';
          return;
        }

        const userData = await response.json();
        console.log('Dados do usuário obtidos:', userData);

        // Redirecionar baseado no tipo de usuário
        if (userData.is_admin) {
          console.log('Admin detectado, redirecionando para dashboard');
          window.location.href = '/dashboard';
        } else if (userData.user_type === 'membro') {
          console.log('Membro detectado, redirecionando para eventos');
          window.location.href = '/eventos';
        } else {
          console.log('Tipo de usuário não identificado, redirecionando para dashboard');
          window.location.href = '/dashboard';
        }
      } catch (error) {
        console.error('Erro no redirecionamento:', error);
        // Em caso de erro, redirecionar para dashboard
        window.location.href = '/dashboard';
      }
    };

    // Aguardar um pouco antes de redirecionar
    const timer = setTimeout(redirectUser, 500);
    
    return () => clearTimeout(timer);
  }, [isRedirecting]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center space-y-4">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        <h2 className="text-xl font-semibold">Redirecionando...</h2>
        <p className="text-gray-600">Carregando suas informações e direcionando para a página apropriada.</p>
        <p className="text-sm text-gray-500">Aguarde um momento...</p>
      </div>
    </div>
  );
};
