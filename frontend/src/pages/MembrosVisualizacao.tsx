import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Search, Users, UserCheck, Calendar, Gift } from "lucide-react";

// Mock data - será substituído pela API Django
const membros = [
  {
    id: 1,
    nome: "João Silva",
    email: "joao@email.com",
    telefone: "(11) 99999-9999",
    endereco: "São Paulo, SP",
    status: "Ativo",
    dataCadastro: "2024-01-15",
    cargo: "Membro",
    avatar: "https://github.com/shadcn.png"
  },
  {
    id: 2,
    nome: "Maria Santos",
    email: "maria@email.com",
    telefone: "(11) 88888-8888",
    endereco: "Rio de Janeiro, RJ",
    status: "Ativo",
    dataCadastro: "2024-02-20",
    cargo: "Líder de Louvor",
    avatar: "https://github.com/shadcn.png"
  },
  {
    id: 3,
    nome: "Pedro Oliveira",
    email: "pedro@email.com",
    telefone: "(11) 77777-7777",
    endereco: "Belo Horizonte, MG",
    status: "Inativo",
    dataCadastro: "2023-12-10",
    cargo: "Membro",
    avatar: "https://github.com/shadcn.png"
  }
];

export default function MembrosVisualizacao() {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredMembros = membros.filter(membro =>
    membro.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    membro.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    membro.cargo.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const totalMembros = membros.length;
  const membrosAtivos = membros.filter(m => m.status === "Ativo").length;
  const novosEsseMes = membros.filter(m => {
    const dataCadastro = new Date(m.dataCadastro);
    const agora = new Date();
    return dataCadastro.getMonth() === agora.getMonth() && dataCadastro.getFullYear() === agora.getFullYear();
  }).length;

  const getStatusColor = (status: string) => {
    return status === "Ativo" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800";
  };

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Membros</h1>
        <p className="text-muted-foreground">Visualize informações dos membros da comunidade</p>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Membros</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalMembros}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Membros Ativos</CardTitle>
            <UserCheck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{membrosAtivos}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Novos este Mês</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{novosEsseMes}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Aniversariantes</CardTitle>
            <Gift className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de Membros */}
      <Card>
        <CardHeader>
          <CardTitle>Lista de Membros</CardTitle>
          <CardDescription>Todos os membros cadastrados na comunidade</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-2 mb-4">
            <div className="relative">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Buscar membros..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8"
              />
            </div>
          </div>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Membro</TableHead>
                <TableHead>Contato</TableHead>
                <TableHead>Localização</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Cargo</TableHead>
                <TableHead>Data de Cadastro</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredMembros.map((membro) => (
                <TableRow key={membro.id}>
                  <TableCell className="font-medium">
                    <div className="flex items-center space-x-3">
                      <Avatar className="h-8 w-8">
                        <AvatarImage src={membro.avatar} />
                        <AvatarFallback>{membro.nome.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                      </Avatar>
                      <div>
                        <div className="font-medium">{membro.nome}</div>
                        <div className="text-sm text-muted-foreground">ID: {membro.id}</div>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div>
                      <div>{membro.email}</div>
                      <div className="text-sm text-muted-foreground">{membro.telefone}</div>
                    </div>
                  </TableCell>
                  <TableCell>{membro.endereco}</TableCell>
                  <TableCell>
                    <Badge className={getStatusColor(membro.status)}>
                      {membro.status}
                    </Badge>
                  </TableCell>
                  <TableCell>{membro.cargo}</TableCell>
                  <TableCell>
                    {new Date(membro.dataCadastro).toLocaleDateString('pt-BR')}
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