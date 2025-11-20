import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Search, Plus, Filter, MoreHorizontal, Phone, Mail, MapPin, Users, UserCheck, UserX, Clock, CalendarDays } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { auth } from "@/lib/auth";
import { useNavigate } from "react-router-dom";

const membros = [
  {
    id: 1,
    nome: "Maria Santos",
    email: "maria.santos@email.com",
    telefone: "(11) 99999-9999",
    endereco: "São Paulo, SP",
    status: "Ativo",
    dataCadastro: "2023-01-15",
    cargo: "Membro"
  },
  {
    id: 2,
    nome: "João Silva",
    email: "joao.silva@email.com",
    telefone: "(11) 98888-8888",
    endereco: "São Paulo, SP",
    status: "Ativo",
    dataCadastro: "2022-08-20",
    cargo: "Diácono"
  },
  {
    id: 3,
    nome: "Ana Costa",
    email: "ana.costa@email.com",
    telefone: "(11) 97777-7777",
    endereco: "São Paulo, SP",
    status: "Inativo",
    dataCadastro: "2023-03-10",
    cargo: "Membro"
  }
];

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

export default function Membros() {
  const [searchTerm, setSearchTerm] = useState("");
  const userType = auth.getUserType();
  const navigate = useNavigate();

  const filteredMembros = membros.filter(membro =>
    membro.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    membro.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Membros</h1>
          <p className="text-muted-foreground">
            Gerencie os membros da sua comunidade
          </p>
        </div>
        {userType === 'admin' && (
          <Button
            onClick={() => window.location.href = '/membros/novo'}
            className="gradient-primary text-white shadow-elegant hover:opacity-90"
          >
            <Plus className="mr-2 h-4 w-4" />
            Novo Membro
          </Button>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        {(userType === 'admin' ? [
          {
            title: "Total de Membros",
            value: "1,247",
            icon: Users,
            change: "+12 este mês",
            changeType: "positive"
          },
          {
            title: "Membros Ativos",
            value: "1,198",
            icon: UserCheck,
            change: "96% do total",
            changeType: "positive"
          },
          {
            title: "Novos este Mês",
            value: "12",
            icon: Clock,
            change: "+8% vs mês anterior",
            changeType: "positive"
          },
          {
            title: "Aniversariantes",
            value: "8",
            icon: CalendarDays,
            change: "Este mês",
            changeType: "neutral"
          }
        ] : memberStats).map((stat) => (
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
      {userType !== 'admin' && (
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
      )}

      {/* Members List */}
      <Card className="shadow-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Lista de Membros</CardTitle>
              <CardDescription>
                Visualize e gerencie todos os membros cadastrados
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <div className="relative">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Buscar membros..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-8 w-64"
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
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Membro</TableHead>
                <TableHead>Contato</TableHead>
                <TableHead>Localização</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Cargo</TableHead>
                <TableHead>Data de Cadastro</TableHead>
                <TableHead className="text-right">Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredMembros.map((membro) => (
                <TableRow key={membro.id} className="hover:bg-accent/50 transition-smooth">
                  <TableCell className="font-medium">
                    <div className="flex items-center space-x-3">
                      <Avatar className="h-8 w-8">
                        <AvatarImage src="" alt={membro.nome} />
                        <AvatarFallback className="gradient-primary text-white text-xs">
                          {membro.nome.split(' ').map(n => n[0]).join('')}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <div className="font-medium">{membro.nome}</div>
                        <div className="text-sm text-muted-foreground">ID: {membro.id}</div>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="flex items-center text-sm">
                        <Mail className="mr-2 h-3 w-3 text-muted-foreground" />
                        {membro.email}
                      </div>
                      <div className="flex items-center text-sm">
                        <Phone className="mr-2 h-3 w-3 text-muted-foreground" />
                        {membro.telefone}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center text-sm">
                      <MapPin className="mr-2 h-3 w-3 text-muted-foreground" />
                      {membro.endereco}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge
                      variant={membro.status === "Ativo" ? "default" : "secondary"}
                      className={membro.status === "Ativo" ? "gradient-primary text-white" : ""}
                    >
                      {membro.status}
                    </Badge>
                  </TableCell>
                  <TableCell>{membro.cargo}</TableCell>
                  <TableCell>{new Date(membro.dataCadastro).toLocaleDateString('pt-BR')}</TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => window.location.href = `/membros/${membro.id}`}>
                          Ver detalhes
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => window.location.href = `/membros/${membro.id}/editar`}>
                          Editar
                        </DropdownMenuItem>
                        <DropdownMenuItem>Gerar cartão</DropdownMenuItem>
                        <DropdownMenuItem className="text-destructive">
                          Desativar
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}