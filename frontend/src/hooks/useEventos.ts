import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient, Evento, EventoCreate } from '@/lib/api';

// Hook para buscar eventos
export const useEventos = (params?: { search?: string }) => {
  return useQuery({
    queryKey: ['eventos', params],
    queryFn: () => apiClient.getEventos(params),
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
};

// Hook para buscar um evento específico
export const useEvento = (id: number) => {
  return useQuery({
    queryKey: ['evento', id],
    queryFn: () => apiClient.getEvento(id),
    enabled: !!id,
  });
};

// Hook para criar evento
export const useCreateEvento = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (evento: EventoCreate) => apiClient.createEvento(evento),
    onSuccess: () => {
      // Invalidar a lista de eventos
      queryClient.invalidateQueries({ queryKey: ['eventos'] });
    },
  });
};

// Hook para atualizar evento
export const useUpdateEvento = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, evento }: { id: number; evento: Partial<EventoCreate> }) =>
      apiClient.updateEvento(id, evento),
    onSuccess: (data, variables) => {
      // Invalidar a lista de eventos e o evento específico
      queryClient.invalidateQueries({ queryKey: ['eventos'] });
      queryClient.invalidateQueries({ queryKey: ['evento', variables.id] });
    },
  });
};

// Hook para deletar evento
export const useDeleteEvento = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.deleteEvento(id),
    onSuccess: () => {
      // Invalidar a lista de eventos
      queryClient.invalidateQueries({ queryKey: ['eventos'] });
    },
  });
};
