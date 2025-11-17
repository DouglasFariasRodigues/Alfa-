const API_BASE_URL = 'http://localhost:8000/api';

export const api = {
  gerarCartaoMembro: async (membroId: number) => {
    const response = await fetch(`${API_BASE_URL}/gerar-cartao-membro/${membroId}/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    });

    if (!response.ok) {
      throw new Error('Erro ao gerar cartão do membro');
    }

    return response.blob();
  },

  gerarPdfTransferencia: async (transferenciaId: number) => {
    const response = await fetch(`${API_BASE_URL}/gerar-pdf-transferencia/${transferenciaId}/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    });

    if (!response.ok) {
      throw new Error('Erro ao gerar PDF da transferência');
    }

    return response.blob();
  },
};
