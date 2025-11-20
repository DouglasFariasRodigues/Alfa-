import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, DollarSign, PieChart, Calendar, Target, Users, Building } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const transacoesMensais = [
  {
    id: 1,
    tipo: "Entrada",
    categoria: "Dízimo",
    valor: 18500.00,
    data: "2024-01-15",
    descricao: "Dízimos coletados nos cultos dominicais",
    metodo: "Dinheiro",
    origem: "Membros da congregação"
  },
  {
    id: 2,
    tipo: "Entrada",
    categoria: "Oferta",
    valor: 6200.00,
    data: "2024-01-15",
    descricao: "Ofertas especiais do mês",
    metodo: "PIX",
    origem: "Doações voluntárias"
  },
  {
    id: 3,
    tipo: "Entrada",
    categoria: "Doação",
    valor: 4800.00,
    data: "2024-01-10",
    descricao: "Doação para reforma do templo",
    metodo: "Transferência",
    origem: "Empresa parceira"
  },
  {
    id: 4,
    tipo: "Saída",
    categoria: "Manutenção",
    valor: 3200.00,
    data: "2024-01-08",
    descricao: "Reparo do sistema de som e iluminação",
    metodo: "Transferência",
    destino: "Empresa de manutenção elétrica",
    finalidade: "Manutenção do templo"
  },
  {
    id: 5,
    tipo: "Saída",
    categoria: "Utilidades",
    valor: 1850.00,
    data: "2024-01-05",
    descricao: "Contas de luz, água e internet",
    metodo: "Débito automático",
    destino: "Concessionárias de serviços",
    finalidade: "Despesas operacionais"
  },
  {
    id: 6,
    tipo: "Saída",
    categoria: "Salários",
    valor: 8500.00,
    data: "2024-01-30",
    descricao: "Pagamento de funcionários",
    metodo: "Transferência",
    destino: "Funcionários da igreja",
    finalidade: "Remuneração da equipe"
  },
  {
    id: 7,
    tipo: "Saída",
    categoria: "Eventos",
    valor: 2100.00,
    data: "2024-01-20",
    descricao: "Materiais para evento beneficente",
    metodo: "Dinheiro",
    destino: "Fornecedores de material",
    finalidade: "Atividades sociais"
  },
  {
    id: 8,
    tipo: "Saída",
    categoria: "Missões",
    valor: 1500.00,
    data: "2024-01-25",
    descricao: "Apoio a projetos missionários",
    metodo: "Transferência",
    destino: "ONG parceira",
    finalidade: "Trabalho missionário"
  }
];

const categoriasEntradas = [
  { nome: "Dízimos", valor: 18500, percentual: 52, cor: "gradient-primary", origem: "Membros" },
  { nome: "Ofertas", valor: 6200, percentual: 17, cor: "bg-blue-500", origem: "Congregação" },
  { nome: "Doações", valor: 4800, percentual: 13, cor: "bg-green-500", origem: "Parceiros externos" },
  { nome: "Eventos", valor: 3200, percentual: 9, cor: "bg-yellow-500", origem: "Atividades especiais" },
  { nome: "Outros", valor: 3300, percentual: 9, cor: "bg-purple-500", origem: "Diversas fontes" }
];

const categoriasSaidas = [
  { nome: "Salários", valor: 8500, percentual: 35, cor: "bg-red-500", destino: "Equipe", finalidade: "Remuneração" },
  { nome: "Manutenção", valor: 3200, percentual: 13, cor: "bg-orange-500", destino: "Serviços", finalidade: "Conservação" },
  { nome: "Utilidades", valor: 1850, percentual: 8, cor: "bg-gray-500", destino: "Concessionárias", finalidade: "Operacional" },
  { nome: "Eventos", valor: 2100, percentual: 9, cor: "bg-indigo-500", destino: "Materiais", finalidade: "Atividades" },
  { nome: "Missões", valor: 1500, percentual: 6, cor: "bg-teal-500", destino: "Projetos", finalidade: "Missionário" },
  { nome: "Outros", valor: 4850, percentual: 20, cor: "bg-pink-500", destino: "Diversos", finalidade: "Várias" }
];

