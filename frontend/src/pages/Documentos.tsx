import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileText, Download, Plus, Search, Filter, Calendar, User, Loader2, Eye } from "lucide-react";
import { usePermissions } from "@/hooks/usePermissions";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useToast } from "@/hooks/use-toast";

// Mock data - em uma implementação real, isso viria da API
const documentos = [
  {
    id: 1,
    nome: "Certificado de Batismo - Maria Santos",
    tipo: "Certificado",
    categoria: "Batismo",
    membro: "Maria Santos",
    dataGeracao: "2024-01-03",
    status: "Gerado",
    tamanho: "245 KB",
    url: "/documents/certificado-batismo-maria-santos.pdf"
  },
  {
    id: 2,
    nome: "Carta de Transferência - João Silva",
    tipo: "Carta",
    categoria: "Transferência",
    membro: "João Silva",
    dataGeracao: "2024-01-02",
    status: "Gerado",
    tamanho: "189 KB",
    url: "/documents/carta-transferencia-joao-silva.pdf"
  },
  {
    id: 3,
    nome: "Relatório Financeiro - Janeiro 2024",
    tipo: "Relatório",
    categoria: "Financeiro",
    membro: null,
    dataGeracao: "2024-02-01",
    status: "Gerado",
    tamanho: "1.2 MB",
    url: "/documents/relatorio-financeiro-janeiro-2024.pdf"
  },
  {
    id: 4,
    nome: "Lista de Membros - Ativos",
    tipo: "Lista",
    categoria: "Membros",
    membro: null,
    dataGeracao: "2024-01-31",
    status: "Gerado",
    tamanho: "456 KB",
    url: "/documents/lista-membros-ativos.pdf"
  },
  {
    id: 5,
    nome: "Certificado de Batismo - Ana Costa",
    tipo: "Certificado",
    categoria: "Batismo",
    membro: "Ana Costa",
    dataGeracao: "2024-01-28",
    status: "Pendente",
    tamanho: "-",
    url: null
  }
];

const tiposDocumento = ["Todos", "Certificado", "Carta", "Relatório", "Lista"];
const categorias = ["Todas", "Batismo", "Transferência", "Financeiro", "Membros"];
const status = ["Todos", "Gerado", "Pendente", "Erro"];

