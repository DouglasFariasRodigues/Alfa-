import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Save, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useCreatePostagem } from "@/hooks/usePostagens";

export default function NovaPostagem() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const createPostagemMutation = useCreatePostagem();
  
  const [formData, setFormData] = useState({
    titulo: "",
    conteudo: ""
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});

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
    } else if (formData.titulo.trim().length < 3) {
      newErrors.titulo = "Título deve ter pelo menos 3 caracteres";
    }

    if (!formData.conteudo.trim()) {
      newErrors.conteudo = "Conteúdo é obrigatório";
    } else if (formData.conteudo.trim().length < 10) {
      newErrors.conteudo = "Conteúdo deve ter pelo menos 10 caracteres";
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
      await createPostagemMutation.mutateAsync({
        titulo: formData.titulo.trim(),
        conteudo: formData.conteudo.trim()
      });
      
      toast({
        title: "Sucesso!",
        description: "Postagem criada com sucesso!",
      });
      
      navigate('/postagens');
    } catch (error: any) {
      console.error('Erro ao criar postagem:', error);
      toast({
        title: "Erro",
        description: error?.message || "Erro ao criar postagem. Tente novamente.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => navigate('/postagens')}
        >
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Nova Postagem</h1>
          <p className="text-muted-foreground">
            Crie uma nova postagem ou notícia para a igreja
          </p>
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit}>
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle>Informações da Postagem</CardTitle>
            <CardDescription>
              Preencha os dados da postagem que será publicada
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Título */}
            <div className="space-y-2">
              <Label htmlFor="titulo">Título *</Label>
              <Input
                id="titulo"
                placeholder="Digite o título da postagem"
                value={formData.titulo}
                onChange={(e) => handleInputChange("titulo", e.target.value)}
                className={errors.titulo ? "border-red-500" : ""}
                maxLength={200}
              />
              {errors.titulo && (
                <p className="text-sm text-red-500">{errors.titulo}</p>
              )}
              <p className="text-xs text-muted-foreground">
                {formData.titulo.length}/200 caracteres
              </p>
            </div>

            {/* Conteúdo */}
            <div className="space-y-2">
              <Label htmlFor="conteudo">Conteúdo *</Label>
              <Textarea
                id="conteudo"
                placeholder="Digite o conteúdo da postagem..."
                value={formData.conteudo}
                onChange={(e) => handleInputChange("conteudo", e.target.value)}
                className={errors.conteudo ? "border-red-500" : ""}
                rows={10}
              />
              {errors.conteudo && (
                <p className="text-sm text-red-500">{errors.conteudo}</p>
              )}
              <p className="text-xs text-muted-foreground">
                {formData.conteudo.length} caracteres
              </p>
            </div>

            {/* Actions */}
            <div className="flex justify-end gap-4 pt-4 border-t">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate('/postagens')}
                disabled={createPostagemMutation.isPending}
              >
                Cancelar
              </Button>
              <Button
                type="submit"
                className="gradient-primary text-white shadow-elegant hover:opacity-90"
                disabled={createPostagemMutation.isPending}
              >
                {createPostagemMutation.isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
                    Salvar Postagem
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

