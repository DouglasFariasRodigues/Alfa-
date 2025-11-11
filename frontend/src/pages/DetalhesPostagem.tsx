import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Edit, FileText, User, Calendar, Trash2, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { usePostagem, useDeletePostagem } from '@/hooks/usePostagens';
import { usePermissions } from '@/hooks/usePermissions';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';

export default function DetalhesPostagem() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const { data: postagem, isLoading, error } = usePostagem(Number(id));
  const { canManage } = usePermissions();
  const deletePostagemMutation = useDeletePostagem();
  
  // Verificar se o usuário pode gerenciar postagens (criar, editar, deletar)
  const canManagePostagens = canManage('postagens');

  const handleDelete = async () => {
    if (!postagem) return;
    
    if (window.confirm('Tem certeza que deseja excluir esta postagem?')) {
      try {
        await deletePostagemMutation.mutateAsync(postagem.id);
        toast.success('Postagem excluída com sucesso!');
        navigate('/postagens');
      } catch (error) {
        toast.error('Erro ao excluir postagem');
      }
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Skeleton className="h-10 w-10" />
          <div>
            <Skeleton className="h-8 w-48" />
            <Skeleton className="h-4 w-64 mt-2" />
          </div>
        </div>
        <Card>
          <CardHeader>
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-4 w-48" />
          </CardHeader>
          <CardContent className="space-y-4">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error || !postagem) {
    return (
      <div className="p-6">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-600">Erro ao carregar postagem</h2>
          <p className="text-gray-600">Postagem não encontrada ou erro ao carregar dados</p>
          <Button 
            onClick={() => navigate('/postagens')}
            className="mt-4"
          >
            Voltar para Postagens
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate('/postagens')}
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{postagem.titulo}</h1>
            <p className="text-muted-foreground">
              Detalhes da postagem
            </p>
          </div>
        </div>
        {canManagePostagens && (
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={() => navigate(`/postagens/${postagem.id}/editar`)}
            >
              <Edit className="mr-2 h-4 w-4" />
              Editar
            </Button>
            <Button
              variant="outline"
              className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200"
              onClick={handleDelete}
              disabled={deletePostagemMutation.isPending}
            >
              {deletePostagemMutation.isPending ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <Trash2 className="mr-2 h-4 w-4" />
              )}
              Excluir
            </Button>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="grid gap-6 md:grid-cols-3">
        {/* Conteúdo Principal */}
        <Card className="md:col-span-2 shadow-card">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="space-y-2">
                <CardTitle className="text-2xl">{postagem.titulo}</CardTitle>
                <CardDescription>
                  Publicado em {new Date(postagem.data_publicacao).toLocaleDateString('pt-BR', {
                    day: '2-digit',
                    month: 'long',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </CardDescription>
              </div>
              <Badge variant="outline" className="text-sm">
                Postagem
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <Separator />
            
            {/* Conteúdo */}
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
                <FileText className="h-4 w-4" />
                Conteúdo
              </div>
              <div className="prose max-w-none">
                <p className="text-base leading-relaxed whitespace-pre-wrap">
                  {postagem.conteudo}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Informações */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="text-lg">Informações</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <User className="h-4 w-4" />
                  <span className="font-medium">Autor</span>
                </div>
                <p className="text-sm font-medium">
                  {postagem.autor_nome || 'Autor desconhecido'}
                </p>
              </div>

              <Separator />

              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="h-4 w-4" />
                  <span className="font-medium">Data de Publicação</span>
                </div>
                <p className="text-sm font-medium">
                  {new Date(postagem.data_publicacao).toLocaleDateString('pt-BR', {
                    day: '2-digit',
                    month: 'long',
                    year: 'numeric'
                  })}
                </p>
                <p className="text-xs text-muted-foreground">
                  {new Date(postagem.data_publicacao).toLocaleTimeString('pt-BR', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Ações Rápidas */}
          {canManagePostagens && (
            <Card className="shadow-card">
              <CardHeader>
                <CardTitle className="text-lg">Ações</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button
                  variant="outline"
                  className="w-full justify-start"
                  onClick={() => navigate(`/postagens/${postagem.id}/editar`)}
                >
                  <Edit className="mr-2 h-4 w-4" />
                  Editar Postagem
                </Button>
                <Button
                  variant="outline"
                  className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200"
                  onClick={handleDelete}
                  disabled={deletePostagemMutation.isPending}
                >
                  {deletePostagemMutation.isPending ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Excluindo...
                    </>
                  ) : (
                    <>
                      <Trash2 className="mr-2 h-4 w-4" />
                      Excluir Postagem
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

