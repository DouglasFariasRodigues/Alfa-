import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ArrowLeft, Save, DollarSign, Plus, Minus } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function NovaTransacao() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    tipo: "",
    categoria: "",
    descricao: "",
    valor: "",
    data: new Date().toISOString().split('T')[0],
    metodoPagamento: "",
    observacoes: ""
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/api/transacoes/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tipo: formData.tipo,
          categoria: formData.categoria,
          valor: parseFloat(formData.valor),
          data: formData.data,
          descricao: formData.descricao,
          metodoPagamento: formData.metodoPagamento,
          observacoes: formData.observacoes,
        }),
      });

      const data = await response.json();

      if (data.success) {
        const tipoTexto = formData.tipo === "entrada" ? "receita" : "despesa";
        toast({
          title: `${tipoTexto.charAt(0).toUpperCase() + tipoTexto.slice(1)} registrada com sucesso!`,
          description: `Transação de R$ ${formData.valor} foi adicionada.`,
        });
        navigate("/financas");
      } else {
        toast({
          title: "Erro ao registrar transação",
          description: data.message,
          variant: "destructive",
        });
      }
    } catch (error) {
      toast({
        title: "Erro de conexão",
        description: "Não foi possível conectar ao servidor. Tente novamente.",
        variant: "destructive",
      });
    }
  };

  const categoriesReceita = [
    "Dízimos",
    "Ofertas",
    "Doações",
    "Eventos",
    "Vendas",
    "Outros"
  ];

  const categoriesDespesa = [
    "Manutenção",
    "Luz",
    "Água",
    "Internet",
    "Material de Escritório",
    "Eventos",
    "Ministérios",
    "Outros"
  ];

  const metodosPagamento = [
    "Dinheiro",
    "PIX",
    "Cartão de Débito",
    "Cartão de Crédito",
    "Transferência Bancária",
    "Cheque"
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button
          variant="outline"
          onClick={() => navigate("/financas")}
          className="flex items-center gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Nova Transação</h1>
          <p className="text-muted-foreground">
            Registre uma nova receita ou despesa
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="h-5 w-5" />
              Informações da Transação
            </CardTitle>
            <CardDescription>
              Preencha os dados da transação financeira
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Tipo de Transação */}
            <div className="space-y-2">
              <Label>Tipo de Transação *</Label>
              <div className="grid grid-cols-2 gap-4">
                <Button
                  type="button"
                  variant={formData.tipo === "entrada" ? "default" : "outline"}
                  onClick={() => handleInputChange("tipo", "entrada")}
                  className={formData.tipo === "entrada" ? "gradient-primary text-white" : ""}
                >
                  <Plus className="mr-2 h-4 w-4" />
                  Receita
                </Button>
                <Button
                  type="button"
                  variant={formData.tipo === "saida" ? "default" : "outline"}
                  onClick={() => handleInputChange("tipo", "saida")}
                  className={formData.tipo === "saida" ? "bg-red-600 text-white hover:bg-red-700" : ""}
                >
                  <Minus className="mr-2 h-4 w-4" />
                  Despesa
                </Button>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="valor">Valor *</Label>
                <div className="relative">
                  <span className="absolute left-3 top-2.5 text-muted-foreground">R$</span>
                  <Input
                    id="valor"
                    type="number"
                    step="0.01"
                    min="0"
                    value={formData.valor}
                    onChange={(e) => handleInputChange("valor", e.target.value)}
                    className="pl-8"
                    placeholder="0,00"
                    required
                  />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="data">Data *</Label>
                <Input
                  id="data"
                  type="date"
                  value={formData.data}
                  onChange={(e) => handleInputChange("data", e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="categoria">Categoria *</Label>
                <Select onValueChange={(value) => handleInputChange("categoria", value)} disabled={!formData.tipo}>
                  <SelectTrigger>
                    <SelectValue placeholder={formData.tipo ? "Selecione a categoria..." : "Primeiro selecione o tipo"} />
                  </SelectTrigger>
                  <SelectContent>
                    {(formData.tipo === "entrada" ? categoriesReceita : categoriesDespesa).map((categoria) => (
                      <SelectItem key={categoria} value={categoria}>
                        {categoria}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="metodoPagamento">Método de Pagamento *</Label>
                <Select onValueChange={(value) => handleInputChange("metodoPagamento", value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o método..." />
                  </SelectTrigger>
                  <SelectContent>
                    {metodosPagamento.map((metodo) => (
                      <SelectItem key={metodo} value={metodo}>
                        {metodo}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="descricao">Descrição *</Label>
              <Input
                id="descricao"
                value={formData.descricao}
                onChange={(e) => handleInputChange("descricao", e.target.value)}
                placeholder="Ex: Dízimo - Maria Santos"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="observacoes">Observações</Label>
              <Textarea
                id="observacoes"
                value={formData.observacoes}
                onChange={(e) => handleInputChange("observacoes", e.target.value)}
                placeholder="Informações adicionais..."
                rows={3}
              />
            </div>

            <div className="flex gap-4 pt-4">
              <Button 
                type="submit" 
                className="gradient-primary text-white shadow-elegant hover:opacity-90"
                disabled={!formData.tipo}
              >
                <Save className="mr-2 h-4 w-4" />
                Registrar Transação
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate("/financas")}
              >
                Cancelar
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}