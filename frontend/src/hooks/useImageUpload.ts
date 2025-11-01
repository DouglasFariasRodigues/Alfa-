import { useState } from 'react';
import { apiClient } from '@/lib/api';

export interface UploadResult {
  url: string;
  filename: string;
  size: number;
}

export const useImageUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const uploadImage = async (
    file: File,
    endpoint: 'membros' | 'eventos' | 'postagens',
    entityId?: number
  ): Promise<UploadResult> => {
    setUploading(true);
    setProgress(0);

    try {
      const formData = new FormData();
      formData.append('imagem', file);
      
      if (entityId) {
        formData.append('entity_id', entityId.toString());
      }

      // Simular progresso
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 100);

      let response;
      switch (endpoint) {
        case 'membros':
          response = await apiClient.uploadMembroFoto(formData, entityId);
          break;
        case 'eventos':
          response = await apiClient.uploadEventoFoto(formData, entityId);
          break;
        case 'postagens':
          response = await apiClient.uploadPostagemFoto(formData, entityId);
          break;
        default:
          throw new Error('Endpoint não suportado');
      }

      clearInterval(progressInterval);
      setProgress(100);

      return {
        url: response.url || response.imagem,
        filename: file.name,
        size: file.size
      };

    } catch (error: any) {
      setProgress(0);
      throw new Error(error.response?.data?.message || 'Erro ao fazer upload da imagem');
    } finally {
      setUploading(false);
      setTimeout(() => setProgress(0), 500);
    }
  };

  const deleteImage = async (
    imageUrl: string,
    endpoint: 'membros' | 'eventos' | 'postagens',
    entityId: number
  ): Promise<void> => {
    try {
      await apiClient.deleteImage(imageUrl, endpoint, entityId);
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Erro ao deletar imagem');
    }
  };

  return {
    uploadImage,
    deleteImage,
    uploading,
    progress
  };
};
