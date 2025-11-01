import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { DollarSign, TrendingUp, TrendingDown, Plus, QrCode } from "lucide-react";

// Mock data - será substituído pela API Django
const transacoes = [
  {
    id: 1,
    tipo: "Entrada" as const,
    categoria: "Dízimo",
    valor: 1500.00,
    data: "2024-01-20",
    descricao: "Dízimo Janeiro",
    metodo: "PIX"
  },
  {
    id: 2,
    tipo: "Entrada" as const,
    categoria: "Oferta",
    valor: 800.00,
    data: "2024-01-21",
    descricao: "Oferta Culto Dominical",
    metodo: "Dinheiro"
  },
  {
    id: 3,
    tipo: "Saída" as const,
    categoria: "Manutenção",
    valor: 350.00,
    data: "2024-01-22",
    descricao: "Reparo do ar condicionado",
    metodo: "Transferência"
  }
];

const categorias = [
  { nome: "Dízimos", valor: 15000, percentual: 60, cor: "bg-blue-500" },
  { nome: "Ofertas", valor: 6000, percentual: 24, cor: "bg-green-500" },
  { nome: "Doações", valor: 4000, percentual: 16, cor: "bg-purple-500" }
];

export default function FinancasVisualizacao() {
  const [showDoacao, setShowDoacao] = useState(false);
  const [valorDoacao, setValorDoacao] = useState("");
  const [categoriaDoacao, setCategoriaDoacao] = useState("");
  const [showQRCode, setShowQRCode] = useState(false);
  const { toast } = useToast();

  const totalEntradas = transacoes
    .filter(t => t.tipo === "Entrada")
    .reduce((acc, t) => acc + t.valor, 0);

  const totalSaidas = transacoes
    .filter(t => t.tipo === "Saída")
    .reduce((acc, t) => acc + t.valor, 0);

  const saldoAtual = totalEntradas - totalSaidas;

  const getTipoColor = (tipo: string) => {
    return tipo === "Entrada" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800";
  };

  const processarDoacao = () => {
    if (!valorDoacao || !categoriaDoacao) {
      toast({
        title: "Erro",
        description: "Por favor, preencha todos os campos",
        variant: "destructive"
      });
      return;
    }

    // Aqui será a integração com Django para processar a doação
    setShowQRCode(true);
    
    toast({
      title: "QR Code gerado",
      description: "Use o QR Code para finalizar sua doação",
    });
  };

  // Mock QR Code - será substituído pelo QR Code real do pastor
  const mockQRCodeData = {
    pastor: "Pastor João Silva",
    igreja: "Igreja Evangélica Alfa+",
    chave: "pastor@alfa.com.br",
    valor: valorDoacao,
    categoria: categoriaDoacao
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Finanças</h1>
          <p className="text-muted-foreground">Acompanhe a transparência financeira da igreja</p>
        </div>
        
        <Dialog open={showDoacao} onOpenChange={setShowDoacao}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Fazer Doação
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Nova Doação</DialogTitle>
              <DialogDescription>
                Preencha os dados para gerar o QR Code de doação
              </DialogDescription>
            </DialogHeader>
            
            <div className="space-y-4">
              <div>
                <Label htmlFor="valor">Valor da Doação (R$)</Label>
                <Input
                  id="valor"
                  type="number"
                  placeholder="0,00"
                  value={valorDoacao}
                  onChange={(e) => setValorDoacao(e.target.value)}
                />
              </div>
              
              <div>
                <Label htmlFor="categoria">Categoria</Label>
                <Select value={categoriaDoacao} onValueChange={setCategoriaDoacao}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione a categoria" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="dizimo">Dízimo</SelectItem>
                    <SelectItem value="oferta">Oferta</SelectItem>
                    <SelectItem value="doacao">Doação Especial</SelectItem>
                    <SelectItem value="missoes">Missões</SelectItem>
                    <SelectItem value="construcao">Construção</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {!showQRCode ? (
                <Button onClick={processarDoacao} className="w-full">
                  <QrCode className="h-4 w-4 mr-2" />
                  Gerar QR Code
                </Button>
              ) : (
                <div className="text-center space-y-4">
                  <div className="bg-muted p-8 rounded-lg">
                    <QrCode className="h-32 w-32 mx-auto text-muted-foreground" />
                    <p className="text-sm text-muted-foreground mt-2">QR Code para PIX</p>
                  </div>
                  
                  <div className="text-left space-y-2 bg-muted/50 p-4 rounded-lg">
                    <p><strong>Pastor:</strong> {mockQRCodeData.pastor}</p>
                    <p><strong>Igreja:</strong> {mockQRCodeData.igreja}</p>
                    <p><strong>Chave PIX:</strong> {mockQRCodeData.chave}</p>
                    <p><strong>Valor:</strong> R$ {valorDoacao}</p>
                    <p><strong>Categoria:</strong> {categoriaDoacao}</p>
                  </div>
                  
                  <p className="text-sm text-muted-foreground">
                    Escaneie o QR Code com seu app bancário ou copie a chave PIX
                  </p>
                </div>
              )}
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Resumo Financeiro */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Entradas</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              R$ {totalEntradas.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Saídas</CardTitle>
            <TrendingDown className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              R$ {totalSaidas.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Saldo Atual</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${saldoAtual >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              R$ {saldoAtual.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Entradas por Categoria */}
      <Card>
        <CardHeader>
          <CardTitle>Entradas por Categoria</CardTitle>
          <CardDescription>Distribuição das receitas por tipo</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {categorias.map((categoria, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${categoria.cor}`}></div>
                  <span className="font-medium">{categoria.nome}</span>
                </div>
                <div className="text-right">
                  <div className="font-medium">
                    R$ {categoria.valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </div>
                  <div className="text-sm text-muted-foreground">{categoria.percentual}%</div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Transações Recentes */}
      <Card>
        <CardHeader>
          <CardTitle>Transações Recentes</CardTitle>
          <CardDescription>Últimas movimentações financeiras</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Tipo</TableHead>
                <TableHead>Categoria</TableHead>
                <TableHead>Descrição</TableHead>
                <TableHead>Método</TableHead>
                <TableHead>Data</TableHead>
                <TableHead className="text-right">Valor</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {transacoes.map((transacao) => (
                <TableRow key={transacao.id}>
                  <TableCell>
                    <Badge className={getTipoColor(transacao.tipo)}>
                      {transacao.tipo}
                    </Badge>
                  </TableCell>
                  <TableCell>{transacao.categoria}</TableCell>
                  <TableCell>{transacao.descricao}</TableCell>
                  <TableCell>{transacao.metodo}</TableCell>
                  <TableCell>
                    {new Date(transacao.data).toLocaleDateString('pt-BR')}
                  </TableCell>
                  <TableCell className={`text-right font-medium ${
                    transacao.tipo === "Entrada" ? "text-green-600" : "text-red-600"
                  }`}>
                    {transacao.tipo === "Entrada" ? "+" : "-"}R$ {transacao.valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
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