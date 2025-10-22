import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Calendar, DollarSign, Heart, MessageCircle, CheckCircle, User, Clock } from "lucide-react";
import { usePermissions } from "@/hooks/usePermissions";
import { useEventos } from "@/hooks/useEventos";
import { useTransacoes } from "@/hooks/useTransacoes";
import { useEventPresences } from "@/hooks/useEventPresence";
import { QRCodeDonation } from "@/components/donations/QRCodeDonation";
import { toast } from 'sonner';

export default function MemberDashboard() {
  const { user } = usePermissions();
  const { data: eventos = [], isLoading: loadingEventos } = useEventos();
  const { data: transacoes = [], isLoading: loadingTransacoes } = useTransacoes();
  const { data: presencas = [] } = useEventPresences(user?.id);

  const isLoading = loadingEventos || loadingTransacoes;

  // Estatísticas para membros
  const eventosConfirmados = presencas.filter((p: any) => p.confirmado).length;
  const proximosEventos = eventos.filter((e: any) => new Date(e.data) > new Date()).slice(0, 3);
  
  // Transações do membro (simuladas - em um sistema real, você filtraria por membro)
  const doacoesMembro = [
    { tipo: 'Oferta Especial', valor: 50, data: '15/10/2024' },
    { tipo: 'Dízimo', valor: 200, data: '01/10/2024' },
    { tipo: 'Oferta', valor: 30, data: '20/09/2024' }
  ];

  const totalDoacoes = doacoesMembro.reduce((sum, doacao) => sum + doacao.valor, 0);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const handleDonation = (amount: number, method: string) => {
    toast.success(`Doação de R$ ${amount.toFixed(2)} via ${method.toUpperCase()} realizada!`);
    // Aqui você implementaria a lógica real de doação
  };

  if (isLoading) {
    return (
      <div className="p-6 space-y-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Bem-vindo, {user?.nome}!</h1>
        <p className="text-muted-foreground">
          Sua área pessoal na Igreja Central - {new Date().toLocaleDateString('pt-BR', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}
        </p>
      </div>

      {/* Estatísticas Pessoais */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Eventos Confirmados</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{eventosConfirmados}</div>
            <p className="text-xs text-muted-foreground">
              Presenças confirmadas
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Doações</CardTitle>
            <Heart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">R$ {totalDoacoes.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">
              Este ano
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Próximos Eventos</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{proximosEventos.length}</div>
            <p className="text-xs text-muted-foreground">
              Eventos programados
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Status</CardTitle>
            <User className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <Badge className="bg-green-100 text-green-800">
              Membro Ativo
            </Badge>
            <p className="text-xs text-muted-foreground mt-1">
              Desde {formatDate(user?.created_at || '')}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Ações Rápidas */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Doações */}
        <QRCodeDonation onDonate={handleDonation} />
        
        {/* Próximos Eventos */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5 text-primary" />
              Próximos Eventos
            </CardTitle>
            <CardDescription>
              Eventos que você pode participar
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {proximosEventos.length === 0 ? (
                <p className="text-muted-foreground text-center py-4">
                  Nenhum evento programado
                </p>
              ) : (
                proximosEventos.map((evento: any) => (
                  <div key={evento.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <p className="font-medium">{evento.titulo}</p>
                      <p className="text-sm text-muted-foreground">
                        {formatDate(evento.data)}
                      </p>
                    </div>
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={() => window.location.href = `/eventos/${evento.id}`}
                    >
                      Ver Detalhes
                    </Button>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Histórico de Doações */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <DollarSign className="h-5 w-5 text-primary" />
            Suas Doações
          </CardTitle>
          <CardDescription>
            Histórico das suas contribuições
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {doacoesMembro.map((doacao, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div>
                  <p className="font-medium text-green-800">{doacao.tipo}</p>
                  <p className="text-sm text-green-600">{doacao.data}</p>
                </div>
                <Badge className="bg-green-100 text-green-800">
                  R$ {doacao.valor.toFixed(2)}
                </Badge>
              </div>
            ))}
            
            <div className="text-center py-4 border-t">
              <p className="text-sm text-muted-foreground">
                Total doado este ano: <span className="font-semibold text-green-600">R$ {totalDoacoes.toFixed(2)}</span>
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Ações Rápidas */}
      <Card>
        <CardHeader>
          <CardTitle>Ações Rápidas</CardTitle>
          <CardDescription>
            Acesso rápido às principais funcionalidades
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <Button 
              variant="outline" 
              className="h-20 flex-col gap-2"
              onClick={() => window.location.href = '/eventos-membro'}
            >
              <Calendar className="h-6 w-6" />
              Ver Eventos
            </Button>
            
            <Button 
              variant="outline" 
              className="h-20 flex-col gap-2"
              onClick={() => window.location.href = '/financas'}
            >
              <DollarSign className="h-6 w-6" />
              Finanças
            </Button>
            
            <Button 
              variant="outline" 
              className="h-20 flex-col gap-2"
              onClick={() => window.location.href = '/configuracoes'}
            >
              <User className="h-6 w-6" />
              Perfil
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
