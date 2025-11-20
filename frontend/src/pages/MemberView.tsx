import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Users, UserCheck, UserX, Clock, CalendarDays } from "lucide-react";
import { auth } from "@/lib/auth";
import { useNavigate } from "react-router-dom";

const memberStats = [
  {
    title: "Total de Membros",
    value: "1,247",
    icon: Users,
    change: "Comunidade ativa",
    changeType: "positive"
  },
  {
    title: "Membros Ativos",
    value: "1,089",
    icon: UserCheck,
    change: "87% da comunidade",
    changeType: "positive"
  },
  {
    title: "Membros Inativos",
    value: "158",
    icon: UserX,
    change: "13% da comunidade",
    changeType: "neutral"
  },
  {
    title: "Registrados Recentemente",
    value: "23",
    icon: Clock,
    change: "Últimos 30 dias",
    changeType: "positive"
  }
];

const upcomingEvents = [
  {
    title: "Reunião de Oração",
    date: "Quinta-feira, 19h",
    location: "Salão Principal"
  },
  {
    title: "Culto de Domingo",
    date: "Domingo, 10h",
    location: "Templo Central"
  },
  {
    title: "Estudo Bíblico",
    date: "Terça-feira, 20h",
    location: "Sala de Estudos"
  }
];

const recentPosts = [
  {
    title: "Mensagem do Pastor",
    excerpt: "Reflexões sobre fé e perseverança...",
    date: "2 dias atrás"
  },
  {
    title: "Anúncios da Semana",
    excerpt: "Atualizações sobre eventos e atividades...",
    date: "4 dias atrás"
  },
  {
    title: "Testemunho de Fé",
    excerpt: "História inspiradora de transformação...",
    date: "1 semana atrás"
  }
];

export default function MemberView() {
  const navigate = useNavigate();

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Comunidade</h1>
        <p className="text-muted-foreground">
          Conheça nossa comunidade e participe dos eventos
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {memberStats.map((stat) => (
          <Card key={stat.title} className="shadow-card">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
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

      {/* Member Dashboard for non-admin users */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Upcoming Events */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle>Próximos Eventos</CardTitle>
            <CardDescription>
              Eventos programados para os próximos dias
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {upcomingEvents.map((event, index) => (
                <div key={index} className="flex items-start space-x-4 p-3 rounded-lg hover:bg-accent/50 transition-smooth cursor-pointer" onClick={() => navigate('/eventos')}>
                  <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                    <CalendarDays className="h-4 w-4 text-primary" />
                  </div>
                  <div className="flex-1 space-y-1">
                    <p className="text-sm font-medium">{event.title}</p>
                    <p className="text-sm text-muted-foreground">{event.date}</p>
                    <p className="text-xs text-muted-foreground">{event.location}</p>
                  </div>
                </div>
              ))}
            </div>
            <button
              className="w-full mt-4 p-2 text-sm text-primary hover:underline"
              onClick={() => navigate('/eventos')}
            >
              Ver todos os eventos →
            </button>
          </CardContent>
        </Card>

        {/* Recent Posts */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle>Postagens Recentes</CardTitle>
            <CardDescription>
              Últimas mensagens e anúncios
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentPosts.map((post, index) => (
                <div key={index} className="p-3 rounded-lg hover:bg-accent/50 transition-smooth cursor-pointer" onClick={() => navigate('/posts')}>
                  <p className="text-sm font-medium">{post.title}</p>
                  <p className="text-sm text-muted-foreground line-clamp-2">{post.excerpt}</p>
                  <p className="text-xs text-muted-foreground mt-1">{post.date}</p>
                </div>
              ))}
            </div>
            <button
              className="w-full mt-4 p-2 text-sm text-primary hover:underline"
              onClick={() => navigate('/posts')}
            >
              Ver todas as postagens →
            </button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
