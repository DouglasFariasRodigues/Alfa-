// Configuração da API
const API_BASE_URL = 'http://localhost:8000/api';

// Tipos para autenticação
export interface LoginRequest {
  email: string;
  senha: string;
}

export interface LoginResponse {
  success: boolean;
  message: string;
  access_token?: string;
  refresh_token?: string;
  user?: {
    id: number;
    nome: string;
    email: string;
    cargo?: {
      id: number;
      nome: string;
    };
  };
}

// Tipos para membros
export interface Membro {
  id: number;
  nome: string;
  cpf: string;
  rg?: string;
  data_nascimento?: string;
  telefone: string;
  email: string;
  endereco?: string;
  foto?: string;
  status: 'ativo' | 'inativo' | 'falecido' | 'afastado';
  data_batismo?: string;
  igreja_origem?: string;
  observacoes?: string;
  cadastrado_por_nome?: string;
  cargo?: number;
  cargo_nome?: string;
  created_at: string;
  updated_at: string;
}

export interface MembroCreate {
  nome: string;
  cpf: string;
  rg?: string;
  data_nascimento?: string;
  telefone: string;
  email: string;
  endereco?: string;
  foto?: File;
  status: 'ativo' | 'inativo' | 'falecido' | 'afastado';
  data_batismo?: string;
  igreja_origem?: string;
  senha: string;
  observacoes?: string;
}

// Tipos para eventos
export interface Evento {
  id: number;
  titulo: string;
  descricao: string;
  data: string;
  local: string;
  observacoes?: string;
  organizador_nome: string;
  foto?: string;
}

export interface EventoCreate {
  titulo: string;
  descricao: string;
  data: string;
  local: string;
  observacoes?: string;
  foto?: File;
}

// Tipos para transações
export interface Transacao {
  id: number;
  tipo: 'entrada' | 'saida';
  categoria: string;
  valor: number;
  data: string;
  descricao: string;
  metodo_pagamento: string;
  observacoes: string;
  registrado_por_nome: string;
  created_at: string;
  updated_at: string;
}

export interface TransacaoCreate {
  tipo: 'entrada' | 'saida';
  categoria: string;
  valor: number;
  data: string;
  descricao: string;
  metodo_pagamento: string;
  observacoes: string;
}

// Tipos para postagens
export interface Postagem {
  id: number;
  titulo: string;
  conteudo: string;
  autor_nome: string;
  data_publicacao: string;
}

export interface PostagemCreate {
  titulo: string;
  conteudo: string;
}

// Classe para gerenciar tokens
class TokenManager {
  private static readonly ACCESS_TOKEN_KEY = 'access_token';
  private static readonly REFRESH_TOKEN_KEY = 'refresh_token';

