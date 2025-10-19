import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Edit, Calendar, Clock, MapPin, User, FileText } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { useEvento } from '@/hooks/useEventos'
import { Skeleton } from '@/components/ui/skeleton'

export default function DetalhesEvento() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  
  const { data: evento, isLoading, error } = useEvento(Number(id))

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
        <div className="grid gap-6 md:grid-cols-2">
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
          <Card>
            <CardHeader>
              <Skeleton className="h-6 w-32" />
            </CardHeader>
            <CardContent className="space-y-4">
              <Skeleton className="h-6 w-24" />
              <Skeleton className="h-6 w-24" />
              <Skeleton className="h-6 w-24" />
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  if (error || !evento) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate('/eventos')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Evento não encontrado</h1>
            <p className="text-muted-foreground">
              O evento solicitado não foi encontrado ou não existe.
            </p>
          </div>
        </div>
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-muted-foreground mb-4">
                Verifique se o ID do evento está correto.
              </p>
              <Button onClick={() => navigate('/eventos')}>
                Voltar para Eventos
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const formatDate = (dateString: string) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }

  const formatTime = (dateString: string) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleTimeString('pt-BR', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const formatDateTime = (dateString: string) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const isEventPast = (dateString: string) => {
    if (!dateString) return false
    return new Date(dateString) < new Date()
  }

  const getEventStatus = (dateString: string) => {
    if (!dateString) return { label: 'Data não definida', color: 'bg-gray-100 text-gray-800' }
    
    const eventDate = new Date(dateString)
    const now = new Date()
    const diffTime = eventDate.getTime() - now.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays < 0) {
      return { label: 'Realizado', color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' }
    } else if (diffDays === 0) {
      return { label: 'Hoje', color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300' }
    } else if (diffDays === 1) {
      return { label: 'Amanhã', color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300' }
    } else if (diffDays <= 7) {
      return { label: 'Esta semana', color: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300' }
    } else {
      return { label: 'Futuro', color: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300' }
    }
  }

  const eventStatus = getEventStatus(evento.data)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate('/eventos')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{evento.titulo}</h1>
            <p className="text-muted-foreground">
              Detalhes e informações do evento
            </p>
          </div>
        </div>
        <Button onClick={() => navigate(`/eventos/${evento.id}/editar`)}>
          <Edit className="h-4 w-4 mr-2" />
          Editar Evento
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Informações do Evento */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Informações do Evento
            </CardTitle>
            <CardDescription>
              Dados principais do evento
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4">
              <div>
                <h3 className="text-lg font-semibold">{evento.titulo}</h3>
                <Badge className={eventStatus.color}>
                  {eventStatus.label}
                </Badge>
              </div>
            </div>
            
            <Separator />
            
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Data</p>
                  <p className="text-sm text-muted-foreground">{formatDate(evento.data)}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <Clock className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Hora</p>
                  <p className="text-sm text-muted-foreground">{formatTime(evento.data)}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <MapPin className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Local</p>
                  <p className="text-sm text-muted-foreground">{evento.local || '-'}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <User className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Organizador</p>
                  <p className="text-sm text-muted-foreground">{evento.organizador_nome || '-'}</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Descrição e Detalhes */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Descrição
            </CardTitle>
            <CardDescription>
              Detalhes sobre o evento
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-sm text-muted-foreground mb-2">Descrição</h4>
                <p className="text-sm">
                  {evento.descricao || 'Nenhuma descrição disponível.'}
                </p>
              </div>
              
              {evento.observacoes && (
                <div>
                  <h4 className="font-medium text-sm text-muted-foreground mb-2">Observações</h4>
                  <p className="text-sm">
                    {evento.observacoes}
                  </p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Estatísticas */}
      <Card>
        <CardHeader>
          <CardTitle>Informações Adicionais</CardTitle>
          <CardDescription>
            Dados sobre o evento
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <Calendar className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">
                {formatDateTime(evento.data)}
              </p>
              <p className="text-sm text-muted-foreground">Data e hora</p>
            </div>
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <User className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">
                {evento.organizador_nome || '-'}
              </p>
              <p className="text-sm text-muted-foreground">Organizador</p>
            </div>
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <MapPin className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">
                {evento.local ? 'Definido' : 'Não definido'}
              </p>
              <p className="text-sm text-muted-foreground">Local</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Ações */}
      <Card>
        <CardHeader>
          <CardTitle>Ações</CardTitle>
          <CardDescription>
            Opções disponíveis para este evento
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-3">
            <Button onClick={() => navigate(`/eventos/${evento.id}/editar`)}>
              <Edit className="h-4 w-4 mr-2" />
              Editar Evento
            </Button>
            <Button variant="outline" onClick={() => navigate('/eventos')}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar para Eventos
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}