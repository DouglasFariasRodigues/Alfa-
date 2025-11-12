import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';

export interface Documento {
  id: number;
  membro: number;
  membro_nome: string;
  tipo: 'cartao_membro' | 'transferencia' | 'registro';
  arquivo?: string;
  gerado_em: string;
  gerado_por?: number;
  gerado_por_nome?: string;
}

export const useDocumentos = () => {
  return useQuery({
    queryKey: ['documentos'],
    queryFn: () => apiClient.getDocumentos(),
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
};

export const useDocumento = (id: number) => {
  return useQuery({
    queryKey: ['documento', id],
    queryFn: () => apiClient.getDocumento(id),
    enabled: !!id,
  });
};