  static setTokens(accessToken: string, refreshToken: string) {
    localStorage.setItem(this.ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
  }

  static getAccessToken(): string | null {
    return localStorage.getItem(this.ACCESS_TOKEN_KEY);
  }

  static getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  static clearTokens() {
    localStorage.removeItem(this.ACCESS_TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
  }

  static isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }
}

// Classe principal da API
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const token = TokenManager.getAccessToken();

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (response.status === 401) {
        // Token expirado, tentar refresh
        const refreshed = await this.refreshToken();
        if (refreshed) {
          // Tentar novamente com novo token
          config.headers = {
            ...config.headers,
            Authorization: `Bearer ${TokenManager.getAccessToken()}`,
          };
          const retryResponse = await fetch(url, config);
          if (!retryResponse.ok) {
            throw new Error(`HTTP error! status: ${retryResponse.status}`);
          }
          return retryResponse.json();
        } else {
          // Refresh falhou, redirecionar para login
          TokenManager.clearTokens();
          window.location.href = '/login';
          throw new Error('Authentication failed');
        }
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  private async refreshToken(): Promise<boolean> {
    const refreshToken = TokenManager.getRefreshToken();
    if (!refreshToken) return false;

    try {
      const response = await fetch(`${this.baseURL}/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        TokenManager.setTokens(data.access, refreshToken);
        return true;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
    }

    return false;
  }

  // Métodos de autenticação
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await this.request<LoginResponse>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    if (response.success && response.access_token && response.refresh_token) {
      TokenManager.setTokens(response.access_token, response.refresh_token);
    }

    return response;
  }

  async logout(): Promise<void> {
    TokenManager.clearTokens();
  }

  // Métodos para membros
  async getMembros(params?: { status?: string; search?: string }): Promise<Membro[]> {
    const queryParams = new URLSearchParams();
    if (params?.status) queryParams.append('status', params.status);
    if (params?.search) queryParams.append('search', params.search);
    
    const queryString = queryParams.toString();
    const endpoint = queryString ? `/membros/?${queryString}` : '/membros/';
    
    return this.request<Membro[]>(endpoint);
  }

  async getMembro(id: number): Promise<Membro> {
    return this.request<Membro>(`/membros/${id}/`);
  }

  async createMembro(membro: MembroCreate): Promise<Membro> {
    return this.request<Membro>('/membros/', {
      method: 'POST',
      body: JSON.stringify(membro),
    });
  }

  async updateMembro(id: number, membro: Partial<MembroCreate>): Promise<Membro> {
    return this.request<Membro>(`/membros/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(membro),
    });
  }

  async deleteMembro(id: number): Promise<void> {
    return this.request<void>(`/membros/${id}/`, {
      method: 'DELETE',
    });
  }

  // Métodos para eventos
  async getEventos(params?: { search?: string }): Promise<Evento[]> {
    const queryParams = new URLSearchParams();
    if (params?.search) queryParams.append('search', params.search);
    
    const queryString = queryParams.toString();
    const endpoint = queryString ? `/eventos/?${queryString}` : '/eventos/';
    
    return this.request<Evento[]>(endpoint);
  }

  async getEvento(id: number): Promise<Evento> {
    return this.request<Evento>(`/eventos/${id}/`);
  }

  async createEvento(evento: EventoCreate): Promise<Evento> {
    return this.request<Evento>('/eventos/', {
      method: 'POST',
      body: JSON.stringify(evento),
    });
  }

  async updateEvento(id: number, evento: Partial<EventoCreate>): Promise<Evento> {
    return this.request<Evento>(`/eventos/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(evento),
    });
  }

  async deleteEvento(id: number): Promise<void> {
    return this.request<void>(`/eventos/${id}/`, {
      method: 'DELETE',
    });
  }

  // Métodos para transações
  async getTransacoes(params?: { tipo?: string; categoria?: string }): Promise<Transacao[]> {
    const queryParams = new URLSearchParams();
    if (params?.tipo) queryParams.append('tipo', params.tipo);
    if (params?.categoria) queryParams.append('categoria', params.categoria);
    
    const queryString = queryParams.toString();
    const endpoint = queryString ? `/transacoes/?${queryString}` : '/transacoes/';
    
    return this.request<Transacao[]>(endpoint);
  }

  async getTransacao(id: number): Promise<Transacao> {
    return this.request<Transacao>(`/transacoes/${id}/`);
  }

  async createTransacao(transacao: TransacaoCreate): Promise<Transacao> {
    return this.request<Transacao>('/transacoes/', {
      method: 'POST',
      body: JSON.stringify(transacao),
    });
  }

  async updateTransacao(id: number, transacao: Partial<TransacaoCreate>): Promise<Transacao> {
    return this.request<Transacao>(`/transacoes/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(transacao),
    });
  }

  async deleteTransacao(id: number): Promise<void> {
    return this.request<void>(`/transacoes/${id}/`, {
      method: 'DELETE',
    });
  }

  // Métodos para postagens
  async getPostagens(): Promise<Postagem[]> {
    return this.request<Postagem[]>('/postagens/');
  }

  async getPostagem(id: number): Promise<Postagem> {
    return this.request<Postagem>(`/postagens/${id}/`);
  }

  async createPostagem(postagem: PostagemCreate): Promise<Postagem> {
    return this.request<Postagem>('/postagens/', {
      method: 'POST',
      body: JSON.stringify(postagem),
    });
  }

