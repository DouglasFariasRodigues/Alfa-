import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Search, Plus, Filter, MoreHorizontal, Phone, Mail, MapPin, Loader2, Eye, Edit, Trash2, Download } from "lucide-react";
import { usePermissions } from "@/hooks/usePermissions";
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
import { useMembros, useDeleteMembro } from "@/hooks/useMembros";
import { toast } from "sonner";

export default function Membros() {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("");

  // Buscar membros da API
  const { data: membros = [], isLoading, error } = useMembros({ 
    search: searchTerm || undefined,
    status: statusFilter || undefined 
  });
  
  const deleteMembroMutation = useDeleteMembro();
  const { canManage } = usePermissions();
  
  // Verificar se o usuário pode gerenciar membros (criar, editar, deletar)
  const canManageMembers = canManage('membros');

  const handleDeleteMembro = async (id: number) => {
    if (window.confirm('Tem certeza que deseja desativar este membro?')) {
      try {
        await deleteMembroMutation.mutateAsync(id);
        toast.success('Membro desativado com sucesso!');
      } catch (error) {
        toast.error('Erro ao desativar membro');
      }
    }
  };

  const handleGerarRelatorio = async () => {
    try {
      // Gerar relatório PDF de membros
      const dataInicio = new Date();
      dataInicio.setMonth(dataInicio.getMonth() - 1);
      const dataFim = new Date();
      
      const params = new URLSearchParams({
        data_inicio: dataInicio.toISOString().split('T')[0],
        data_fim: dataFim.toISOString().split('T')[0]
      });
      
      // Fazer requisição para o backend
      const response = await fetch(`http://127.0.0.1:8000/api/relatorios/membros/pdf/?${params}`, {
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
        a.download = `relatorio_membros_${new Date().toISOString().split('T')[0]}.pdf`;
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

  // Calcular estatísticas
  const totalMembros = membros.length;
  const membrosAtivos = membros.filter(m => m.status === 'ativo').length;
  const membrosInativos = membros.filter(m => m.status === 'inativo').length;
  
  // Membros cadastrados este mês
  const currentMonth = new Date().getMonth();
  const currentYear = new Date().getFullYear();
  const novosEsteMes = membros.filter(m => {
    const dataCadastro = new Date(m.created_at);
    return dataCadastro.getMonth() === currentMonth && dataCadastro.getFullYear() === currentYear;
  }).length;

  if (error) {
    return (
      <div className="p-6">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-600">Erro ao carregar membros</h2>
          <p className="text-gray-600">Tente recarregar a página</p>
        </div>
      </div>
    );
  }

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
        <div className="flex gap-2">
          <Button 
            onClick={handleGerarRelatorio}
            variant="outline"
            className="border-blue-200 text-blue-600 hover:bg-blue-50"
          >
            <Download className="mr-2 h-4 w-4" />
            Relatório
          </Button>
          {canManageMembers && (
            <Button 
              onClick={() => window.location.href = '/membros/novo'}
              className="gradient-primary text-white shadow-elegant hover:opacity-90"
            >
              <Plus className="mr-2 h-4 w-4" />
              Novo Membro
            </Button>
          )}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total de Membros</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalMembros}</div>
            <p className="text-xs text-green-600">+{novosEsteMes} este mês</p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Membros Ativos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{membrosAtivos}</div>
            <p className="text-xs text-muted-foreground">
              {totalMembros > 0 ? Math.round((membrosAtivos / totalMembros) * 100) : 0}% do total
            </p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Novos este Mês</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{novosEsteMes}</div>
            <p className="text-xs text-green-600">Cadastros recentes</p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Membros Inativos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{membrosInativos}</div>
            <p className="text-xs text-muted-foreground">Precisam de atenção</p>
          </CardContent>
        </Card>
      </div>

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
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-3 py-2 border border-input bg-background rounded-md text-sm"
              >
                <option value="">Todos os status</option>
                <option value="ativo">Ativo</option>
                <option value="inativo">Inativo</option>
                <option value="falecido">Falecido</option>
                <option value="afastado">Afastado</option>
              </select>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin" />
              <span className="ml-2">Carregando membros...</span>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Membro</TableHead>
                  <TableHead>Contato</TableHead>
                  <TableHead>Localização</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Data de Cadastro</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {membros.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8">
                      <p className="text-muted-foreground">Nenhum membro encontrado</p>
                    </TableCell>
                  </TableRow>
                ) : (
                  membros.map((membro) => (
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
                      variant={membro.status === "ativo" ? "default" : "secondary"}
                      className={membro.status === "ativo" ? "gradient-primary text-white" : ""}
                    >
                      {membro.status}
                    </Badge>
                  </TableCell>
                  <TableCell>{new Date(membro.created_at).toLocaleDateString('pt-BR')}</TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => window.location.href = `/membros/${membro.id}`}>
                          <Eye className="mr-2 h-4 w-4" />
                          Ver detalhes
                        </DropdownMenuItem>
                        {canManageMembers && (
                          <>
                            <DropdownMenuItem onClick={() => window.location.href = `/membros/${membro.id}/editar`}>
                              <Edit className="mr-2 h-4 w-4" />
                              Editar
                            </DropdownMenuItem>
                            <DropdownMenuItem>Gerar cartão</DropdownMenuItem>
                            <DropdownMenuItem 
                              className="text-destructive"
                              onClick={() => handleDeleteMembro(membro.id)}
                            >
                              <Trash2 className="mr-2 h-4 w-4" />
                              Desativar
                            </DropdownMenuItem>
                          </>
                        )}
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}