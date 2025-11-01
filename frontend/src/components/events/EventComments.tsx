import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { useEventComments, useCreateEventComment, useDeleteEventComment } from '@/hooks/useEventComments';
import { usePermissions } from '@/hooks/usePermissions';
import { MessageCircle, Send, Trash2, User } from 'lucide-react';
import { toast } from 'sonner';

interface EventCommentsProps {
  eventoId: number;
}

export const EventComments: React.FC<EventCommentsProps> = ({ eventoId }) => {
  const [newComment, setNewComment] = useState('');
  const { data: comments = [], isLoading } = useEventComments(eventoId);
  const createCommentMutation = useCreateEventComment();
  const deleteCommentMutation = useDeleteEventComment();
  const { user } = usePermissions();

  const handleSubmitComment = async () => {
    if (!newComment.trim() || !user) {
      toast.error('Comentário não pode estar vazio');
      return;
    }

    try {
      await createCommentMutation.mutateAsync({
        evento: eventoId,
        membro: user.id,
        comentario: newComment.trim()
      });
      setNewComment('');
      toast.success('Comentário adicionado com sucesso!');
    } catch (error) {
      toast.error('Erro ao adicionar comentário');
      console.error('Erro ao criar comentário:', error);
    }
  };

  const handleDeleteComment = async (commentId: number) => {
    if (!confirm('Tem certeza que deseja excluir este comentário?')) {
      return;
    }

    try {
      await deleteCommentMutation.mutateAsync(commentId);
      toast.success('Comentário excluído com sucesso!');
    } catch (error) {
      toast.error('Erro ao excluir comentário');
      console.error('Erro ao excluir comentário:', error);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(word => word.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <Card className="shadow-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageCircle className="h-5 w-5 text-primary" />
          Comentários ({comments.length})
        </CardTitle>
        <CardDescription>
          Compartilhe suas experiências e opiniões sobre este evento
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Formulário para novo comentário */}
        {user && (
          <div className="space-y-4">
            <div className="flex gap-3">
              <Avatar className="h-10 w-10">
                <AvatarFallback>
                  {getInitials(user.nome || 'U')}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 space-y-2">
                <Textarea
                  placeholder="Escreva seu comentário..."
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  className="min-h-[80px] resize-none"
                />
                <div className="flex justify-end">
                  <Button
                    onClick={handleSubmitComment}
                    disabled={!newComment.trim() || createCommentMutation.isPending}
                    size="sm"
                  >
                    {createCommentMutation.isPending ? (
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                    ) : (
                      <Send className="h-4 w-4 mr-2" />
                    )}
                    Comentar
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Lista de comentários */}
        <div className="space-y-4">
          {isLoading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4" />
              <p className="text-muted-foreground">Carregando comentários...</p>
            </div>
          ) : comments.length === 0 ? (
            <div className="text-center py-8">
              <MessageCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">Nenhum comentário ainda.</p>
              <p className="text-sm text-muted-foreground">Seja o primeiro a comentar!</p>
            </div>
          ) : (
            comments.map((comment: any) => (
              <div key={comment.id} className="flex gap-3 p-4 border rounded-lg bg-gray-50 dark:bg-gray-900">
                <Avatar className="h-10 w-10">
                  <AvatarFallback>
                    {getInitials(comment.membro_nome || 'U')}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 space-y-2">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-sm">{comment.membro_nome}</p>
                      <p className="text-xs text-muted-foreground">
                        {formatDate(comment.data_comentario)}
                      </p>
                    </div>
                    {user && user.id === comment.membro && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDeleteComment(comment.id)}
                        disabled={deleteCommentMutation.isPending}
                        className="h-8 w-8 p-0 text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">
                    {comment.comentario}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
};