export default function Documentos() {
  const { toast } = useToast();
  const [searchTerm, setSearchTerm] = useState("");
  const [filtroTipo, setFiltroTipo] = useState("Todos");
  const { canManage } = usePermissions();
  
  // Verificar se o usuário pode gerenciar documentos (criar, editar, deletar)
  const canManageDocuments = canManage('documentos');
  const [filtroCategoria, setFiltroCategoria] = useState("Todas");
  const [filtroStatus, setFiltroStatus] = useState("Todos");
  const [loading, setLoading] = useState(false);

  // Filtrar documentos
  const documentosFiltrados = documentos.filter(doc => {
    const matchSearch = doc.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
                       (doc.membro && doc.membro.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchTipo = filtroTipo === "Todos" || doc.tipo === filtroTipo;
    const matchCategoria = filtroCategoria === "Todas" || doc.categoria === filtroCategoria;
    const matchStatus = filtroStatus === "Todos" || doc.status === filtroStatus;
    
    return matchSearch && matchTipo && matchCategoria && matchStatus;
  });

  const handleDownload = async (documento: any) => {
    if (!documento.url) {
      toast({
        title: "Documento não disponível",
        description: "Este documento ainda não foi gerado ou está em processamento.",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      // Simular download
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      toast({
        title: "Download iniciado",
        description: `Baixando ${documento.nome}...`,
      });
      
      // Em uma implementação real, aqui seria o download real do arquivo
      console.log(`Downloading: ${documento.url}`);
    } catch (error) {
      toast({
        title: "Erro no download",
        description: "Não foi possível baixar o documento. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGerarDocumento = async (tipo: string) => {
    setLoading(true);
    try {
      // Simular geração de documento
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      toast({
        title: "Documento gerado!",
        description: `O ${tipo} foi gerado com sucesso.`,
      });
    } catch (error) {
      toast({
        title: "Erro ao gerar documento",
        description: "Não foi possível gerar o documento. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "Gerado":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300";
      case "Pendente":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300";
      case "Erro":
        return "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300";
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Documentos</h1>
          <p className="text-muted-foreground">
            Gerencie e baixe documentos da igreja
          </p>
        </div>
        <div className="flex gap-2">
          {canManageDocuments && (
            <>
              <Button onClick={() => handleGerarDocumento("Relatório Financeiro")} disabled={loading}>
                {loading ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <Plus className="h-4 w-4 mr-2" />
                )}
                Gerar Relatório
              </Button>
              <Button variant="outline" onClick={() => handleGerarDocumento("Lista de Membros")} disabled={loading}>
                {loading ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <FileText className="h-4 w-4 mr-2" />
                )}
                Gerar Lista
              </Button>
            </>
          )}
        </div>
      </div>

      {/* Estatísticas */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-muted-foreground" />
              <div className="ml-4">
                <p className="text-2xl font-bold">{documentos.length}</p>
                <p className="text-sm text-muted-foreground">Total de Documentos</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Download className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <p className="text-2xl font-bold">
                  {documentos.filter(d => d.status === "Gerado").length}
                </p>
                <p className="text-sm text-muted-foreground">Disponíveis</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <Calendar className="h-8 w-8 text-yellow-600" />
              <div className="ml-4">
                <p className="text-2xl font-bold">
                  {documentos.filter(d => d.status === "Pendente").length}
                </p>
                <p className="text-sm text-muted-foreground">Pendentes</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <User className="h-8 w-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-2xl font-bold">
                  {documentos.filter(d => d.membro).length}
                </p>
                <p className="text-sm text-muted-foreground">Documentos de Membros</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filtros */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filtros
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Buscar</label>
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Nome do documento ou membro..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Tipo</label>
              <Select value={filtroTipo} onValueChange={setFiltroTipo}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {tiposDocumento.map((tipo) => (
                    <SelectItem key={tipo} value={tipo}>
                      {tipo}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Categoria</label>
              <Select value={filtroCategoria} onValueChange={setFiltroCategoria}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {categorias.map((categoria) => (
                    <SelectItem key={categoria} value={categoria}>
                      {categoria}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Status</label>
              <Select value={filtroStatus} onValueChange={setFiltroStatus}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {status.map((status) => (
                    <SelectItem key={status} value={status}>
                      {status}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Lista de Documentos */}
      <Card>
        <CardHeader>
          <CardTitle>Documentos</CardTitle>
          <CardDescription>
            {documentosFiltrados.length} documento(s) encontrado(s)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Nome</TableHead>
                <TableHead>Tipo</TableHead>
                <TableHead>Categoria</TableHead>
                <TableHead>Membro</TableHead>
                <TableHead>Data de Geração</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Tamanho</TableHead>
                <TableHead className="text-right">Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {documentosFiltrados.map((documento) => (
                <TableRow key={documento.id}>
                  <TableCell className="font-medium">
                    {documento.nome}
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">{documento.tipo}</Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary">{documento.categoria}</Badge>
                  </TableCell>
                  <TableCell>
                    {documento.membro ? (
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4 text-muted-foreground" />
                        {documento.membro}
                      </div>
                    ) : (
                      <span className="text-muted-foreground">-</span>
                    )}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4 text-muted-foreground" />
                      {formatDate(documento.dataGeracao)}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge className={getStatusColor(documento.status)}>
                      {documento.status}
                    </Badge>
                  </TableCell>
                  <TableCell>{documento.tamanho}</TableCell>
                  <TableCell className="text-right">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDownload(documento)}
                      disabled={!documento.url || loading}
                    >
                      {loading ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Download className="h-4 w-4" />
                      )}
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          
          {documentosFiltrados.length === 0 && (
            <div className="text-center py-8">
              <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Nenhum documento encontrado</h3>
              <p className="text-muted-foreground">
                Tente ajustar os filtros ou gerar novos documentos.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}