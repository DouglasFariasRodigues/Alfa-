import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { 
  FileText, 
  Plus, 
  Search, 
  Calendar, 
  User, 
  Edit, 
  Trash2, 
  Eye,
  Loader2
} from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { usePostagens, useDeletePostagem } from "@/hooks/usePostagens";
import { toast } from "sonner";

export default function Postagens() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  
  // Buscar postagens da API
  const { data: postagens = [], isLoading, error } = usePostagens({ 
    search: searchTerm || undefined 
  });
  
  const deletePostagemMutation = useDeletePostagem();

  const handleDeletePostagem = async (id: number) => {
    if (window.confirm('Tem certeza que deseja excluir esta postagem?')) {
      try {
        await deletePostagemMutation.mutateAsync(id);
        toast.success('Postagem excluída com sucesso!');
      } catch (error) {
        toast.error('Erro ao excluir postagem');
      }
    }
  };

  // Filtrar postagens por termo de busca
  const postagensFiltradas = postagens.filter(postagem =>
    postagem.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    postagem.conteudo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    postagem.autor_nome.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Calcular estatísticas
  const totalPostagens = postagens.length;
  const postagensEsteMes = postagens.filter(p => {
    const dataPostagem = new Date(p.data_publicacao);
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    return dataPostagem.getMonth() === currentMonth && dataPostagem.getFullYear() === currentYear;
  }).length;

  const postagensRecentes = postagens
    .sort((a, b) => new Date(b.data_publicacao).getTime() - new Date(a.data_publicacao).getTime())
    .slice(0, 5);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (dataPublicacao: string) => {
    const dataPostagem = new Date(dataPublicacao);
    const agora = new Date();
    const diffTime = agora.getTime() - dataPostagem.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays <= 1) {
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    } else if (diffDays <= 7) {
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
    } else {
      return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  const getStatusLabel = (dataPublicacao: string) => {
    const dataPostagem = new Date(dataPublicacao);
    const agora = new Date();
    const diffTime = agora.getTime() - dataPostagem.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays <= 1) {
      return 'Recente';
    } else if (diffDays <= 7) {
      return 'Esta semana';
    } else {
      return 'Antiga';
    }
  };

  if (error) {
    return (
      <div className="p-6">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-600">Erro ao carregar postagens</h2>
          <p className="text-gray-600">Tente recarregar a página</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Postagens</h1>
          <p className="text-muted-foreground">
            Gerencie as postagens e notícias da igreja
          </p>
        </div>
        <Button onClick={() => navigate('/postagens/nova')}>
          <Plus className="h-4 w-4 mr-2" />
          Nova Postagem
        </Button>
      </div>

      {/* Estatísticas */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-muted-foreground" />
              <div className="ml-4">
                <p className="text-2xl font-bold">{totalPostagens}</p>
                <p className="text-sm text-muted-foreground">Total de Postagens</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Calendar className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <p className="text-2xl font-bold">{postagensEsteMes}</p>
                <p className="text-sm text-muted-foreground">Este Mês</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <User className="h-8 w-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-2xl font-bold">
                  {new Set(postagens.map(p => p.autor_nome)).size}
                </p>
                <p className="text-sm text-muted-foreground">Autores Únicos</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filtros */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="h-5 w-5" />
            Buscar Postagens
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Buscar por título, conteúdo ou autor..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardContent>
      </Card>

      {/* Lista de Postagens */}
      <Card>
        <CardHeader>
          <CardTitle>Postagens</CardTitle>
          <CardDescription>
            {postagensFiltradas.length} postagem(ns) encontrada(s)
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin" />
              <span className="ml-2">Carregando postagens...</span>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Título</TableHead>
                  <TableHead>Autor</TableHead>
                  <TableHead>Data de Publicação</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {postagensFiltradas.map((postagem) => (
                  <TableRow key={postagem.id}>
                    <TableCell className="font-medium">
                      <div>
                        <div className="font-semibold">{postagem.titulo}</div>
                        <div className="text-sm text-muted-foreground line-clamp-2">
                          {postagem.conteudo.substring(0, 100)}...
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4 text-muted-foreground" />
                        {postagem.autor_nome}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        {formatDate(postagem.data_publicacao)}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(postagem.data_publicacao)}>
                        {getStatusLabel(postagem.data_publicacao)}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => navigate(`/postagens/${postagem.id}`)}
                        >
                          <Eye className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => navigate(`/postagens/editar/${postagem.id}`)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDeletePostagem(postagem.id)}
                          disabled={deletePostagemMutation.isPending}
                        >
                          {deletePostagemMutation.isPending ? (
                            <Loader2 className="h-4 w-4 animate-spin" />
                          ) : (
                            <Trash2 className="h-4 w-4" />
                          )}
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
          
          {postagensFiltradas.length === 0 && !isLoading && (
            <div className="text-center py-8">
              <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Nenhuma postagem encontrada</h3>
              <p className="text-muted-foreground mb-4">
                {searchTerm ? 'Tente ajustar os filtros de busca.' : 'Comece criando sua primeira postagem.'}
              </p>
              {!searchTerm && (
                <Button onClick={() => navigate('/postagens/nova')}>
                  <Plus className="h-4 w-4 mr-2" />
                  Criar Primeira Postagem
                </Button>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Postagens Recentes */}
      {postagensRecentes.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Postagens Recentes</CardTitle>
            <CardDescription>
              Últimas postagens publicadas
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {postagensRecentes.map((postagem) => (
                <div key={postagem.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium">{postagem.titulo}</h4>
                    <p className="text-sm text-muted-foreground">
                      Por {postagem.autor_nome} • {formatDate(postagem.data_publicacao)}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => navigate(`/postagens/${postagem.id}`)}
                    >
                      <Eye className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
