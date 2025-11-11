import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Save, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { usePostagem, useUpdatePostagem } from "@/hooks/usePostagens";
import { Skeleton } from "@/components/ui/skeleton";

export default function EditarPostagem() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { toast } = useToast();
  const updatePostagemMutation = useUpdatePostagem();
  
  const { data: postagem, isLoading, error } = usePostagem(Number(id));
  
  const [formData, setFormData] = useState({
    titulo: "",
    conteudo: ""
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Preencher formulário quando os dados da postagem carregarem
  useEffect(() => {
    if (postagem) {
      setFormData({
        titulo: postagem.titulo || "",
        conteudo: postagem.conteudo || ""
      });
    }
  }, [postagem]);

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

    if (!id) {
      toast({
        title: "Erro",
        description: "ID da postagem não encontrado.",
        variant: "destructive",
      });
      return;
    }

    try {
      await updatePostagemMutation.mutateAsync({
        id: Number(id),
        postagem: {
          titulo: formData.titulo.trim(),
          conteudo: formData.conteudo.trim()
        }
      });
      
      toast({
        title: "Sucesso!",
        description: "Postagem atualizada com sucesso!",
      });
      
      navigate(`/postagens/${id}`);
    } catch (error: any) {
      console.error('Erro ao atualizar postagem:', error);
      toast({
        title: "Erro",
        description: error?.message || "Erro ao atualizar postagem. Tente novamente.",
        variant: "destructive",
      });
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center gap-4">
          <Skeleton className="h-10 w-10" />
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
            <Skeleton className="h-40 w-full" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error || !postagem) {
    return (
      <div className="p-6">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-600">Erro ao carregar postagem</h2>
          <p className="text-gray-600">Postagem não encontrada ou erro ao carregar dados</p>
          <Button 
            onClick={() => navigate('/postagens')}
            className="mt-4"
          >
            Voltar para Postagens
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => navigate(`/postagens/${id}`)}
        >
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Editar Postagem</h1>
          <p className="text-muted-foreground">
            Edite as informações da postagem
          </p>
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit}>
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle>Informações da Postagem</CardTitle>
            <CardDescription>
              Edite os dados da postagem
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
                onClick={() => navigate(`/postagens/${id}`)}
                disabled={updatePostagemMutation.isPending}
              >
                Cancelar
              </Button>
              <Button
                type="submit"
                className="gradient-primary text-white shadow-elegant hover:opacity-90"
                disabled={updatePostagemMutation.isPending}
              >
                {updatePostagemMutation.isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="mr-2 h-4 w-4" />
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

