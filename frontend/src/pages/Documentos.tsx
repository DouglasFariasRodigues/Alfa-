import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileText, Download, Plus, Search, Filter, Calendar, User } from "lucide-react";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const documentos = [
  {
    id: 1,
    nome: "Certificado de Batismo - Maria Santos",
    tipo: "Certificado",
    categoria: "Batismo",
    membro: "Maria Santos",
    dataGeracao: "2024-01-03",
    status: "Gerado",
    tamanho: "245 KB"
  },
  {
    id: 2,
    nome: "Carta de Transferência - João Silva",
    tipo: "Carta",
    categoria: "Transferência",
    membro: "João Silva",
    dataGeracao: "2024-01-02",
    status: "Enviado",
    tamanho: "189 KB"
  },
  {
    id: 3,
    nome: "Relatório Financeiro - Dezembro 2023",
    tipo: "Relatório",
    categoria: "Financeiro",
    membro: "-",
    dataGeracao: "2024-01-01",
    status: "Gerado",
    tamanho: "2.1 MB"
  },
  {
    id: 4,
    nome: "Certificado de Apresentação - Ana Costa",
    tipo: "Certificado",
    categoria: "Apresentação",
    membro: "Ana Costa",
    dataGeracao: "2023-12-30",
    status: "Gerado",
    tamanho: "198 KB"
  }
];

const tiposDocumento = [
  { nome: "Certificados", quantidade: 45, cor: "gradient-primary" },
  { nome: "Cartas", quantidade: 23, cor: "bg-blue-500" },
  { nome: "Relatórios", quantidade: 12, cor: "bg-green-500" },
  { nome: "Declarações", quantidade: 8, cor: "bg-orange-500" }
];

export default function Documentos() {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "Gerado":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "Enviado":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200";
      case "Pendente":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200";
    }
  };

  const getTipoColor = (tipo: string) => {
    switch (tipo) {
      case "Certificado":
        return "gradient-primary text-white";
      case "Carta":
        return "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200";
      case "Relatório":
        return "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200";
      case "Declaração":
        return "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200";
      default:
        return "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200";
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Documentos</h1>
          <p className="text-muted-foreground">
            Gerencie certificados, cartas e relatórios automatizados
          </p>
        </div>
        <Button className="gradient-primary text-white shadow-elegant hover:opacity-90">
          <Plus className="mr-2 h-4 w-4" />
          Gerar Documento
        </Button>
      </div>

      {/* Stats */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total de Documentos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">88</div>
            <p className="text-xs text-green-600">+12 este mês</p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Certificados Emitidos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">45</div>
            <p className="text-xs text-muted-foreground">51% do total</p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Cartas Enviadas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">23</div>
            <p className="text-xs text-green-600">+5 esta semana</p>
          </CardContent>
        </Card>
        <Card className="shadow-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Relatórios Gerados</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground">Mensais e anuais</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-4">
        {/* Document Types */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle>Tipos de Documento</CardTitle>
            <CardDescription>
              Distribuição por categoria
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {tiposDocumento.map((tipo, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium">{tipo.nome}</span>
                  <span className="text-muted-foreground">{tipo.quantidade}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      tipo.cor.startsWith('gradient') 
                        ? tipo.cor 
                        : `${tipo.cor}`
                    }`}
                    style={{ width: `${(tipo.quantidade / 88) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="shadow-card lg:col-span-3">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Documentos Recentes</CardTitle>
                <CardDescription>
                  Histórico de documentos gerados automaticamente
                </CardDescription>
              </div>
              <div className="flex items-center space-x-2">
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Buscar documentos..."
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
                  <TableHead>Documento</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead>Membro</TableHead>
                  <TableHead>Data de Geração</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Tamanho</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {documentos.map((doc) => (
                  <TableRow key={doc.id} className="hover:bg-accent/50 transition-smooth">
                    <TableCell className="font-medium">
                      <div className="flex items-center gap-2">
                        <FileText className="h-4 w-4 text-muted-foreground" />
                        <span className="line-clamp-1">{doc.nome}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge className={getTipoColor(doc.tipo)}>
                        {doc.tipo}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        {doc.membro !== "-" && <User className="h-3 w-3 text-muted-foreground" />}
                        <span>{doc.membro}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-3 w-3 text-muted-foreground" />
                        <span>{new Date(doc.dataGeracao).toLocaleDateString('pt-BR')}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(doc.status)}>
                        {doc.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-muted-foreground">{doc.tamanho}</TableCell>
                    <TableCell className="text-right">
                      <div className="flex gap-2 justify-end">
                        <Button variant="outline" size="sm">
                          <Download className="mr-1 h-3 w-3" />
                          Download
                        </Button>
                        <Button variant="outline" size="sm">
                          Ver
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      {/* Quick Generate */}
      <Card className="shadow-card">
        <CardHeader>
          <CardTitle>Geração Rápida de Documentos</CardTitle>
          <CardDescription>
            Crie documentos automatizados com apenas alguns cliques
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <FileText className="h-6 w-6" />
              <span>Certificado de Batismo</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <FileText className="h-6 w-6" />
              <span>Carta de Transferência</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <FileText className="h-6 w-6" />
              <span>Relatório Financeiro</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <FileText className="h-6 w-6" />
              <span>Declaração de Membro</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}