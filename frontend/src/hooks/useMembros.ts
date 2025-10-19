import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient, Membro, MembroCreate } from '@/lib/api';

// Hook para buscar membros
export const useMembros = (params?: { status?: string; search?: string }) => {
  return useQuery({
    queryKey: ['membros', params],
    queryFn: () => apiClient.getMembros(params),
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
};

// Hook para buscar um membro específico
export const useMembro = (id: number) => {
  return useQuery({
    queryKey: ['membro', id],
    queryFn: () => apiClient.getMembro(id),
    enabled: !!id,
  });
};

// Hook para criar membro
export const useCreateMembro = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (membro: MembroCreate) => apiClient.createMembro(membro),
    onSuccess: () => {
      // Invalidar a lista de membros
      queryClient.invalidateQueries({ queryKey: ['membros'] });
    },
  });
};

// Hook para atualizar membro
export const useUpdateMembro = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, membro }: { id: number; membro: Partial<MembroCreate> }) =>
      apiClient.updateMembro(id, membro),
    onSuccess: (data, variables) => {
      // Invalidar a lista de membros e o membro específico
      queryClient.invalidateQueries({ queryKey: ['membros'] });
      queryClient.invalidateQueries({ queryKey: ['membro', variables.id] });
    },
  });
};

// Hook para deletar membro
export const useDeleteMembro = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.deleteMembro(id),
    onSuccess: () => {
      // Invalidar a lista de membros
      queryClient.invalidateQueries({ queryKey: ['membros'] });
    },
  });
};
