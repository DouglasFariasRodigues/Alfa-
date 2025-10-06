import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, DollarSign, PieChart, Plus, Download } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const transacoes = [
  {
    id: 1,
    tipo: "Entrada",
    categoria: "Dízimo",
    valor: 2500.00,
    data: "2024-01-03",
    descricao: "Dízimos coletados no culto",
    metodo: "Dinheiro"
  },
  {
    id: 2,
    tipo: "Entrada",
    categoria: "Oferta",
    valor: 850.00,
    data: "2024-01-03",
    descricao: "Ofertas especiais",
    metodo: "PIX"
  },
  {
    id: 3,
    tipo: "Saída",
    categoria: "Manutenção",
    valor: 450.00,
    data: "2024-01-02",
    descricao: "Reparo do sistema de som",
    metodo: "Transferência"
  },
  {
    id: 4,
    tipo: "Saída",
    categoria: "Utilidades",
    valor: 320.00,
    data: "2024-01-02",
    descricao: "Conta de luz",
    metodo: "Débito"
  }
];

const categorias = [
  { nome: "Dízimos", valor: 25800, percentual: 45, cor: "gradient-primary" },
  { nome: "Ofertas", valor: 12400, percentual: 22, cor: "bg-blue-500" },
  { nome: "Doações", valor: 8600, percentual: 15, cor: "bg-green-500" },
  { nome: "Eventos", valor: 5200, percentual: 9, cor: "bg-yellow-500" },
  { nome: "Outros", valor: 4800, percentual: 9, cor: "bg-purple-500" }
];

export default function Financas() {
  const totalEntradas = 52000;
  const totalSaidas = 18500;
  const saldoAtual = totalEntradas - totalSaidas;

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Finanças</h1>
          <p className="text-muted-foreground">
            Controle financeiro completo da sua igreja
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Download className="mr-2 h-4 w-4" />
            Relatório
          </Button>
        <Button 
          onClick={() => window.location.href = '/financas/nova-transacao'}
          className="gradient-primary text-white shadow-elegant hover:opacity-90"
        >
          <Plus className="mr-2 h-4 w-4" />
          Nova Transação
        </Button>
        </div>
      </div>

      {/* Financial Overview */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="shadow-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Entradas</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              R$ {totalEntradas.toLocaleString('pt-BR')}
            </div>
            <p className="text-xs text-green-600">+12% vs mês anterior</p>
          </CardContent>
        </Card>
        
        <Card className="shadow-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Saídas</CardTitle>
            <TrendingDown className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              R$ {totalSaidas.toLocaleString('pt-BR')}
            </div>
            <p className="text-xs text-red-600">+8% vs mês anterior</p>
          </CardContent>
        </Card>
        
        <Card className="shadow-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Saldo Atual</CardTitle>
            <DollarSign className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              R$ {saldoAtual.toLocaleString('pt-BR')}
            </div>
            <p className="text-xs text-green-600">Posição financeira saudável</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Categories Breakdown */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <PieChart className="h-5 w-5" />
              Entradas por Categoria
            </CardTitle>
            <CardDescription>
              Distribuição das receitas no último mês
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {categorias.map((categoria, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium">{categoria.nome}</span>
                  <div className="flex items-center gap-2">
                    <span>R$ {categoria.valor.toLocaleString('pt-BR')}</span>
                    <span className="text-muted-foreground">({categoria.percentual}%)</span>
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${
                      categoria.cor.startsWith('gradient') 
                        ? categoria.cor 
                        : `${categoria.cor}`
                    }`}
                    style={{ width: `${categoria.percentual}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Recent Transactions */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle>Transações Recentes</CardTitle>
            <CardDescription>
              Últimas movimentações financeiras
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Tipo</TableHead>
                  <TableHead>Categoria</TableHead>
                  <TableHead>Valor</TableHead>
                  <TableHead>Data</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {transacoes.slice(0, 5).map((transacao) => (
                  <TableRow key={transacao.id} className="hover:bg-accent/50 transition-smooth">
                    <TableCell>
                      <Badge
                        variant={transacao.tipo === "Entrada" ? "default" : "secondary"}
                        className={transacao.tipo === "Entrada" ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200" : "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"}
                      >
                        {transacao.tipo}
                      </Badge>
                    </TableCell>
                    <TableCell className="font-medium">{transacao.categoria}</TableCell>
                    <TableCell className={transacao.tipo === "Entrada" ? "text-green-600 font-medium" : "text-red-600 font-medium"}>
                      {transacao.tipo === "Entrada" ? "+" : "-"}R$ {transacao.valor.toLocaleString('pt-BR')}
                    </TableCell>
                    <TableCell>{new Date(transacao.data).toLocaleDateString('pt-BR')}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Transactions */}
      <Card className="shadow-card">
        <CardHeader>
          <CardTitle>Todas as Transações</CardTitle>
          <CardDescription>
            Histórico completo de movimentações financeiras
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Data</TableHead>
                <TableHead>Tipo</TableHead>
                <TableHead>Categoria</TableHead>
                <TableHead>Descrição</TableHead>
                <TableHead>Método</TableHead>
                <TableHead className="text-right">Valor</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {transacoes.map((transacao) => (
                <TableRow key={transacao.id} className="hover:bg-accent/50 transition-smooth">
                  <TableCell>{new Date(transacao.data).toLocaleDateString('pt-BR')}</TableCell>
                  <TableCell>
                    <Badge
                      variant={transacao.tipo === "Entrada" ? "default" : "secondary"}
                      className={transacao.tipo === "Entrada" ? 
                        "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200" : 
                        "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
                      }
                    >
                      {transacao.tipo}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-medium">{transacao.categoria}</TableCell>
                  <TableCell>{transacao.descricao}</TableCell>
                  <TableCell>{transacao.metodo}</TableCell>
                  <TableCell className={`text-right font-medium ${
                    transacao.tipo === "Entrada" ? "text-green-600" : "text-red-600"
                  }`}>
                    {transacao.tipo === "Entrada" ? "+" : "-"}R$ {transacao.valor.toLocaleString('pt-BR')}
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