  async updatePostagem(id: number, postagem: Partial<PostagemCreate>): Promise<Postagem> {
    return this.request<Postagem>(`/postagens/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(postagem),
    });
  }

  async deletePostagem(id: number): Promise<void> {
    return this.request<void>(`/postagens/${id}/`, {
      method: 'DELETE',
    });
  }

  // Métodos para cargos
  async getCargos(params?: { search?: string; pode_fazer_postagens?: boolean; pode_registrar_dizimos?: boolean; pode_registrar_ofertas?: boolean }): Promise<any[]> {
    const queryParams = new URLSearchParams();
    if (params?.search) queryParams.append('search', params.search);
    if (params?.pode_fazer_postagens !== undefined) queryParams.append('pode_fazer_postagens', params.pode_fazer_postagens.toString());
    if (params?.pode_registrar_dizimos !== undefined) queryParams.append('pode_registrar_dizimos', params.pode_registrar_dizimos.toString());
    if (params?.pode_registrar_ofertas !== undefined) queryParams.append('pode_registrar_ofertas', params.pode_registrar_ofertas.toString());
    
    const queryString = queryParams.toString();
    const endpoint = queryString ? `/cargos/?${queryString}` : '/cargos/';
    
    return this.request<any[]>(endpoint);
  }

  async getCargo(id: number): Promise<any> {
    return this.request<any>(`/cargos/${id}/`);
  }

  async createCargo(cargo: any): Promise<any> {
    return this.request<any>('/cargos/', {
      method: 'POST',
      body: JSON.stringify(cargo),
    });
  }

  async updateCargo(id: number, cargo: any): Promise<any> {
    return this.request<any>(`/cargos/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(cargo),
    });
  }

  async deleteCargo(id: number): Promise<void> {
    return this.request<void>(`/cargos/${id}/`, {
      method: 'DELETE',
    });
  }

  // Métodos para upload de imagens
  async uploadMembroFoto(formData: FormData, membroId?: number): Promise<any> {
    const endpoint = membroId ? `/membros/${membroId}/upload-foto/` : '/membros/upload-foto/';
    return this.request<any>(endpoint, {
      method: 'POST',
      body: formData,
      headers: {
        // Não definir Content-Type para FormData, o browser define automaticamente
      },
    });
  }

  async uploadEventoFoto(formData: FormData, eventoId?: number): Promise<any> {
    const endpoint = eventoId ? `/eventos/${eventoId}/upload-foto/` : '/eventos/upload-foto/';
    return this.request<any>(endpoint, {
      method: 'POST',
      body: formData,
    });
  }

  async uploadPostagemFoto(formData: FormData, postagemId?: number): Promise<any> {
    const endpoint = postagemId ? `/postagens/${postagemId}/upload-foto/` : '/postagens/upload-foto/';
    return this.request<any>(endpoint, {
      method: 'POST',
      body: formData,
    });
  }

  async deleteImage(imageUrl: string, endpoint: 'membros' | 'eventos' | 'postagens', entityId: number): Promise<void> {
    const baseEndpoint = endpoint === 'membros' ? '/membros' : endpoint === 'eventos' ? '/eventos' : '/postagens';
    return this.request<void>(`${baseEndpoint}/${entityId}/delete-foto/`, {
      method: 'DELETE',
      body: JSON.stringify({ image_url: imageUrl }),
    });
  }

  // Método para obter dados do usuário atual
  async getCurrentUser(): Promise<any> {
    return this.request<any>('/auth/me/');
  }

  // Método para login de membro
  async loginMembro(credentials: { email: string; senha: string }): Promise<any> {
    const response = await this.request<any>('/auth/login_membro/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    if (response.success && response.access_token && response.refresh_token) {
      TokenManager.setTokens(response.access_token, response.refresh_token);
    }

    return response;
  }

  // Métodos para confirmação de presença em eventos
  async getEventPresences(membroId?: number): Promise<any> {
    const url = membroId ? `/eventos-presencas/?membro=${membroId}` : '/eventos-presencas/';
    return this.request<any>(url);
  }

  async confirmEventPresence(data: { evento: number; membro: number; confirmado: boolean; observacoes?: string }): Promise<any> {
    return this.request<any>('/eventos-presencas/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async cancelEventPresence(presenceId: number): Promise<any> {
    return this.request<any>(`/eventos-presencas/${presenceId}/`, {
      method: 'DELETE',
    });
  }

  async getEventComments(eventoId?: number): Promise<any> {
    const url = eventoId ? `/eventos-comentarios/?evento=${eventoId}` : '/eventos-comentarios/';
    return this.request<any>(url);
  }

  async createEventComment(data: { evento: number; membro: number; comentario: string }): Promise<any> {
    return this.request<any>('/eventos-comentarios/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async deleteEventComment(commentId: number): Promise<any> {
    return this.request<any>(`/eventos-comentarios/${commentId}/`, {
      method: 'DELETE',
    });
  }
}

// Instância singleton da API
export const apiClient = new ApiClient();

// Exportar TokenManager para uso em componentes
export { TokenManager };
