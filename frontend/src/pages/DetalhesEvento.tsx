import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { ArrowLeft, Edit, Calendar, Clock, MapPin, Users, FileText } from "lucide-react";

// Mock data - substituir por dados reais do backend
const eventoMock = {
  id: 1,
  titulo: "Culto de Domingo",
  descricao: "Culto dominical com pregação e louvor especial com coral da igreja",
  data: "2024-01-07",
  hora: "10:00",
  local: "Templo Principal",
  categoria: "Culto",
  confirmados: 450,
  capacidade: 500,
  status: "Confirmado",
  observacoes: "Haverá transmissão ao vivo pelo YouTube. Confirmar equipamentos de som."
};

// Mock de participantes confirmados
const participantesMock = [
  { id: 1, nome: "Maria Santos", avatar: "" },
  { id: 2, nome: "João Silva", avatar: "" },
  { id: 3, nome: "Ana Costa", avatar: "" },
  { id: 4, nome: "Pedro Oliveira", avatar: "" },
  { id: 5, nome: "Carla Mendes", avatar: "" }
];

export default function DetalhesEvento() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [evento, setEvento] = useState(eventoMock);

  useEffect(() => {
    // Aqui carregaria os dados do evento pelo ID
    console.log("Carregando evento ID:", id);
  }, [id]);

  const handleEdit = () => {
    navigate(`/eventos/${id}/editar`);
  };

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

  const porcentagemOcupacao = Math.round((evento.confirmados / evento.capacidade) * 100);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="outline"
            onClick={() => navigate("/eventos")}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Voltar
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Detalhes do Evento</h1>
            <p className="text-muted-foreground">
              Informações completas do evento
            </p>
          </div>
        </div>
        <Button onClick={handleEdit} className="gradient-primary text-white shadow-elegant hover:opacity-90">
          <Edit className="mr-2 h-4 w-4" />
          Editar
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {/* Informações do Evento */}
        <Card className="shadow-card md:col-span-2">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="space-y-2">
                <CardTitle className="text-2xl">{evento.titulo}</CardTitle>
                <CardDescription className="text-base">{evento.descricao}</CardDescription>
              </div>
              <div className="flex gap-2">
                <Badge className={getStatusColor(evento.status)}>
                  {evento.status}
                </Badge>
                <Badge className={getCategoriaColor(evento.categoria)}>
                  {evento.categoria}
                </Badge>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <Calendar className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Data</p>
                    <p className="font-medium">
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
                  <Clock className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Horário</p>
                    <p className="font-medium">{evento.hora}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <MapPin className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Local</p>
                    <p className="font-medium">{evento.local}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Users className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Participantes</p>
                    <p className="font-medium">{evento.confirmados}/{evento.capacidade} confirmados</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Progress bar for capacity */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Taxa de Ocupação</span>
                <span className="font-medium">{porcentagemOcupacao}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="gradient-primary h-3 rounded-full transition-all"
                  style={{ width: `${porcentagemOcupacao}%` }}
                ></div>
              </div>
            </div>

            {evento.observacoes && (
              <>
                <Separator />
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <FileText className="h-4 w-4 text-muted-foreground" />
                    <p className="text-sm font-medium text-muted-foreground">Observações</p>
                  </div>
                  <p className="text-sm">{evento.observacoes}</p>
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Participantes e Ações */}
        <div className="space-y-6">
          {/* Ações Rápidas */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle>Ações</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full">
                Exportar Lista
              </Button>
              <Button variant="outline" className="w-full">
                Enviar Lembrete
              </Button>
              <Button variant="outline" className="w-full">
                Ver Relatório
              </Button>
              <Separator className="my-2" />
              <Button variant="outline" className="w-full text-destructive hover:text-destructive">
                Cancelar Evento
              </Button>
            </CardContent>
          </Card>

          {/* Participantes Recentes */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle>Confirmados Recentemente</CardTitle>
              <CardDescription>
                Últimas confirmações de presença
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {participantesMock.slice(0, 5).map((participante) => (
                <div key={participante.id} className="flex items-center space-x-3">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={participante.avatar} alt={participante.nome} />
                    <AvatarFallback className="gradient-primary text-white text-xs">
                      {participante.nome.split(' ').map(n => n[0]).join('')}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{participante.nome}</p>
                  </div>
                </div>
              ))}
              <Button variant="outline" className="w-full mt-4">
                Ver Todos ({evento.confirmados})
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}