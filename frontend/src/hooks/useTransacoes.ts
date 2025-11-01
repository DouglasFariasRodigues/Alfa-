import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient, Transacao, TransacaoCreate } from '@/lib/api';

// Hook para buscar transações
export const useTransacoes = (params?: { tipo?: string; categoria?: string }) => {
  return useQuery({
    queryKey: ['transacoes', params],
    queryFn: () => apiClient.getTransacoes(params),
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
};

// Hook para buscar uma transação específica
export const useTransacao = (id: number) => {
  return useQuery({
    queryKey: ['transacao', id],
    queryFn: () => apiClient.getTransacao(id),
    enabled: !!id,
  });
};

// Hook para criar transação
export const useCreateTransacao = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (transacao: TransacaoCreate) => apiClient.createTransacao(transacao),
    onSuccess: () => {
      // Invalidar a lista de transações
      queryClient.invalidateQueries({ queryKey: ['transacoes'] });
    },
  });
};

// Hook para atualizar transação
export const useUpdateTransacao = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, transacao }: { id: number; transacao: Partial<TransacaoCreate> }) =>
      apiClient.updateTransacao(id, transacao),
    onSuccess: (data, variables) => {
      // Invalidar a lista de transações e a transação específica
      queryClient.invalidateQueries({ queryKey: ['transacoes'] });
      queryClient.invalidateQueries({ queryKey: ['transacao', variables.id] });
    },
  });
};

// Hook para deletar transação
export const useDeleteTransacao = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.deleteTransacao(id),
    onSuccess: () => {
      // Invalidar a lista de transações
      queryClient.invalidateQueries({ queryKey: ['transacoes'] });
    },
  });
};
