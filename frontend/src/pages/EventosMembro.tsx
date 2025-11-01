import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Calendar, Clock, MapPin, Users, Filter, Loader2, Eye, CheckCircle, MessageCircle, Heart } from "lucide-react";
import { Input } from "@/components/ui/input";
import { useEventos, useDeleteEvento } from "@/hooks/useEventos";
import { usePermissions } from "@/hooks/usePermissions";
import { useConfirmPresence, useEventPresences } from "@/hooks/useEventPresence";
import { toast } from "sonner";

export default function EventosMembro() {
  const [searchTerm, setSearchTerm] = useState("");

  // Buscar eventos da API
  const { data: eventos = [], isLoading, error } = useEventos({ 
    search: searchTerm || undefined 
  });
  
  const confirmPresenceMutation = useConfirmPresence();
  const { user } = usePermissions();
  
  // Buscar confirmações de presença do membro
  const { data: presencas = [] } = useEventPresences(user?.id);
  
  // Função para verificar se o membro já confirmou presença em um evento
  const isPresenceConfirmed = (eventoId: number) => {
    return presencas.some((presenca: any) => presenca.evento === eventoId && presenca.confirmado);
  };

  const handleConfirmPresence = async (eventoId: number) => {
    try {
      await confirmPresenceMutation.mutateAsync({
        evento: eventoId,
        membro: user?.id,
        confirmado: true
      });
      toast.success('Presença confirmada com sucesso!');
    } catch (error) {
      toast.error('Erro ao confirmar presença');
      console.error('Erro ao confirmar presença:', error);
    }
  };

  // Calcular estatísticas para membros
  const totalEventos = eventos.length;
  const eventosConfirmados = presencas.filter((p: any) => p.confirmado).length;
  const proximosEventos = eventos.filter(e => new Date(e.data) > new Date()).length;

  if (error) {
    return (
      <div className="p-6">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-600">Erro ao carregar eventos</h2>
          <p className="text-gray-600">Tente recarregar a página</p>
        </div>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Confirmado":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "Planejamento":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      case "Cancelado":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200";
    }
  };

  const getEventStatus = (data: string) => {
    const agora = new Date();
    const dataEvento = new Date(data);
    const diffTime = dataEvento.getTime() - agora.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) return "Passado";
    if (diffDays === 0) return "Hoje";
    if (diffDays === 1) return "Amanhã";
    if (diffDays <= 7) return "Esta semana";
    return "Futuro";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Eventos</h1>
          <p className="text-muted-foreground">
            Participe dos eventos da nossa igreja
          </p>
        </div>
      </div>

      {/* Estatísticas para Membros */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="shadow-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Eventos</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalEventos}</div>
            <p className="text-xs text-muted-foreground">
              Eventos disponíveis
            </p>
          </CardContent>
        </Card>

        <Card className="shadow-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Presenças Confirmadas</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{eventosConfirmados}</div>
            <p className="text-xs text-muted-foreground">
              Eventos que você confirmou
            </p>
          </CardContent>
        </Card>

        <Card className="shadow-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Próximos Eventos</CardTitle>
            <Clock className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{proximosEventos}</div>
            <p className="text-xs text-muted-foreground">
              Eventos futuros
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Lista de Eventos */}
      <Card className="shadow-card">
        <CardHeader>
          <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5 text-primary" />
                Próximos Eventos
              </CardTitle>
              <CardDescription>
                Confirme sua presença e participe dos eventos
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Input
                placeholder="Buscar eventos..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-64"
              />
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
              <span className="ml-2">Carregando eventos...</span>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {eventos.length === 0 ? (
                <div className="col-span-full text-center py-8">
                  <p className="text-muted-foreground">Nenhum evento encontrado</p>
                </div>
              ) : (
                eventos.map((evento) => (
              <Card key={evento.id} className="shadow-card hover:shadow-elegant transition-smooth">
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <CardTitle className="text-lg">{evento.titulo}</CardTitle>
                      <CardDescription>{evento.descricao}</CardDescription>
                    </div>
                    <Badge className={getStatusColor(evento.status)}>
                      {evento.status}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm">
                      <Calendar className="h-4 w-4 text-muted-foreground" />
                      <span>{new Date(evento.data).toLocaleDateString('pt-BR', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <Clock className="h-4 w-4 text-muted-foreground" />
                      <span>{new Date(evento.data).toLocaleTimeString('pt-BR', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <MapPin className="h-4 w-4 text-muted-foreground" />
                      <span>{evento.local || 'Local não informado'}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <Users className="h-4 w-4 text-muted-foreground" />
                      <span>Organizado por: {evento.organizador_nome}</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <Badge className="gradient-primary text-white">
                      {getEventStatus(evento.data)}
                    </Badge>
                    <div className="flex gap-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => window.location.href = `/eventos/${evento.id}/membro`}
                      >
                        <Eye className="mr-1 h-3 w-3" />
                        Ver Detalhes
                      </Button>
                      {isPresenceConfirmed(evento.id) ? (
                        <Button 
                          variant="outline" 
                          size="sm"
                          className="border-green-500 text-green-600 bg-green-50"
                          disabled
                        >
                          <CheckCircle className="mr-1 h-3 w-3" />
                          Presença Confirmada
                        </Button>
                      ) : (
                        <Button 
                          variant="default" 
                          size="sm"
                          className="bg-green-600 hover:bg-green-700"
                          onClick={() => handleConfirmPresence(evento.id)}
                          disabled={confirmPresenceMutation.isPending}
                        >
                          {confirmPresenceMutation.isPending ? (
                            <Loader2 className="mr-1 h-3 w-3 animate-spin" />
                          ) : (
                            <CheckCircle className="mr-1 h-3 w-3" />
                          )}
                          Confirmar Presença
                        </Button>
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

      {/* Seção de Status de Presença para Membros */}
      {user && (
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              Minhas Confirmações de Presença
            </CardTitle>
            <CardDescription>
              Eventos em que você confirmou presença
            </CardDescription>
          </CardHeader>
          <CardContent>
            {presencas.length === 0 ? (
              <div className="text-center py-8">
                <CheckCircle className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">Você ainda não confirmou presença em nenhum evento</p>
                <p className="text-sm text-muted-foreground mt-2">
                  Confirme sua presença nos eventos acima para vê-los aqui
                </p>
              </div>
            ) : (
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {presencas
                  .filter((presenca: any) => presenca.confirmado)
                  .map((presenca: any) => {
                    const evento = eventos.find((e: any) => e.id === presenca.evento);
                    if (!evento) return null;
                    
                    return (
                      <Card key={presenca.id} className="border-green-200 bg-green-50">
                        <CardHeader className="pb-3">
                          <div className="flex items-center justify-between">
                            <CardTitle className="text-lg text-green-800">{evento.titulo}</CardTitle>
                            <Badge className="bg-green-600 text-white">
                              <CheckCircle className="mr-1 h-3 w-3" />
                              Confirmado
                            </Badge>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-2 text-sm">
                            <div className="flex items-center gap-2">
                              <Calendar className="h-4 w-4 text-green-600" />
                              <span className="text-green-700">
                                {new Date(evento.data).toLocaleDateString('pt-BR')}
                              </span>
                            </div>
                            <div className="flex items-center gap-2">
                              <Clock className="h-4 w-4 text-green-600" />
                              <span className="text-green-700">
                                {new Date(evento.data).toLocaleTimeString('pt-BR', {
                                  hour: '2-digit',
                                  minute: '2-digit'
                                })}
                              </span>
                            </div>
                            <div className="flex items-center gap-2">
                              <MapPin className="h-4 w-4 text-green-600" />
                              <span className="text-green-700">{evento.local || 'Local não informado'}</span>
                            </div>
                          </div>
                          <div className="mt-4">
                            <Button 
                              variant="outline" 
                              size="sm"
                              className="w-full border-green-300 text-green-700 hover:bg-green-100"
                              onClick={() => window.location.href = `/eventos/${evento.id}/membro`}
                            >
                              <Eye className="mr-1 h-3 w-3" />
                              Ver Detalhes
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    );
                  })}
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
