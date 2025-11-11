import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, DollarSign, PieChart, Plus, Download, Loader2, Eye, Heart } from "lucide-react";
import { usePermissions } from "@/hooks/usePermissions";
import { QRCodeDonation } from "@/components/donations/QRCodeDonation";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useTransacoes } from "@/hooks/useTransacoes";
import { toast } from "sonner";

export default function Financas() {
  // Buscar transações da API
  const { data: transacoes = [], isLoading, error } = useTransacoes();
  const { canManage } = usePermissions();
  
  // Verificar se o usuário pode gerenciar finanças (criar, editar, deletar)
  const canManageFinances = canManage('financas');

  const handleDoacao = (amount: number, method: string) => {
    toast.success(`Doação de R$ ${amount.toFixed(2)} via ${method.toUpperCase()} registrada!`);
    console.log('Doação realizada!', { amount, method });
  };

  const handleGerarRelatorio = async () => {
    try {
      // Gerar relatório PDF financeiro
      const dataInicio = new Date();
      dataInicio.setMonth(dataInicio.getMonth() - 1);
      const dataFim = new Date();
      
      const params = new URLSearchParams({
        data_inicio: dataInicio.toISOString().split('T')[0],
        data_fim: dataFim.toISOString().split('T')[0]
      });
      
      // Fazer requisição para o backend
      const response = await fetch(`http://127.0.0.1:8000/api/relatorios/financeiro/pdf/?${params}`, {
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
        a.download = `relatorio_financeiro_${new Date().toISOString().split('T')[0]}.pdf`;
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

  if (error) {
    return (
      <div className="p-6">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-600">Erro ao carregar transações</h2>
          <p className="text-gray-600">Tente recarregar a página</p>
        </div>
      </div>
    );
  }

  // Calcular estatísticas
  const totalEntradas = transacoes
    .filter(t => t.tipo === 'entrada')
    .reduce((sum, t) => sum + parseFloat(t.valor.toString()), 0);
  
  const totalSaidas = transacoes
    .filter(t => t.tipo === 'saida')
    .reduce((sum, t) => sum + parseFloat(t.valor.toString()), 0);
  
  const saldoAtual = totalEntradas - totalSaidas;

  // Calcular categorias
  const categoriasMap = new Map();
  transacoes
    .filter(t => t.tipo === 'entrada')
    .forEach(t => {
      const valor = parseFloat(t.valor.toString());
      categoriasMap.set(t.categoria, (categoriasMap.get(t.categoria) || 0) + valor);
    });

  const categorias = Array.from(categoriasMap.entries()).map(([nome, valor]) => ({
    nome,
    valor,
    percentual: totalEntradas > 0 ? Math.round((valor / totalEntradas) * 100) : 0,
    cor: nome === 'Dízimo' ? 'gradient-primary' : 
         nome === 'Oferta' ? 'bg-blue-500' :
         nome === 'Doação' ? 'bg-green-500' : 'bg-purple-500'
  }));

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Finanças</h1>
          <p className="text-muted-foreground">
            {canManageFinances 
              ? "Controle financeiro completo da sua igreja"
              : "Visualize as finanças e faça sua contribuição"
            }
          </p>
        </div>
        <div className="flex gap-2">
          {canManageFinances && (
            <>
              <Button 
                onClick={handleGerarRelatorio}
                variant="outline"
                className="border-blue-200 text-blue-600 hover:bg-blue-50"
              >
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
            </>
          )}
          {!canManageFinances && (
            <Button 
              onClick={() => {
                // Scroll para a seção de doação
                const doacaoSection = document.getElementById('secao-doacao');
                doacaoSection?.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }}
              className="gradient-primary text-white shadow-elegant hover:opacity-90"
            >
              <Heart className="mr-2 h-4 w-4" />
              Fazer Doação
            </Button>
          )}
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
            {isLoading ? (
              <div className="flex items-center justify-center py-4">
                <Loader2 className="h-6 w-6 animate-spin" />
                <span className="ml-2">Carregando...</span>
              </div>
            ) : categorias.length === 0 ? (
              <p className="text-muted-foreground text-center py-4">Nenhuma transação de entrada encontrada</p>
            ) : (
              categorias.map((categoria, index) => (
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
              ))
            )}
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
            {isLoading ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin" />
                <span className="ml-2">Carregando transações...</span>
              </div>
            ) : (
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
                  {transacoes.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={4} className="text-center py-8">
                        <p className="text-muted-foreground">Nenhuma transação encontrada</p>
                      </TableCell>
                    </TableRow>
                  ) : (
                    transacoes.slice(0, 5).map((transacao) => (
                  <TableRow key={transacao.id} className="hover:bg-accent/50 transition-smooth">
                    <TableCell>
                      <Badge
                        variant={transacao.tipo === "entrada" ? "default" : "secondary"}
                        className={transacao.tipo === "entrada" ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200" : "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"}
                      >
                        {transacao.tipo === "entrada" ? "Entrada" : "Saída"}
                      </Badge>
                    </TableCell>
                    <TableCell className="font-medium">{transacao.categoria}</TableCell>
                    <TableCell className={transacao.tipo === "entrada" ? "text-green-600 font-medium" : "text-red-600 font-medium"}>
                      {transacao.tipo === "entrada" ? "+" : "-"}R$ {parseFloat(transacao.valor.toString()).toLocaleString('pt-BR')}
                    </TableCell>
                    <TableCell>{new Date(transacao.data).toLocaleDateString('pt-BR')}</TableCell>
                  </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            )}
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
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-6 w-6 animate-spin" />
              <span className="ml-2">Carregando transações...</span>
            </div>
          ) : (
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
                {transacoes.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8">
                      <p className="text-muted-foreground">Nenhuma transação encontrada</p>
                    </TableCell>
                  </TableRow>
                ) : (
                  transacoes.map((transacao) => (
                <TableRow key={transacao.id} className="hover:bg-accent/50 transition-smooth">
                  <TableCell>{new Date(transacao.data).toLocaleDateString('pt-BR')}</TableCell>
                  <TableCell>
                    <Badge
                      variant={transacao.tipo === "entrada" ? "default" : "secondary"}
                      className={transacao.tipo === "entrada" ? 
                        "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200" : 
                        "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
                      }
                    >
                      {transacao.tipo === "entrada" ? "Entrada" : "Saída"}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-medium">{transacao.categoria}</TableCell>
                  <TableCell>{transacao.descricao || 'Sem descrição'}</TableCell>
                  <TableCell>{transacao.metodo_pagamento || 'Não informado'}</TableCell>
                  <TableCell className={`text-right font-medium ${
                    transacao.tipo === "entrada" ? "text-green-600" : "text-red-600"
                  }`}>
                    {transacao.tipo === "entrada" ? "+" : "-"}R$ {parseFloat(transacao.valor.toString()).toLocaleString('pt-BR')}
                  </TableCell>
                </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Seção de Doação para Membros */}
      {!canManageFinances ? (
        <div id="secao-doacao" className="space-y-6">
          <Card className="shadow-card border-2 border-primary/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-2xl">
                <Heart className="h-6 w-6 text-red-500" />
                Faça sua Doação
              </CardTitle>
              <CardDescription className="text-base">
                Sua contribuição é muito importante para nossa comunidade. Escolha o valor e método de pagamento.
              </CardDescription>
            </CardHeader>
          </Card>
          
          <div className="grid gap-6 md:grid-cols-2">
            <QRCodeDonation onDonate={handleDoacao} />
          
            <Card className="shadow-card">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Heart className="h-5 w-5 text-red-500" />
                  Suas Doações
                </CardTitle>
                <CardDescription>
                  Histórico das suas contribuições
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <div>
                      <p className="font-medium text-green-800">Oferta Especial</p>
                      <p className="text-sm text-green-600">15/10/2024</p>
                    </div>
                    <Badge className="bg-green-100 text-green-800">R$ 50,00</Badge>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                    <div>
                      <p className="font-medium text-blue-800">Dízimo</p>
                      <p className="text-sm text-blue-600">01/10/2024</p>
                    </div>
                    <Badge className="bg-blue-100 text-blue-800">R$ 200,00</Badge>
                  </div>
                  
                  <div className="text-center py-4">
                    <p className="text-sm text-muted-foreground">
                      Total doado este mês: <span className="font-semibold text-green-600">R$ 250,00</span>
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      ) : null}
    </div>
  );
}