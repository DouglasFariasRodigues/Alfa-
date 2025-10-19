import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient, TokenManager, LoginRequest, LoginResponse } from '@/lib/api';

// Hook para verificar se o usuário está autenticado
export const useAuth = () => {
  const isAuthenticated = TokenManager.isAuthenticated();
  const accessToken = TokenManager.getAccessToken();
  
  return {
    isAuthenticated,
    accessToken,
    logout: () => {
      TokenManager.clearTokens();
      window.location.href = '/';
    }
  };
};

// Hook para login de admin
export const useLogin = () => {
  const queryClient = useQueryClient();

  return useMutation<LoginResponse, Error, LoginRequest>({
    mutationFn: (credentials) => apiClient.login(credentials),
    onSuccess: (data) => {
      if (data.success) {
        // Invalidar queries relacionadas ao usuário
        queryClient.invalidateQueries({ queryKey: ['user'] });
      }
    },
    onError: (error) => {
      console.error('Login failed:', error);
    }
  });
};

// Hook para login de membro
export const useLoginMembro = () => {
  const queryClient = useQueryClient();

  return useMutation<any, Error, { email: string; senha: string }>({
    mutationFn: (credentials) => apiClient.loginMembro(credentials),
    onSuccess: (data) => {
      if (data.success) {
        // Invalidar queries relacionadas ao usuário
        queryClient.invalidateQueries({ queryKey: ['user'] });
      }
    },
    onError: (error) => {
      console.error('Login de membro failed:', error);
    }
  });
};

// Hook para logout
export const useLogout = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => apiClient.logout(),
    onSuccess: () => {
      // Limpar todas as queries
      queryClient.clear();
      // Redirecionar para a página inicial
      window.location.href = '/';
    }
  });
};
