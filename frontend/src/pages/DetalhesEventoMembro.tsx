import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Calendar, Clock, MapPin, User, CheckCircle, MessageCircle, Heart } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { useEvento } from '@/hooks/useEventos'
import { usePermissions } from '@/hooks/usePermissions'
import { useEventPresences, useConfirmPresence } from '@/hooks/useEventPresence'
import { EventComments } from '@/components/events/EventComments'
import { Skeleton } from '@/components/ui/skeleton'
import { toast } from 'sonner'

export default function DetalhesEventoMembro() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  
  const { data: evento, isLoading, error } = useEvento(Number(id))
  const { user } = usePermissions()
  const confirmPresenceMutation = useConfirmPresence()
  
  // Buscar confirmações de presença do membro
  const { data: presencas = [] } = useEventPresences(user?.id);

  // Verificar se o membro já confirmou presença neste evento
  const isPresenceConfirmed = (eventoId: number) => {
    return presencas.some((presenca: any) => presenca.evento === eventoId && presenca.confirmado);
  };

  const handleConfirmPresence = async () => {
    if (!evento || !user) return;
    
    try {
      await confirmPresenceMutation.mutateAsync({
        evento: evento.id,
        membro: user.id,
        confirmado: true
      });
      toast.success('Presença confirmada com sucesso!');
    } catch (error) {
      toast.error('Erro ao confirmar presença');
      console.error('Erro ao confirmar presença:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Skeleton className="h-8 w-8" />
          <div className="space-y-2">
            <Skeleton className="h-8 w-64" />
            <Skeleton className="h-4 w-48" />
          </div>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="space-y-4">
            <Skeleton className="h-32 w-full" />
            <Skeleton className="h-24 w-full" />
          </div>
          <div className="space-y-4">
            <Skeleton className="h-32 w-full" />
            <Skeleton className="h-24 w-full" />
          </div>
        </div>
      </div>
    );
  }

  if (error || !evento) {
    return (
      <div className="text-center py-8">
        <h2 className="text-xl font-semibold text-red-600">Evento não encontrado</h2>
        <p className="text-gray-600">O evento que você está procurando não existe</p>
        <Button 
          onClick={() => navigate('/eventos-membro')} 
          className="mt-4"
        >
          Voltar para Eventos
        </Button>
      </div>
    );
  }

  const getEventStatus = (data: string) => {
    const agora = new Date();
    const dataEvento = new Date(data);
    const diffTime = dataEvento.getTime() - agora.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) return { text: "Passado", color: "bg-gray-100 text-gray-800" };
    if (diffDays === 0) return { text: "Hoje", color: "bg-blue-100 text-blue-800" };
    if (diffDays === 1) return { text: "Amanhã", color: "bg-yellow-100 text-yellow-800" };
    if (diffDays <= 7) return { text: "Esta semana", color: "bg-green-100 text-green-800" };
    return { text: "Futuro", color: "bg-purple-100 text-purple-800" };
  }

  const eventStatus = getEventStatus(evento.data)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate('/eventos-membro')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{evento.titulo}</h1>
            <p className="text-muted-foreground">
              Detalhes do evento e participação
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          {isPresenceConfirmed(evento.id) ? (
            <Button 
              variant="outline"
              className="border-green-500 text-green-600 bg-green-50"
              disabled
            >
              <CheckCircle className="h-4 w-4 mr-2" />
              Presença Confirmada
            </Button>
          ) : (
            <Button 
              onClick={handleConfirmPresence}
              className="bg-green-600 hover:bg-green-700"
              disabled={confirmPresenceMutation.isPending}
            >
              <CheckCircle className="h-4 w-4 mr-2" />
              {confirmPresenceMutation.isPending ? 'Confirmando...' : 'Confirmar Presença'}
            </Button>
          )}
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Informações do Evento */}
        <div className="space-y-6">
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5 text-primary" />
                Informações do Evento
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">Data</p>
                    <p className="text-sm text-muted-foreground">
                      {new Date(evento.data).toLocaleDateString('pt-BR', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">Horário</p>
                    <p className="text-sm text-muted-foreground">
                      {new Date(evento.data).toLocaleTimeString('pt-BR', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">Local</p>
                    <p className="text-sm text-muted-foreground">
                      {evento.local || 'Local não informado'}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3">
                  <User className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="font-medium">Organizador</p>
                    <p className="text-sm text-muted-foreground">
                      {evento.organizador_nome}
                    </p>
                  </div>
                </div>
              </div>
              
              <Separator />
              
              <div className="flex items-center justify-between">
                <span className="font-medium">Status do Evento</span>
                <Badge className={eventStatus.color}>
                  {eventStatus.text}
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Descrição */}
          {evento.descricao && (
            <Card className="shadow-card">
              <CardHeader>
                <CardTitle>Sobre o Evento</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground leading-relaxed">
                  {evento.descricao}
                </p>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Participação e Ações */}
        <div className="space-y-6">
          {/* Status de Presença */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                Sua Participação
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {isPresenceConfirmed(evento.id) ? (
                <div className="text-center py-4">
                  <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CheckCircle className="h-8 w-8 text-green-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-green-800">Presença Confirmada!</h3>
                  <p className="text-sm text-green-600 mt-2">
                    Você confirmou sua presença neste evento
                  </p>
                </div>
              ) : (
                <div className="text-center py-4">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Calendar className="h-8 w-8 text-gray-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-800">Confirme sua Presença</h3>
                  <p className="text-sm text-gray-600 mt-2">
                    Clique no botão acima para confirmar sua participação
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Ações Rápidas */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Heart className="h-5 w-5 text-red-500" />
                Ações Rápidas
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button 
                variant="outline" 
                className="w-full justify-start"
                onClick={() => {
                  // Aqui você pode implementar compartilhamento
                  navigator.share?.({
                    title: evento.titulo,
                    text: `Confira este evento: ${evento.titulo}`,
                    url: window.location.href
                  }).catch(() => {
                    // Fallback para copiar link
                    navigator.clipboard.writeText(window.location.href);
                    toast.success('Link copiado para a área de transferência!');
                  });
                }}
              >
                <MessageCircle className="mr-2 h-4 w-4" />
                Compartilhar Evento
              </Button>
              
              <Button 
                variant="outline" 
                className="w-full justify-start"
                onClick={() => {
                  // Aqui você pode implementar adicionar ao calendário
                  const startDate = new Date(evento.data);
                  const endDate = new Date(startDate.getTime() + 2 * 60 * 60 * 1000); // +2 horas
                  
                  const calendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(evento.titulo)}&dates=${startDate.toISOString().replace(/[-:]/g, '').split('.')[0]}Z/${endDate.toISOString().replace(/[-:]/g, '').split('.')[0]}Z&details=${encodeURIComponent(evento.descricao || '')}&location=${encodeURIComponent(evento.local || '')}`;
                  
                  window.open(calendarUrl, '_blank');
                }}
              >
                <Calendar className="mr-2 h-4 w-4" />
                Adicionar ao Calendário
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Comentários - Integrado */}
      <EventComments eventoId={evento.id} />
    </div>
  );
}
