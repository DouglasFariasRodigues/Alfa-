import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ArrowLeft, Save, DollarSign, Plus, Minus, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useCreateTransacao } from "@/hooks/useTransacoes";

export default function NovaTransacao() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const createTransacaoMutation = useCreateTransacao();
  
  const [formData, setFormData] = useState({
    tipo: "entrada" as "entrada" | "saida",
    categoria: "",
    descricao: "",
    valor: "",
    data: new Date().toISOString().split('T')[0],
    metodo_pagamento: "",
    observacoes: ""
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});

  const categoriasEntrada = [
    "Dízimo",
    "Oferta",
    "Doação",
    "Evento",
    "Venda",
    "Outros"
  ];

  const categoriasSaida = [
    "Manutenção",
    "Energia",
    "Água",
    "Internet",
    "Material",
    "Evento",
    "Salário",
    "Outros"
  ];

  const metodosPagamento = [
    "Dinheiro",
    "PIX",
    "Cartão de Débito",
    "Cartão de Crédito",
    "Transferência",
    "Cheque"
  ];

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Limpar erro do campo quando usuário começar a digitar
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: "" }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.tipo) {
      newErrors.tipo = "Tipo é obrigatório";
    }
    if (!formData.categoria.trim()) {
      newErrors.categoria = "Categoria é obrigatória";
    }
    if (!formData.descricao.trim()) {
      newErrors.descricao = "Descrição é obrigatória";
    }
    if (!formData.valor.trim()) {
      newErrors.valor = "Valor é obrigatório";
    } else if (isNaN(parseFloat(formData.valor)) || parseFloat(formData.valor) <= 0) {
      newErrors.valor = "Valor deve ser um número positivo";
    }
    if (!formData.data.trim()) {
      newErrors.data = "Data é obrigatória";
    }
    if (!formData.metodo_pagamento.trim()) {
      newErrors.metodo_pagamento = "Método de pagamento é obrigatório";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      toast({
        title: "Erro de validação",
        description: "Por favor, corrija os erros no formulário.",
        variant: "destructive",
      });
      return;
    }

    try {
      await createTransacaoMutation.mutateAsync({
        ...formData,
        valor: parseFloat(formData.valor)
      });
      
      toast({
        title: "Transação registrada com sucesso!",
        description: `${formData.tipo === 'entrada' ? 'Entrada' : 'Saída'} de R$ ${parseFloat(formData.valor).toFixed(2)} registrada.`,
      });
      navigate("/financas");
    } catch (error: any) {
      toast({
        title: "Erro ao registrar transação",
        description: error.response?.data?.message || "Erro inesperado. Tente novamente.",
        variant: "destructive",
      });
    }
  };

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
            Registre uma nova entrada ou saída financeira
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
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="tipo">Tipo *</Label>
                <Select
                  value={formData.tipo}
                  onValueChange={(value) => handleInputChange("tipo", value)}
                >
                  <SelectTrigger className={errors.tipo ? "border-red-500" : ""}>
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="entrada">
                      <div className="flex items-center gap-2">
                        <Plus className="h-4 w-4 text-green-600" />
                        Entrada
                      </div>
                    </SelectItem>
                    <SelectItem value="saida">
                      <div className="flex items-center gap-2">
                        <Minus className="h-4 w-4 text-red-600" />
                        Saída
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
                {errors.tipo && <p className="text-sm text-red-500">{errors.tipo}</p>}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="categoria">Categoria *</Label>
                <Select
                  value={formData.categoria}
                  onValueChange={(value) => handleInputChange("categoria", value)}
                >
                  <SelectTrigger className={errors.categoria ? "border-red-500" : ""}>
                    <SelectValue placeholder="Selecione a categoria" />
                  </SelectTrigger>
                  <SelectContent>
                    {(formData.tipo === "entrada" ? categoriasEntrada : categoriasSaida).map((categoria) => (
                      <SelectItem key={categoria} value={categoria}>
                        {categoria}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {errors.categoria && <p className="text-sm text-red-500">{errors.categoria}</p>}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="descricao">Descrição *</Label>
              <Input
                id="descricao"
                value={formData.descricao}
                onChange={(e) => handleInputChange("descricao", e.target.value)}
                placeholder="Descreva a transação..."
                className={errors.descricao ? "border-red-500" : ""}
              />
              {errors.descricao && <p className="text-sm text-red-500">{errors.descricao}</p>}
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="valor">Valor *</Label>
                <Input
                  id="valor"
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.valor}
                  onChange={(e) => handleInputChange("valor", e.target.value)}
                  placeholder="0,00"
                  className={errors.valor ? "border-red-500" : ""}
                />
                {errors.valor && <p className="text-sm text-red-500">{errors.valor}</p>}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="data">Data *</Label>
                <Input
                  id="data"
                  type="date"
                  value={formData.data}
                  onChange={(e) => handleInputChange("data", e.target.value)}
                  className={errors.data ? "border-red-500" : ""}
                />
                {errors.data && <p className="text-sm text-red-500">{errors.data}</p>}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="metodo_pagamento">Método de Pagamento *</Label>
              <Select
                value={formData.metodo_pagamento}
                onValueChange={(value) => handleInputChange("metodo_pagamento", value)}
              >
                <SelectTrigger className={errors.metodo_pagamento ? "border-red-500" : ""}>
                  <SelectValue placeholder="Selecione o método" />
                </SelectTrigger>
                <SelectContent>
                  {metodosPagamento.map((metodo) => (
                    <SelectItem key={metodo} value={metodo}>
                      {metodo}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.metodo_pagamento && <p className="text-sm text-red-500">{errors.metodo_pagamento}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="observacoes">Observações</Label>
              <Textarea
                id="observacoes"
                value={formData.observacoes}
                onChange={(e) => handleInputChange("observacoes", e.target.value)}
                placeholder="Informações adicionais sobre a transação..."
                rows={3}
              />
            </div>

            <div className="flex justify-end gap-3 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate("/financas")}
              >
                Cancelar
              </Button>
              <Button 
                type="submit" 
                disabled={createTransacaoMutation.isPending}
                className="flex items-center gap-2"
              >
                {createTransacaoMutation.isPending ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" />
                    Registrar Transação
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}