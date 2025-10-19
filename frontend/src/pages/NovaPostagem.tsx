import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Save, FileText, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useCreatePostagem, useUpdatePostagem, usePostagem } from "@/hooks/usePostagens";
import { Skeleton } from "@/components/ui/skeleton";

export default function NovaPostagem() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { toast } = useToast();
  const isEditing = !!id;
  
  const createPostagemMutation = useCreatePostagem();
  const updatePostagemMutation = useUpdatePostagem();
  const { data: postagem, isLoading, error } = usePostagem(Number(id));
  
  const [formData, setFormData] = useState({
    titulo: "",
    conteudo: ""
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Preencher formulário quando os dados da postagem carregarem (modo edição)
  useEffect(() => {
    if (isEditing && postagem) {
      setFormData({
        titulo: postagem.titulo || "",
        conteudo: postagem.conteudo || ""
      });
    }
  }, [isEditing, postagem]);

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
      if (isEditing) {
        await updatePostagemMutation.mutateAsync({
          id: Number(id),
          ...formData
        });
        
        toast({
          title: "Postagem atualizada com sucesso!",
          description: `${formData.titulo} foi atualizada.`,
        });
      } else {
        await createPostagemMutation.mutateAsync(formData);
        
        toast({
          title: "Postagem criada com sucesso!",
          description: `${formData.titulo} foi publicada.`,
        });
      }
      
      navigate("/postagens");
    } catch (error: any) {
      toast({
        title: `Erro ao ${isEditing ? 'atualizar' : 'criar'} postagem`,
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
            <Skeleton className="h-40 w-full" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error || (isEditing && !postagem)) {
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="outline" onClick={() => navigate("/postagens")}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Voltar
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              {isEditing ? 'Postagem não encontrada' : 'Nova Postagem'}
            </h1>
            <p className="text-muted-foreground">
              {isEditing 
                ? 'A postagem solicitada não foi encontrada ou não existe.'
                : 'Crie uma nova postagem para a igreja'
              }
            </p>
          </div>
        </div>
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-muted-foreground mb-4">
                {isEditing 
                  ? 'Verifique se o ID da postagem está correto.'
                  : 'Preencha os campos abaixo para criar uma nova postagem.'
                }
              </p>
              <Button onClick={() => navigate("/postagens")}>
                Voltar para Postagens
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  const isSubmitting = createPostagemMutation.isPending || updatePostagemMutation.isPending;

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button
          variant="outline"
          onClick={() => navigate("/postagens")}
          className="flex items-center gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            {isEditing ? 'Editar Postagem' : 'Nova Postagem'}
          </h1>
          <p className="text-muted-foreground">
            {isEditing 
              ? `Edite a postagem: ${postagem?.titulo}`
              : 'Crie uma nova postagem para a igreja'
            }
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              {isEditing ? 'Editar Postagem' : 'Informações da Postagem'}
            </CardTitle>
            <CardDescription>
              {isEditing 
                ? 'Edite os dados da postagem'
                : 'Preencha os dados da nova postagem'
              }
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="titulo">Título da Postagem *</Label>
              <Input
                id="titulo"
                value={formData.titulo}
                onChange={(e) => handleInputChange("titulo", e.target.value)}
                placeholder="Digite o título da postagem"
                className={errors.titulo ? "border-red-500" : ""}
              />
              {errors.titulo && <p className="text-sm text-red-500">{errors.titulo}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="conteudo">Conteúdo da Postagem *</Label>
              <Textarea
                id="conteudo"
                value={formData.conteudo}
                onChange={(e) => handleInputChange("conteudo", e.target.value)}
                placeholder="Escreva o conteúdo da postagem aqui..."
                rows={12}
                className={errors.conteudo ? "border-red-500" : ""}
              />
              {errors.conteudo && <p className="text-sm text-red-500">{errors.conteudo}</p>}
              <p className="text-sm text-muted-foreground">
                {formData.conteudo.length} caracteres
              </p>
            </div>

            {/* Preview */}
            {formData.titulo && formData.conteudo && (
              <div className="space-y-2">
                <Label>Preview da Postagem</Label>
                <div className="p-4 border rounded-lg bg-muted/50">
                  <h3 className="text-lg font-semibold mb-2">{formData.titulo}</h3>
                  <div className="text-sm text-muted-foreground whitespace-pre-wrap">
                    {formData.conteudo}
                  </div>
                </div>
              </div>
            )}

            <div className="flex justify-end gap-3 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate("/postagens")}
              >
                Cancelar
              </Button>
              <Button 
                type="submit" 
                disabled={isSubmitting}
                className="flex items-center gap-2"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    {isEditing ? 'Salvando...' : 'Publicando...'}
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" />
                    {isEditing ? 'Salvar Alterações' : 'Publicar Postagem'}
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
