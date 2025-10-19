import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient, Postagem, PostagemCreate } from '@/lib/api';

// Hook para buscar postagens
export const usePostagens = () => {
  return useQuery({
    queryKey: ['postagens'],
    queryFn: () => apiClient.getPostagens(),
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
};

// Hook para buscar uma postagem específica
export const usePostagem = (id: number) => {
  return useQuery({
    queryKey: ['postagem', id],
    queryFn: () => apiClient.getPostagem(id),
    enabled: !!id,
  });
};

// Hook para criar postagem
export const useCreatePostagem = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (postagem: PostagemCreate) => apiClient.createPostagem(postagem),
    onSuccess: () => {
      // Invalidar a lista de postagens
      queryClient.invalidateQueries({ queryKey: ['postagens'] });
    },
  });
};

// Hook para atualizar postagem
export const useUpdatePostagem = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, postagem }: { id: number; postagem: Partial<PostagemCreate> }) =>
      apiClient.updatePostagem(id, postagem),
    onSuccess: (data, variables) => {
      // Invalidar a lista de postagens e a postagem específica
      queryClient.invalidateQueries({ queryKey: ['postagens'] });
      queryClient.invalidateQueries({ queryKey: ['postagem', variables.id] });
    },
  });
};

// Hook para deletar postagem
export const useDeletePostagem = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.deletePostagem(id),
    onSuccess: () => {
      // Invalidar a lista de postagens
      queryClient.invalidateQueries({ queryKey: ['postagens'] });
    },
  });
};
