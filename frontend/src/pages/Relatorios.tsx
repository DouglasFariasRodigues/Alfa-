import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Calendar, Download, FileText, Users, DollarSign, Calendar as CalendarIcon } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface DashboardData {
  total_membros: number;
  membros_ativos: number;
  total_eventos: number;
  eventos_este_mes: number;
  entradas_mes: number;
  saidas_mes: number;
  saldo_mes: number;
  crescimento_membros: Array<{
    mes: string;
    membros: number;
  }>;
}

const Relatorios: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [dataInicio, setDataInicio] = useState('');
  const [dataFim, setDataFim] = useState('');
  const { toast } = useToast();

  useEffect(() => {
    carregarDashboard();
    // Definir período padrão (últimos 30 dias)
    const hoje = new Date();
    const trintaDiasAtras = new Date(hoje.getTime() - 30 * 24 * 60 * 60 * 1000);
    setDataFim(hoje.toISOString().split('T')[0]);
    setDataInicio(trintaDiasAtras.toISOString().split('T')[0]);
  }, []);

  const carregarDashboard = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/dashboard/');
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      } else {
        throw new Error('Erro ao carregar dashboard');
      }
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error);
      toast({
        title: 'Erro',
        description: 'Não foi possível carregar os dados do dashboard',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  const gerarRelatorioPDF = async (tipo: 'membros' | 'financeiro' | 'eventos') => {
    try {
      const params = new URLSearchParams();
      if (dataInicio) params.append('data_inicio', dataInicio);
      if (dataFim) params.append('data_fim', dataFim);

      const url = `http://127.0.0.1:8000/api/relatorios/${tipo}/pdf/?${params.toString()}`;
      
      // Abrir em nova aba para download
      window.open(url, '_blank');
      
      toast({
        title: 'Sucesso',
        description: `Relatório ${tipo} gerado com sucesso!`,
      });
    } catch (error) {
      console.error('Erro ao gerar relatório:', error);
      toast({
        title: 'Erro',
        description: 'Não foi possível gerar o relatório',
        variant: 'destructive',
      });
    }
  };

  const exportarCSV = async (tipo: 'membros' | 'transacoes') => {
    try {
      const url = `http://127.0.0.1:8000/api/exportar/${tipo}/csv/`;
      
      // Abrir em nova aba para download
      window.open(url, '_blank');
      
      toast({
        title: 'Sucesso',
        description: `Exportação ${tipo} realizada com sucesso!`,
      });
    } catch (error) {
      console.error('Erro ao exportar:', error);
      toast({
        title: 'Erro',
        description: 'Não foi possível exportar os dados',
        variant: 'destructive',
      });
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Carregando dashboard...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">📊 Relatórios e Analytics</h1>
        <div className="flex gap-2">
          <Button onClick={carregarDashboard} variant="outline">
            <Calendar className="w-4 h-4 mr-2" />
            Atualizar
          </Button>
        </div>
      </div>

      {/* Dashboard Cards */}
      {dashboardData && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total de Membros</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dashboardData.total_membros}</div>
              <p className="text-xs text-muted-foreground">
                {dashboardData.membros_ativos} ativos
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Eventos</CardTitle>
              <CalendarIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dashboardData.total_eventos}</div>
              <p className="text-xs text-muted-foreground">
                {dashboardData.eventos_este_mes} este mês
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Entradas do Mês</CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                R$ {Number(dashboardData.entradas_mes || 0).toFixed(2)}
              </div>
              <p className="text-xs text-muted-foreground">
                Receitas
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Saldo do Mês</CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className={`text-2xl font-bold ${
                Number(dashboardData.saldo_mes || 0) >= 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                R$ {Number(dashboardData.saldo_mes || 0).toFixed(2)}
              </div>
              <p className="text-xs text-muted-foreground">
                {Number(dashboardData.saidas_mes || 0).toFixed(2)} em saídas
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Filtros de Data */}
      <Card>
        <CardHeader>
          <CardTitle>📅 Filtros de Período</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="data-inicio">Data de Início</Label>
              <Input
                id="data-inicio"
                type="date"
                value={dataInicio}
                onChange={(e) => setDataInicio(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="data-fim">Data de Fim</Label>
              <Input
                id="data-fim"
                type="date"
                value={dataFim}
                onChange={(e) => setDataFim(e.target.value)}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Relatórios PDF */}
      <Card>
        <CardHeader>
          <CardTitle>📄 Relatórios PDF</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <h3 className="font-semibold">👥 Relatório de Membros</h3>
              <p className="text-sm text-muted-foreground">
                Estatísticas de membros, cargos e faixas etárias
              </p>
              <Button 
                onClick={() => gerarRelatorioPDF('membros')}
                className="w-full"
                variant="outline"
              >
                <FileText className="w-4 h-4 mr-2" />
                Gerar PDF
              </Button>
            </div>

            <div className="space-y-2">
              <h3 className="font-semibold">💰 Relatório Financeiro</h3>
              <p className="text-sm text-muted-foreground">
                Entradas, saídas, saldo e evolução financeira
              </p>
              <Button 
                onClick={() => gerarRelatorioPDF('financeiro')}
                className="w-full"
                variant="outline"
              >
                <FileText className="w-4 h-4 mr-2" />
                Gerar PDF
              </Button>
            </div>

            <div className="space-y-2">
              <h3 className="font-semibold">📅 Relatório de Eventos</h3>
              <p className="text-sm text-muted-foreground">
                Participação, frequência e estatísticas de eventos
              </p>
              <Button 
                onClick={() => gerarRelatorioPDF('eventos')}
                className="w-full"
                variant="outline"
              >
                <FileText className="w-4 h-4 mr-2" />
                Gerar PDF
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Exportação CSV */}
      <Card>
        <CardHeader>
          <CardTitle>📊 Exportação de Dados</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h3 className="font-semibold">👥 Exportar Membros</h3>
              <p className="text-sm text-muted-foreground">
                Exportar lista completa de membros em CSV
              </p>
              <Button 
                onClick={() => exportarCSV('membros')}
                className="w-full"
                variant="outline"
              >
                <Download className="w-4 h-4 mr-2" />
                Exportar CSV
              </Button>
            </div>

            <div className="space-y-2">
              <h3 className="font-semibold">💰 Exportar Transações</h3>
              <p className="text-sm text-muted-foreground">
                Exportar histórico de transações em CSV
              </p>
              <Button 
                onClick={() => exportarCSV('transacoes')}
                className="w-full"
                variant="outline"
              >
                <Download className="w-4 h-4 mr-2" />
                Exportar CSV
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Relatorios;
