import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileText, Plus, Filter, Loader2, Eye, Trash2, Edit, User, Calendar } from "lucide-react";
import { Input } from "@/components/ui/input";
import { usePostagens, useDeletePostagem } from "@/hooks/usePostagens";
import { usePermissions } from "@/hooks/usePermissions";
import { toast } from "sonner";

export default function Postagens() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");

  // Buscar postagens da API
  const { data: postagens = [], isLoading, error } = usePostagens({ 
    search: searchTerm || undefined 
  });
  
  const deletePostagemMutation = useDeletePostagem();
  const { canManage } = usePermissions();
  
  // Verificar se o usuário pode gerenciar postagens (criar, editar, deletar)
  const canManagePostagens = canManage('postagens');

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
  const filteredPostagens = postagens.filter(postagem => {
    if (!searchTerm) return true;
    const search = searchTerm.toLowerCase();
    return (
      postagem.titulo.toLowerCase().includes(search) ||
      postagem.conteudo.toLowerCase().includes(search) ||
      postagem.autor_nome?.toLowerCase().includes(search)
    );
  });

  // Calcular estatísticas
  const totalPostagens = postagens.length;
  const postagensEsteMes = postagens.filter(p => {
    const dataPostagem = new Date(p.data_publicacao);
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    return dataPostagem.getMonth() === currentMonth && dataPostagem.getFullYear() === currentYear;
  }).length;

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
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Postagens</h1>
          <p className="text-muted-foreground">
            Gerencie as postagens e notícias da sua igreja
          </p>
        </div>
        {canManagePostagens && (
          <Button 
            onClick={() => navigate('/postagens/novo')}
            className="gradient-primary text-white shadow-elegant hover:opacity-90"
          >
            <Plus className="mr-2 h-4 w-4" />
            Nova Postagem
          </Button>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total de Postagens</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalPostagens}</div>
            <p className="text-xs text-green-600">{postagensEsteMes} este mês</p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Postagens Este Mês</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{postagensEsteMes}</div>
            <p className="text-xs text-muted-foreground">Publicadas</p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Última Postagem</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {postagens.length > 0 
                ? new Date(postagens[0].data_publicacao).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })
                : '-'
              }
            </div>
            <p className="text-xs text-muted-foreground">Data da última publicação</p>
          </CardContent>
        </Card>
      </div>

      {/* Search and Filter */}
      <Card className="shadow-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Todas as Postagens</CardTitle>
              <CardDescription>
                Visualize e gerencie todas as postagens publicadas
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <div className="relative">
                <Input
                  placeholder="Buscar postagens..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-64"
                />
              </div>
              <Button variant="outline" size="sm">
                <Filter className="mr-2 h-4 w-4" />
                Filtros
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin" />
              <span className="ml-2">Carregando postagens...</span>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {filteredPostagens.length === 0 ? (
                <div className="col-span-full text-center py-12">
                  <div className="text-muted-foreground">
                    <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p className="text-lg font-medium">Nenhuma postagem encontrada</p>
                    <p className="text-sm">
                      {searchTerm 
                        ? "Não há postagens que correspondam à sua busca"
                        : "Não há postagens cadastradas no momento"
                      }
                    </p>
                  </div>
                </div>
              ) : (
                filteredPostagens.map((postagem) => (
                  <Card key={postagem.id} className="shadow-card hover:shadow-elegant transition-all duration-300 hover:-translate-y-1 h-full flex flex-col">
                    <CardHeader className="pb-4 flex-1">
                      <div className="space-y-2">
                        <CardTitle className="text-xl leading-tight line-clamp-2">{postagem.titulo}</CardTitle>
                        <CardDescription className="line-clamp-3 text-sm leading-relaxed">
                          {postagem.conteudo}
                        </CardDescription>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4 flex-1 flex flex-col justify-between">
                      <div className="space-y-2">
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <User className="h-4 w-4" />
                          <span>{postagem.autor_nome || 'Autor desconhecido'}</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                          <Calendar className="h-4 w-4" />
                          <span>
                            {new Date(postagem.data_publicacao).toLocaleDateString('pt-BR', {
                              day: '2-digit',
                              month: 'long',
                              year: 'numeric'
                            })}
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center justify-between pt-4 border-t">
                        <Badge variant="outline" className="text-sm">
                          Postagem
                        </Badge>
                        <div className="flex gap-2">
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => navigate(`/postagens/${postagem.id}`)}
                          >
                            <Eye className="mr-2 h-4 w-4" />
                            Ver
                          </Button>
                          {canManagePostagens && (
                            <>
                              <Button 
                                variant="outline" 
                                size="sm"
                                onClick={() => navigate(`/postagens/${postagem.id}/editar`)}
                              >
                                <Edit className="mr-2 h-4 w-4" />
                                Editar
                              </Button>
                              <Button 
                                variant="outline" 
                                size="sm"
                                className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200"
                                onClick={() => handleDeletePostagem(postagem.id)}
                                disabled={deletePostagemMutation.isPending}
                              >
                                {deletePostagemMutation.isPending ? (
                                  <Loader2 className="h-4 w-4 animate-spin" />
                                ) : (
                                  <Trash2 className="h-4 w-4" />
                                )}
                              </Button>
                            </>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

