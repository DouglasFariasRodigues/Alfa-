import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Users, Calendar, DollarSign, TrendingUp, UserPlus, CalendarDays, Loader2 } from "lucide-react";
import { useMembros } from "@/hooks/useMembros";
import { useEventos } from "@/hooks/useEventos";
import { useTransacoes } from "@/hooks/useTransacoes";

export default function Dashboard() {
  // Buscar dados da API
  const { data: membros = [], isLoading: loadingMembros } = useMembros();
  const { data: eventos = [], isLoading: loadingEventos } = useEventos();
  const { data: transacoes = [], isLoading: loadingTransacoes } = useTransacoes();

  const isLoading = loadingMembros || loadingEventos || loadingTransacoes;

  // Calcular estatísticas
  const totalMembros = membros.length;
  const membrosAtivos = membros.filter(m => m.status === 'ativo').length;
  
  const currentMonth = new Date().getMonth();
  const currentYear = new Date().getFullYear();
  const novosMembrosEsteMes = membros.filter(m => {
    const dataCadastro = new Date(m.created_at);
    return dataCadastro.getMonth() === currentMonth && dataCadastro.getFullYear() === currentYear;
  }).length;

  const eventosEsteMes = eventos.filter(e => {
    const dataEvento = new Date(e.data);
    return dataEvento.getMonth() === currentMonth && dataEvento.getFullYear() === currentYear;
  }).length;

  const arrecadacaoMensal = transacoes
    .filter(t => t.tipo === 'entrada')
    .filter(t => {
      const dataTransacao = new Date(t.data);
      return dataTransacao.getMonth() === currentMonth && dataTransacao.getFullYear() === currentYear;
    })
    .reduce((sum, t) => sum + parseFloat(t.valor.toString()), 0);

  const crescimentoAnual = totalMembros > 0 ? Math.round((membrosAtivos / totalMembros) * 100) : 0;

  const stats = [
    {
      title: "Total de Membros",
      value: totalMembros.toString(),
      icon: Users,
      change: `+${novosMembrosEsteMes} este mês`,
      changeType: "positive"
    },
    {
      title: "Eventos este Mês",
      value: eventosEsteMes.toString(),
      icon: Calendar,
      change: `${eventos.length} total`,
      changeType: "neutral"
    },
    {
      title: "Arrecadação Mensal",
      value: `R$ ${arrecadacaoMensal.toLocaleString('pt-BR')}`,
      icon: DollarSign,
      change: `${transacoes.filter(t => t.tipo === 'entrada').length} transações`,
      changeType: "positive"
    },
    {
      title: "Membros Ativos",
      value: `${crescimentoAnual}%`,
      icon: TrendingUp,
      change: `${membrosAtivos} de ${totalMembros}`,
      changeType: "neutral"
    }
  ];

  // Atividades recentes baseadas nos dados reais
  const recentActivities = [
    ...(membros.length > 0 ? [{
      icon: UserPlus,
      title: "Membros cadastrados",
      description: `${totalMembros} membros no total`,
      time: "Dados atualizados"
    }] : []),
    ...(eventos.length > 0 ? [{
      icon: CalendarDays,
      title: "Eventos programados",
      description: `${eventos.length} eventos cadastrados`,
      time: "Dados atualizados"
    }] : []),
    ...(transacoes.length > 0 ? [{
      icon: DollarSign,
      title: "Transações registradas",
      description: `${transacoes.length} movimentações financeiras`,
      time: "Dados atualizados"
    }] : [])
  ];
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Visão geral da Igreja Central - {new Date().toLocaleDateString('pt-BR', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {isLoading ? (
          Array.from({ length: 4 }).map((_, index) => (
            <Card key={index} className="shadow-card">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div className="h-4 w-24 bg-gray-200 rounded animate-pulse"></div>
                <div className="h-4 w-4 bg-gray-200 rounded animate-pulse"></div>
              </CardHeader>
              <CardContent>
                <div className="h-8 w-16 bg-gray-200 rounded animate-pulse mb-2"></div>
                <div className="h-3 w-20 bg-gray-200 rounded animate-pulse"></div>
              </CardContent>
            </Card>
          ))
        ) : (
          stats.map((stat) => (
            <Card key={stat.title} className="shadow-card transition-smooth hover:shadow-elegant">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                <stat.icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className={`text-xs ${
                  stat.changeType === 'positive' ? 'text-green-600' : 
                  stat.changeType === 'negative' ? 'text-red-600' : 
                  'text-muted-foreground'
                }`}>
                  {stat.change}
                </p>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Main Content Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Recent Activities */}
        <Card className="lg:col-span-2 shadow-card">
          <CardHeader>
            <CardTitle>Atividades Recentes</CardTitle>
            <CardDescription>
              Últimas movimentações no sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-4">
                {Array.from({ length: 3 }).map((_, index) => (
                  <div key={index} className="flex items-start space-x-4 p-3 rounded-lg">
                    <div className="h-8 w-8 bg-gray-200 rounded-full animate-pulse"></div>
                    <div className="flex-1 space-y-2">
                      <div className="h-4 w-32 bg-gray-200 rounded animate-pulse"></div>
                      <div className="h-3 w-48 bg-gray-200 rounded animate-pulse"></div>
                      <div className="h-3 w-20 bg-gray-200 rounded animate-pulse"></div>
                    </div>
                  </div>
                ))}
              </div>
            ) : recentActivities.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-muted-foreground">Nenhuma atividade recente</p>
              </div>
            ) : (
              <div className="space-y-4">
                {recentActivities.map((activity, index) => (
                  <div key={index} className="flex items-start space-x-4 p-3 rounded-lg hover:bg-accent/50 transition-smooth">
                    <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                      <activity.icon className="h-4 w-4 text-primary" />
                    </div>
                    <div className="flex-1 space-y-1">
                      <p className="text-sm font-medium">{activity.title}</p>
                      <p className="text-sm text-muted-foreground">{activity.description}</p>
                      <p className="text-xs text-muted-foreground">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle>Ações Rápidas</CardTitle>
            <CardDescription>
              Acesso direto às principais funcionalidades
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <button 
              onClick={() => window.location.href = '/membros/novo'}
              className="w-full p-3 text-left rounded-lg border border-border hover:bg-accent transition-smooth"
            >
              <div className="font-medium">Cadastrar Membro</div>
              <div className="text-sm text-muted-foreground">Adicionar novo membro à igreja</div>
            </button>
            <button 
              onClick={() => window.location.href = '/eventos/novo'}
              className="w-full p-3 text-left rounded-lg border border-border hover:bg-accent transition-smooth"
            >
              <div className="font-medium">Criar Evento</div>
              <div className="text-sm text-muted-foreground">Agendar nova atividade</div>
            </button>
            <button 
              onClick={() => window.location.href = '/financas/nova-transacao'}
              className="w-full p-3 text-left rounded-lg border border-border hover:bg-accent transition-smooth"
            >
              <div className="font-medium">Registrar Transação</div>
              <div className="text-sm text-muted-foreground">Lançar entrada ou saída financeira</div>
            </button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}