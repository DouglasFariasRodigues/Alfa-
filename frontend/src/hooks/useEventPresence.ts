import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';

export interface EventPresence {
  id: number;
  evento: number;
  membro: number;
  confirmado: boolean;
  data_confirmacao: string;
  observacoes?: string;
}

export interface EventPresenceCreate {
  evento: number;
  membro: number;
  confirmado: boolean;
  observacoes?: string;
}

// Hook para buscar confirmações de presença de um membro
export const useEventPresences = (membroId?: number) => {
  return useQuery({
    queryKey: ['event-presences', membroId],
    queryFn: () => apiClient.getEventPresences(membroId),
    enabled: !!membroId,
  });
};

// Hook para confirmar presença em um evento
export const useConfirmPresence = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: EventPresenceCreate) => apiClient.confirmEventPresence(data),
    onSuccess: () => {
      // Invalidar queries relacionadas
      queryClient.invalidateQueries({ queryKey: ['event-presences'] });
      queryClient.invalidateQueries({ queryKey: ['eventos'] });
    },
  });
};

// Hook para cancelar confirmação de presença
export const useCancelPresence = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (presenceId: number) => apiClient.cancelEventPresence(presenceId),
    onSuccess: () => {
      // Invalidar queries relacionadas
      queryClient.invalidateQueries({ queryKey: ['event-presences'] });
      queryClient.invalidateQueries({ queryKey: ['eventos'] });
    },
  });
};
