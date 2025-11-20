import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { useToast } from "@/hooks/use-toast";
import { Search, Calendar, MapPin, Users, Clock, Check, X } from "lucide-react";
import { auth } from "@/lib/auth";

interface Evento {
  id: number;
  titulo: string;
  descricao: string;
  data: string;
  hora: string;
  local: string;
  categoria: string;
  status: string;
  capacidade: number;
  participantesConfirmados: number;
  jaConfirmei: boolean;
}

export default function EventosVisualizacao() {
  const [searchTerm, setSearchTerm] = useState("");
  const [eventos, setEventos] = useState<Evento[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  // Carregar eventos da API
  useEffect(() => {
    carregarEventos();
  }, []);

  const carregarEventos = async () => {
    try {
      const token = auth.getToken();
      if (!token) {
        toast({
          title: "Erro",
          description: "Token de autenticação não encontrado",
          variant: "destructive"
        });
        return;
      }

      const response = await fetch('http://localhost:8000/api/eventos/list/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setEventos(data.eventos);
        } else {
          toast({
            title: "Erro",
            description: data.message,
            variant: "destructive"
          });
        }
      } else {
        toast({
          title: "Erro",
          description: "Erro ao carregar eventos",
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Erro",
        description: "Erro de conexão",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const filteredEventos = eventos.filter(evento =>
    evento.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    evento.categoria.toLowerCase().includes(searchTerm.toLowerCase()) ||
    evento.local.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Confirmado": return "bg-green-100 text-green-800";
      case "Pendente": return "bg-yellow-100 text-yellow-800";
      case "Cancelado": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getCategoriaColor = (categoria: string) => {
    switch (categoria) {
      case "Culto": return "bg-blue-100 text-blue-800";
      case "Ministério": return "bg-purple-100 text-purple-800";
      case "Conferência": return "bg-orange-100 text-orange-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const confirmarPresenca = async (eventoId: number) => {
    try {
      const token = auth.getToken();
      if (!token) {
        toast({
          title: "Erro",
          description: "Token de autenticação não encontrado",
          variant: "destructive"
        });
        return;
      }

      const response = await fetch(`http://localhost:8000/api/eventos/${eventoId}/confirmar/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          // Atualizar estado do evento
          setEventos(prev =>
            prev.map(evento =>
              evento.id === eventoId
                ? {
                    ...evento,
                    jaConfirmei: data.confirmado,
                    participantesConfirmados: data.participantesConfirmados
                  }
                : evento
            )
          );

          toast({
            title: data.confirmado ? "Presença confirmada" : "Presença cancelada",
            description: data.message,
          });
        } else {
          toast({
            title: "Erro",
            description: data.message,
            variant: "destructive"
          });
        }
      } else {
        toast({
          title: "Erro",
          description: "Erro ao confirmar presença",
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Erro",
        description: "Erro de conexão",
        variant: "destructive"
      });
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Eventos</h1>
        <p className="text-muted-foreground">Visualize eventos e confirme sua participação</p>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Eventos Este Mês</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{eventos.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Minha Participação</CardTitle>
            <Check className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{eventos.filter(e => e.jaConfirmei).length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Participantes</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {eventos.reduce((acc, evento) => acc + evento.participantesConfirmados, 0)}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de Eventos */}
      <Card>
        <CardHeader>
          <CardTitle>Próximos Eventos</CardTitle>
          <CardDescription>Confira os eventos programados e confirme sua participação</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-2 mb-4">
            <div className="relative">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Buscar eventos..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8"
              />
            </div>
          </div>

          {loading ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground">Carregando eventos...</p>
            </div>
          ) : (
            <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Evento</TableHead>
                <TableHead>Data e Horário</TableHead>
                <TableHead>Local</TableHead>
                <TableHead>Categoria</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Participantes</TableHead>
                <TableHead>Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredEventos.map((evento) => (
                <TableRow key={evento.id}>
                  <TableCell className="font-medium">
                    <div>
                      <div className="font-medium flex items-center gap-2">
                        {evento.titulo}
                        {evento.jaConfirmei && (
                          <Badge className="bg-green-100 text-green-800 text-xs">
                            Confirmado
                          </Badge>
                        )}
                      </div>
                      <div className="text-sm text-muted-foreground">{evento.descricao}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center space-x-2">
                      <Calendar className="h-4 w-4 text-muted-foreground" />
                      <div>
                        <div>{new Date(evento.data).toLocaleDateString('pt-BR')}</div>
                        <div className="text-sm text-muted-foreground flex items-center">
                          <Clock className="h-3 w-3 mr-1" />
                          {evento.horario}
                        </div>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center space-x-2">
                      <MapPin className="h-4 w-4 text-muted-foreground" />
                      <span>{evento.local}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge className={getCategoriaColor(evento.categoria)}>
                      {evento.categoria}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge className={getStatusColor(evento.status)}>
                      {evento.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="text-sm">
                      <div>{evento.participantesConfirmados}/{evento.capacidade}</div>
                      <div className="text-muted-foreground">
                        {Math.round((evento.participantesConfirmados / evento.capacidade) * 100)}% ocupado
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Button
                      variant={evento.jaConfirmei ? "destructive" : "default"}
                      size="sm"
                      onClick={() => confirmarPresenca(evento.id)}
                    >
                      {evento.jaConfirmei ? (
                        <>
                          <X className="h-4 w-4 mr-2" />
                          Cancelar
                        </>
                      ) : (
                        <>
                          <Check className="h-4 w-4 mr-2" />
                          Confirmar
                        </>
                      )}
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
