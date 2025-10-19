import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Save, Calendar, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useEvento, useUpdateEvento } from "@/hooks/useEventos";
import { Skeleton } from "@/components/ui/skeleton";

export default function EditarEvento() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { toast } = useToast();
  const updateEventoMutation = useUpdateEvento();
  
  const { data: evento, isLoading, error } = useEvento(Number(id));
  
  const [formData, setFormData] = useState({
    titulo: "",
    descricao: "",
    data: "",
    hora: "",
    local: "",
    observacoes: ""
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Preencher formulário quando os dados do evento carregarem
  useEffect(() => {
    if (evento) {
      // Separar data e hora do campo data do evento
      const dataHora = new Date(evento.data);
      const data = dataHora.toISOString().split('T')[0];
      const hora = dataHora.toTimeString().slice(0, 5);
      
      setFormData({
        titulo: evento.titulo || "",
        descricao: evento.descricao || "",
        data: data,
        hora: hora,
        local: evento.local || "",
        observacoes: evento.observacoes || ""
      });
    }
  }, [evento]);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Limpar erro do campo quando usuário começar a digitar
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: "" }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.titulo.trim()) {
      newErrors.titulo = "Título é obrigatório";
    }
    if (!formData.data.trim()) {
      newErrors.data = "Data é obrigatória";
    }
    if (!formData.hora.trim()) {
      newErrors.hora = "Hora é obrigatória";
    }
    if (!formData.local.trim()) {
      newErrors.local = "Local é obrigatório";
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
      // Combinar data e hora para o formato esperado pela API
      const dataHora = `${formData.data}T${formData.hora}:00`;
      
      // Preparar dados para envio, removendo campos vazios
      const eventoData = {
        titulo: formData.titulo,
        descricao: formData.descricao || '',
        data: dataHora,
        local: formData.local,
        observacoes: formData.observacoes || ''
      };
      
      await updateEventoMutation.mutateAsync({
        id: Number(id),
        ...eventoData
      });
      
      toast({
        title: "Evento atualizado com sucesso!",
        description: `${formData.titulo} foi atualizado no calendário.`,
      });
      navigate("/eventos");
    } catch (error: any) {
      toast({
        title: "Erro ao atualizar evento",
        description: error.response?.data?.message || "Erro inesperado. Tente novamente.",
        variant: "destructive",
      });
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center gap-4">
          <Skeleton className="h-10 w-20" />
          <div>
            <Skeleton className="h-8 w-48" />
            <Skeleton className="h-4 w-64 mt-2" />
          </div>
        </div>
        <Card>
          <CardHeader>
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-4 w-48" />
          </CardHeader>
          <CardContent className="space-y-4">
            <Skeleton className="h-10 w-full" />
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-10 w-full" />
            <Skeleton className="h-10 w-full" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error || !evento) {
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="outline" onClick={() => navigate("/eventos")}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Voltar
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Evento não encontrado</h1>
            <p className="text-muted-foreground">
              O evento solicitado não foi encontrado ou não existe.
            </p>
          </div>
        </div>
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-muted-foreground mb-4">
                Verifique se o ID do evento está correto.
              </p>
              <Button onClick={() => navigate("/eventos")}>
                Voltar para Eventos
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
      <div className="flex items-center gap-4">
        <Button
          variant="outline"
          onClick={() => navigate("/eventos")}
          className="flex items-center gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Editar Evento</h1>
          <p className="text-muted-foreground">
            Edite as informações de {evento.titulo}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Informações do Evento
            </CardTitle>
            <CardDescription>
              Edite os dados do evento
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="titulo">Título do Evento *</Label>
              <Input
                id="titulo"
                value={formData.titulo}
                onChange={(e) => handleInputChange("titulo", e.target.value)}
                placeholder="Ex: Culto de Domingo, Escola Bíblica, etc."
                className={errors.titulo ? "border-red-500" : ""}
              />
              {errors.titulo && <p className="text-sm text-red-500">{errors.titulo}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="descricao">Descrição</Label>
              <Textarea
                id="descricao"
                value={formData.descricao}
                onChange={(e) => handleInputChange("descricao", e.target.value)}
                placeholder="Descreva o evento, objetivos, público-alvo..."
                rows={4}
              />
            </div>

            <div className="grid gap-4 md:grid-cols-2">
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
              
              <div className="space-y-2">
                <Label htmlFor="hora">Hora *</Label>
                <Input
                  id="hora"
                  type="time"
                  value={formData.hora}
                  onChange={(e) => handleInputChange("hora", e.target.value)}
                  className={errors.hora ? "border-red-500" : ""}
                />
                {errors.hora && <p className="text-sm text-red-500">{errors.hora}</p>}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="local">Local *</Label>
              <Input
                id="local"
                value={formData.local}
                onChange={(e) => handleInputChange("local", e.target.value)}
                placeholder="Ex: Templo Principal, Salão de Eventos, etc."
                className={errors.local ? "border-red-500" : ""}
              />
              {errors.local && <p className="text-sm text-red-500">{errors.local}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="observacoes">Observações</Label>
              <Textarea
                id="observacoes"
                value={formData.observacoes}
                onChange={(e) => handleInputChange("observacoes", e.target.value)}
                placeholder="Informações adicionais, materiais necessários, etc."
                rows={3}
              />
            </div>

            <div className="flex justify-end gap-3 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate("/eventos")}
              >
                Cancelar
              </Button>
              <Button 
                type="submit" 
                disabled={updateEventoMutation.isPending}
                className="flex items-center gap-2"
              >
                {updateEventoMutation.isPending ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" />
                    Salvar Alterações
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