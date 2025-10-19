import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Save, Calendar, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useCreateEvento } from "@/hooks/useEventos";
import { ImageUpload } from "@/components/ui/ImageUpload";
import { useImageUpload } from "@/hooks/useImageUpload";

export default function NovoEvento() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const createEventoMutation = useCreateEvento();
  const { uploadImage } = useImageUpload();
  
  const [formData, setFormData] = useState({
    titulo: "",
    descricao: "",
    data: "",
    hora: "",
    local: "",
    observacoes: ""
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [fotosUrls, setFotosUrls] = useState<string[]>([]);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Limpar erro do campo quando usuário começar a digitar
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: "" }));
    }
  };

  const handleImageUpload = async (file: File): Promise<string> => {
    try {
      const result = await uploadImage(file, 'eventos');
      setFotosUrls(prev => [...prev, result.url]);
      return result.url;
    } catch (error: any) {
      throw new Error(error.message || 'Erro ao fazer upload da foto');
    }
  };

  const handleRemoveImage = (url: string) => {
    setFotosUrls(prev => prev.filter(fotoUrl => fotoUrl !== url));
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
        observacoes: formData.observacoes || '',
        fotos: fotosUrls.length > 0 ? fotosUrls : undefined
      };
      
      await createEventoMutation.mutateAsync(eventoData);
      
      toast({
        title: "Evento criado com sucesso!",
        description: `${formData.titulo} foi adicionado ao calendário.`,
      });
      navigate("/eventos");
    } catch (error: any) {
      toast({
        title: "Erro ao criar evento",
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
          onClick={() => navigate("/eventos")}
          className="flex items-center gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Novo Evento</h1>
          <p className="text-muted-foreground">
            Crie um novo evento para a comunidade
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
              Preencha os dados do novo evento
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
              <Label>Fotos do Evento</Label>
              <ImageUpload
                onUpload={handleImageUpload}
                onRemove={handleRemoveImage}
                existingImages={fotosUrls}
                maxImages={5}
                maxSize={5}
              />
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
                disabled={createEventoMutation.isPending}
                className="flex items-center gap-2"
              >
                {createEventoMutation.isPending ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" />
                    Criar Evento
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