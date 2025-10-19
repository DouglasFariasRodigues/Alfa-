import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';

export interface EventComment {
  id: number;
  evento: number;
  membro: number;
  membro_nome: string;
  comentario: string;
  data_comentario: string;
  aprovado: boolean;
}

export interface EventCommentCreate {
  evento: number;
  membro: number;
  comentario: string;
}

// Hook para buscar comentários de um evento
export const useEventComments = (eventoId?: number) => {
  return useQuery({
    queryKey: ['eventComments', eventoId],
    queryFn: () => apiClient.getEventComments(eventoId),
    enabled: !!eventoId, // Only fetch if eventoId is available
  });
};

// Hook para criar comentário em um evento
export const useCreateEventComment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: EventCommentCreate) => apiClient.createEventComment(data),
    onSuccess: (_, variables) => {
      // Invalidate comments for the specific event
      queryClient.invalidateQueries({ queryKey: ['eventComments', variables.evento] });
      // Also invalidate the event details to update comment count
      queryClient.invalidateQueries({ queryKey: ['evento', variables.evento] });
    },
  });
};

// Hook para deletar comentário
export const useDeleteEventComment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (commentId: number) => apiClient.deleteEventComment(commentId),
    onSuccess: () => {
      // Invalidate all event comments queries
      queryClient.invalidateQueries({ queryKey: ['eventComments'] });
    },
  });
};
