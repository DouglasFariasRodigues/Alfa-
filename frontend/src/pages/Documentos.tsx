import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileText, Download, Search, Calendar, User, Loader2 } from "lucide-react";
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
import { useDocumentos, type Documento } from "@/hooks/useDocumentos";
import { apiClient } from "@/lib/api";
import { Skeleton } from "@/components/ui/skeleton";

const tiposDocumento = [
  { value: "todos", label: "Todos" },
  { value: "cartao_membro", label: "Cartão de Membro" },
  { value: "transferencia", label: "Transferência" },
  { value: "registro", label: "Registro" },
];

const getTipoLabel = (tipo: string) => {
  const tipoObj = tiposDocumento.find(t => t.value === tipo);
  return tipoObj ? tipoObj.label : tipo;
};

export default function Documentos() {
  const { toast } = useToast();
  const [searchTerm, setSearchTerm] = useState("");
  const [filtroTipo, setFiltroTipo] = useState("todos");
  const { canManage, user } = usePermissions();
  const { data: documentos = [], isLoading, error } = useDocumentos();
  const [downloadingId, setDownloadingId] = useState<number | null>(null);
  
  // Verificar se o usuário pode gerenciar documentos (criar, editar, deletar)
  const canManageDocuments = canManage('documentos');

  // Filtrar documentos
  const documentosFiltrados = documentos.filter((doc: Documento) => {
    const matchSearch = 
      getTipoLabel(doc.tipo).toLowerCase().includes(searchTerm.toLowerCase()) ||
      (doc.membro_nome && doc.membro_nome.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchTipo = filtroTipo === "todos" || doc.tipo === filtroTipo;
    
    return matchSearch && matchTipo;
  });

  const handleDownload = async (documento: Documento) => {
    if (!documento.arquivo) {
      toast({
        title: "Documento não disponível",
        description: "Este documento ainda não foi gerado ou está em processamento.",
        variant: "destructive",
      });
      return;
    }

    setDownloadingId(documento.id);
    try {
      // Se o arquivo é uma URL completa, fazer download direto
      if (documento.arquivo.startsWith('http')) {
        const link = document.createElement('a');
        link.href = documento.arquivo;
        link.download = `${getTipoLabel(documento.tipo)}_${documento.id}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        // Caso contrário, usar a API
        const blob = await apiClient.downloadDocumento(documento.id);
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${getTipoLabel(documento.tipo)}_${documento.id}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      }
      
      toast({
        title: "Download iniciado",
        description: `Baixando ${getTipoLabel(documento.tipo)}...`,
      });
    } catch (error) {
      toast({
        title: "Erro no download",
        description: "Não foi possível baixar o documento. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setDownloadingId(null);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const getStatusBadge = (documento: Documento) => {
    if (documento.arquivo) {
      return <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">Disponível</Badge>;
    }
    return <Badge className="bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300">Pendente</Badge>;
  };

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <Card className="w-full max-w-md">
          <CardContent>
            <div className="text-center">
              <p className="text-red-500 mb-4">Erro ao carregar documentos</p>
              <Button onClick={() => window.location.reload()}>
                Tentar Novamente
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Meus Documentos</h1>
          <p className="text-muted-foreground">
            {canManageDocuments 
              ? "Gerencie e baixe documentos da igreja" 
              : "Visualize e baixe seus documentos pessoais"}
          </p>
        </div>
      </div>

      {/* Estatísticas */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-muted-foreground" />
              <div className="ml-4">
                <p className="text-2xl font-bold">
                  {isLoading ? <Skeleton className="h-8 w-16" /> : documentos.length}
                </p>
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
                  {isLoading ? <Skeleton className="h-8 w-16" /> : documentos.filter((d: Documento) => d.arquivo).length}
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
                  {isLoading ? <Skeleton className="h-8 w-16" /> : documentos.filter((d: Documento) => !d.arquivo).length}
                </p>
                <p className="text-sm text-muted-foreground">Pendentes</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filtros */}
      <Card>
        <CardHeader>
          <CardTitle>Filtros</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <label className="text-sm font-medium">Buscar</label>
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Buscar por tipo ou nome..."
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
                    <SelectItem key={tipo.value} value={tipo.value}>
                      {tipo.label}
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
            {isLoading ? "Carregando..." : `${documentosFiltrados.length} documento(s) encontrado(s)`}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="flex items-center space-x-4">
                  <Skeleton className="h-4 w-[200px]" />
                  <Skeleton className="h-4 w-[150px]" />
                  <Skeleton className="h-4 w-[100px]" />
                </div>
              ))}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Tipo</TableHead>
                  {canManageDocuments && <TableHead>Membro</TableHead>}
                  <TableHead>Data de Geração</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {documentosFiltrados.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={canManageDocuments ? 5 : 4} className="text-center py-8">
                      <div className="text-muted-foreground">
                        {searchTerm || filtroTipo !== "todos" 
                          ? 'Nenhum documento encontrado para os filtros selecionados.' 
                          : 'Nenhum documento disponível.'}
                      </div>
                    </TableCell>
                  </TableRow>
                ) : (
                  documentosFiltrados.map((documento: Documento) => (
                    <TableRow key={documento.id}>
                      <TableCell className="font-medium">
                        {getTipoLabel(documento.tipo)}
                      </TableCell>
                      {canManageDocuments && (
                        <TableCell>
                          {documento.membro_nome ? (
                            <div className="flex items-center gap-2">
                              <User className="h-4 w-4 text-muted-foreground" />
                              {documento.membro_nome}
                            </div>
                          ) : (
                            <span className="text-muted-foreground">-</span>
                          )}
                        </TableCell>
                      )}
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Calendar className="h-4 w-4 text-muted-foreground" />
                          {formatDate(documento.gerado_em)}
                        </div>
                      </TableCell>
                      <TableCell>
                        {getStatusBadge(documento)}
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDownload(documento)}
                          disabled={!documento.arquivo || downloadingId === documento.id}
                        >
                          {downloadingId === documento.id ? (
                            <Loader2 className="h-4 w-4 animate-spin" />
                          ) : (
                            <Download className="h-4 w-4" />
                          )}
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          )}
          
          {!isLoading && documentosFiltrados.length === 0 && (
            <div className="text-center py-8">
              <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Nenhum documento encontrado</h3>
              <p className="text-muted-foreground">
                {searchTerm || filtroTipo !== "todos"
                  ? "Tente ajustar os filtros de busca."
                  : "Você ainda não possui documentos cadastrados."}
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
