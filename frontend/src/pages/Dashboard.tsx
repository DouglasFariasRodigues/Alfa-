import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Users, Calendar, DollarSign, TrendingUp, UserPlus, CalendarDays } from "lucide-react";

const stats = [
  {
    title: "Total de Membros",
    value: "1,247",
    icon: Users,
    change: "+12 este mês",
    changeType: "positive"
  },
  {
    title: "Eventos este Mês",
    value: "8",
    icon: Calendar,
    change: "3 pendentes",
    changeType: "neutral"
  },
  {
    title: "Arrecadação Mensal",
    value: "R$ 45.230",
    icon: DollarSign,
    change: "+15% vs mês anterior",
    changeType: "positive"
  },
  {
    title: "Crescimento Anual",
    value: "+18%",
    icon: TrendingUp,
    change: "Meta: +20%",
    changeType: "neutral"
  }
];

const recentActivities = [
  {
    icon: UserPlus,
    title: "Novo membro cadastrado",
    description: "Maria Santos se juntou à comunidade",
    time: "2 horas atrás"
  },
  {
    icon: CalendarDays,
    title: "Evento criado",
    description: "Reunião de Oração - Quinta-feira às 19h",
    time: "5 horas atrás"
  },
  {
    icon: DollarSign,
    title: "Doação registrada",
    description: "Doação de R$ 500 para obras sociais",
    time: "1 dia atrás"
  }
];

export default function Dashboard() {
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
        {stats.map((stat) => (
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
        ))}
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
            <button className="w-full p-3 text-left rounded-lg border border-border hover:bg-accent transition-smooth">
              <div className="font-medium">Cadastrar Membro</div>
              <div className="text-sm text-muted-foreground">Adicionar novo membro à igreja</div>
            </button>
            <button className="w-full p-3 text-left rounded-lg border border-border hover:bg-accent transition-smooth">
              <div className="font-medium">Criar Evento</div>
              <div className="text-sm text-muted-foreground">Agendar nova atividade</div>
            </button>
            <button className="w-full p-3 text-left rounded-lg border border-border hover:bg-accent transition-smooth">
              <div className="font-medium">Registrar Doação</div>
              <div className="text-sm text-muted-foreground">Lançar entrada financeira</div>
            </button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}