export default function FinancasPublico() {
  const totalEntradas = transacoesMensais
    .filter(t => t.tipo === "Entrada")
    .reduce((sum, t) => sum + t.valor, 0);

  const totalSaidas = transacoesMensais
    .filter(t => t.tipo === "Saída")
    .reduce((sum, t) => sum + t.valor, 0);

  const saldoAtual = totalEntradas - totalSaidas;

  const totalDoacoes = transacoesMensais
    .filter(t => t.tipo === "Entrada" && t.categoria === "Doação")
    .reduce((sum, t) => sum + t.valor, 0);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Transparência Financeira</h1>
        <p className="text-muted-foreground">
          Relatório financeiro mensal detalhado - Janeiro 2024
        </p>
        <p className="text-sm text-muted-foreground">
          📊 Informações públicas para transparência da congregação
        </p>
      </div>

      {/* Monthly Financial Summary */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="shadow-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Entradas</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              R$ {totalEntradas.toLocaleString('pt-BR')}
            </div>
            <p className="text-xs text-green-600">Receitas do mês</p>
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
            <p className="text-xs text-red-600">Despesas do mês</p>
          </CardContent>
        </Card>

        <Card className="shadow-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Saldo do Mês</CardTitle>
            <DollarSign className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              R$ {saldoAtual.toLocaleString('pt-BR')}
            </div>
            <p className="text-xs text-green-600">Resultado mensal</p>
          </CardContent>
        </Card>

        <Card className="shadow-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Doações Recebidas</CardTitle>
            <Users className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">
              R$ {totalDoacoes.toLocaleString('pt-BR')}
            </div>
            <p className="text-xs text-blue-600">Doações especiais</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Income Breakdown */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-green-600" />
              Entradas por Categoria
            </CardTitle>
            <CardDescription>
              Origem das receitas mensais
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {categoriasEntradas.map((categoria, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">{categoria.nome}</span>
                    <Badge variant="outline" className="text-xs">
                      {categoria.origem}
                    </Badge>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">R$ {categoria.valor.toLocaleString('pt-BR')}</div>
                    <div className="text-xs text-muted-foreground">({categoria.percentual}%)</div>
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

        {/* Expenses Breakdown */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingDown className="h-5 w-5 text-red-600" />
              Saídas por Categoria
            </CardTitle>
            <CardDescription>
              Destino e finalidade das despesas
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {categoriasSaidas.map((categoria, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex flex-col">
                    <span className="font-medium">{categoria.nome}</span>
                    <div className="flex gap-2 text-xs text-muted-foreground">
                      <span>📍 {categoria.destino}</span>
                      <span>🎯 {categoria.finalidade}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">R$ {categoria.valor.toLocaleString('pt-BR')}</div>
                    <div className="text-xs text-muted-foreground">({categoria.percentual}%)</div>
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${categoria.cor}`}
                    style={{ width: `${categoria.percentual}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Detailed Monthly Transactions */}
      <Card className="shadow-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="h-5 w-5" />
            Transações do Mês
          </CardTitle>
          <CardDescription>
            Movimentações financeiras detalhadas com origem/destino e finalidade
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
                <TableHead>Origem/Destino</TableHead>
                <TableHead>Finalidade</TableHead>
                <TableHead>Método</TableHead>
                <TableHead className="text-right">Valor</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {transacoesMensais.map((transacao) => (
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
                  <TableCell className="max-w-xs truncate" title={transacao.descricao}>
                    {transacao.descricao}
                  </TableCell>
                  <TableCell>
                    {transacao.tipo === "Entrada" ? (
                      <div className="flex items-center gap-1">
                        <Users className="h-3 w-3" />
                        {transacao.origem}
                      </div>
                    ) : (
                      <div className="flex items-center gap-1">
                        <Building className="h-3 w-3" />
                        {transacao.destino}
                      </div>
                    )}
                  </TableCell>
                  <TableCell>
                    {transacao.tipo === "Saída" && (
                      <div className="flex items-center gap-1">
                        <Target className="h-3 w-3" />
                        {transacao.finalidade}
                      </div>
                    )}
                  </TableCell>
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

      {/* Footer with transparency message */}
      <div className="text-center py-4 border-t">
        <p className="text-sm text-muted-foreground">
          💡 Esta página demonstra o compromisso da igreja com a transparência financeira.
          Todos os valores são públicos e auditáveis pela congregação.
        </p>
      </div>
    </div>
  );
}
