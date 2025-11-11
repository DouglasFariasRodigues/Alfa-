import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Calendar, Clock, MapPin, Users, Plus, Filter, Loader2, Eye, CheckCircle, Trash2, Download } from "lucide-react";
import { Input } from "@/components/ui/input";
import { useEventos, useDeleteEvento } from "@/hooks/useEventos";
import { usePermissions } from "@/hooks/usePermissions";
import { useConfirmPresence, useEventPresences } from "@/hooks/useEventPresence";
import { toast } from "sonner";

export default function Eventos() {
  const [searchTerm, setSearchTerm] = useState("");

  // Buscar eventos da API
  const { data: eventos = [], isLoading, error } = useEventos({ 
    search: searchTerm || undefined 
  });
  
  const deleteEventoMutation = useDeleteEvento();
  const confirmPresenceMutation = useConfirmPresence();
  const { canManage, user } = usePermissions();
  
  // Buscar confirmações de presença do membro
  const { data: presencas = [] } = useEventPresences(user?.id);
  
  // Verificar se o usuário pode gerenciar eventos (criar, editar, deletar)
  const canManageEvents = canManage('eventos');

  // Função para verificar se o membro já confirmou presença em um evento
  const isPresenceConfirmed = (eventoId: number) => {
    return presencas.some((presenca: any) => presenca.evento === eventoId && presenca.confirmado);
  };

  const handleDeleteEvento = async (id: number) => {
    if (window.confirm('Tem certeza que deseja excluir este evento?')) {
      try {
        await deleteEventoMutation.mutateAsync(id);
        toast.success('Evento excluído com sucesso!');
      } catch (error) {
        toast.error('Erro ao excluir evento');
      }
    }
  };

  const handleGerarRelatorio = async () => {
    try {
      // Gerar relatório PDF de eventos
      const dataInicio = new Date();
      dataInicio.setMonth(dataInicio.getMonth() - 1);
      const dataFim = new Date();
      
      const params = new URLSearchParams({
        data_inicio: dataInicio.toISOString().split('T')[0],
        data_fim: dataFim.toISOString().split('T')[0]
      });
      
      // Fazer requisição para o backend
      const response = await fetch(`http://127.0.0.1:8000/api/relatorios/eventos/pdf/?${params}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });
      
      if (response.ok) {
        // Criar blob e download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `relatorio_eventos_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        toast.success('Relatório gerado com sucesso!');
      } else {
        toast.error('Erro ao gerar relatório');
      }
    } catch (error) {
      console.error('Erro ao gerar relatório:', error);
      toast.error('Erro ao gerar relatório');
    }
  };

  const handleConfirmPresence = async (eventoId: number) => {
    if (!user) {
      toast.error('Usuário não encontrado');
      return;
    }

    try {
      await confirmPresenceMutation.mutateAsync({
        evento: eventoId,
        membro: user.id,
        confirmado: true,
        observacoes: 'Presença confirmada pelo membro'
      });
      toast.success('Presença confirmada com sucesso!');
    } catch (error) {
      toast.error('Erro ao confirmar presença');
      console.error('Erro ao confirmar presença:', error);
    }
  };

  // Calcular estatísticas
  const totalEventos = eventos.length;
  const eventosEsteMes = eventos.filter(e => {
    const dataEvento = new Date(e.data);
    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    return dataEvento.getMonth() === currentMonth && dataEvento.getFullYear() === currentYear;
  }).length;

  // Próximo evento
  const agora = new Date();
  const proximosEventos = eventos
    .filter(e => new Date(e.data) > agora)
    .sort((a, b) => new Date(a.data).getTime() - new Date(b.data).getTime());
  
  const proximoEvento = proximosEventos[0];
  const diasParaProximo = proximoEvento 
    ? Math.ceil((new Date(proximoEvento.data).getTime() - agora.getTime()) / (1000 * 60 * 60 * 24))
    : 0;

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

  const getCategoriaColor = (categoria: string) => {
    switch (categoria) {
      case "Culto":
        return "gradient-primary text-white";
      case "Oração":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200";
      case "Retiro":
        return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200";
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Eventos</h1>
          <p className="text-muted-foreground">
            Gerencie os eventos e atividades da sua igreja
          </p>
        </div>
        <div className="flex gap-2">
          <Button 
            onClick={handleGerarRelatorio}
            variant="outline"
            className="border-blue-200 text-blue-600 hover:bg-blue-50"
          >
            <Download className="mr-2 h-4 w-4" />
            Relatório
          </Button>
          {canManageEvents && (
            <Button 
              onClick={() => window.location.href = '/eventos/novo'}
              className="gradient-primary text-white shadow-elegant hover:opacity-90"
            >
              <Plus className="mr-2 h-4 w-4" />
              Novo Evento
            </Button>
          )}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total de Eventos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalEventos}</div>
            <p className="text-xs text-green-600">{eventosEsteMes} este mês</p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Eventos Este Mês</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{eventosEsteMes}</div>
            <p className="text-xs text-muted-foreground">Programados</p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Próximos Eventos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{proximosEventos.length}</div>
            <p className="text-xs text-green-600">Agendados</p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Próximo Evento</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{diasParaProximo}</div>
            <p className="text-xs text-muted-foreground">dias</p>
          </CardContent>
        </Card>
      </div>

      {/* Search and Filter */}
      <Card className="shadow-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Próximos Eventos</CardTitle>
              <CardDescription>
                Visualize e gerencie todos os eventos programados
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <div className="relative">
                <Input
                  placeholder="Buscar eventos..."
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
              <span className="ml-2">Carregando eventos...</span>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-2">
              {eventos.length === 0 ? (
                <div className="col-span-full text-center py-12">
                  <div className="text-muted-foreground">
                    <Calendar className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p className="text-lg font-medium">Nenhum evento encontrado</p>
                    <p className="text-sm">Não há eventos cadastrados no momento</p>
                  </div>
                </div>
              ) : (
                eventos.map((evento) => (
              <Card key={evento.id} className="shadow-card hover:shadow-elegant transition-all duration-300 hover:-translate-y-1 h-full">
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="space-y-2 flex-1 min-w-0">
                      <CardTitle className="text-xl leading-tight">{evento.titulo}</CardTitle>
                      {evento.descricao && (
                        <CardDescription className="text-sm leading-relaxed">{evento.descricao}</CardDescription>
                      )}
                    </div>
                    <Badge className={getStatusColor(evento.status)} variant="secondary">
                      {evento.status}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-5 flex-1">
                  <div className="grid grid-cols-1 gap-4">
                    <div className="flex items-center gap-3 text-sm">
                      <Calendar className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                      <span className="font-medium">{new Date(evento.data).toLocaleDateString('pt-BR', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}</span>
                    </div>
                    <div className="flex items-center gap-3 text-sm">
                      <Clock className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                      <span className="font-medium">{new Date(evento.data).toLocaleTimeString('pt-BR', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}</span>
                    </div>
                    <div className="flex items-center gap-3 text-sm">
                      <MapPin className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                      <span className="font-medium">{evento.local || 'Local não informado'}</span>
                    </div>
                    <div className="flex items-center gap-3 text-sm">
                      <Users className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                      <span className="font-medium">Organizado por: {evento.organizador_nome}</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t">
                    <Badge variant="outline" className="text-sm">
                      Evento
                    </Badge>
                    <div className="flex gap-3">
                      {canManageEvents ? (
                        <>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => window.location.href = `/eventos/${evento.id}/editar`}
                          >
                            Editar
                          </Button>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => window.location.href = `/eventos/${evento.id}`}
                          >
                            <Eye className="mr-2 h-4 w-4" />
                            Ver Detalhes
                          </Button>
                          <Button 
                            variant="outline" 
                            size="sm"
                            className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200"
                            onClick={() => handleDeleteEvento(evento.id)}
                            disabled={deleteEventoMutation.isPending}
                          >
                            {deleteEventoMutation.isPending ? (
                              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            ) : (
                              <Trash2 className="mr-2 h-4 w-4" />
                            )}
                            Remover
                          </Button>
                        </>
                      ) : (
                        <>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => window.location.href = `/eventos/${evento.id}`}
                          >
                            <Eye className="mr-2 h-4 w-4" />
                            Ver Detalhes
                          </Button>
                          {isPresenceConfirmed(evento.id) ? (
                            <Button 
                              variant="outline" 
                              size="sm"
                              className="border-green-500 text-green-600 bg-green-50"
                              disabled
                            >
                              <CheckCircle className="mr-2 h-4 w-4" />
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
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                              ) : (
                                <CheckCircle className="mr-2 h-4 w-4" />
                              )}
                              Confirmar Presença
                            </Button>
                          )}
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

      {/* Seção de Status de Presença para Membros */}
      {!canManageEvents && user && (
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
                <CheckCircle className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <p className="text-muted-foreground">Você ainda não confirmou presença em nenhum evento</p>
                <p className="text-sm text-muted-foreground mt-2">
                  Confirme sua presença nos eventos acima para aparecer aqui
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {presencas.map((presenca: any) => {
                  const evento = eventos.find(e => e.id === presenca.evento);
                  if (!evento) return null;
                  
                  return (
                    <div key={presenca.id} className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200">
                      <div>
                        <p className="font-medium text-green-800">{evento.titulo}</p>
                        <p className="text-sm text-green-600">
                          {new Date(evento.data).toLocaleDateString('pt-BR')} às {evento.hora}
                        </p>
                      </div>
                      <Badge className="bg-green-100 text-green-800">
                        Confirmado
                      </Badge>
                    </div>
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