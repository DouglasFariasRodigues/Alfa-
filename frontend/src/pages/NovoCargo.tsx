import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Save, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { useCreateCargo, useUpdateCargo, useCargo, type CargoCreate } from '@/hooks/useCargos'
import { toast } from '@/hooks/use-toast'
import { Skeleton } from '@/components/ui/skeleton'

export default function NovoCargo() {
  const navigate = useNavigate()
  const { id } = useParams<{ id: string }>()
  const isEditing = !!id

  const [formData, setFormData] = useState<CargoCreate>({
    nome: '',
    descricao: '',
    pode_registrar_dizimos: false,
    pode_registrar_ofertas: false,
    pode_gerenciar_membros: false,
    pode_gerenciar_eventos: false,
    pode_gerenciar_financas: false,
    pode_gerenciar_cargos: false,
    pode_gerenciar_documentos: false,
    pode_visualizar_relatorios: false,
  })

  const [errors, setErrors] = useState<Partial<CargoCreate>>({})

  // Hooks
  const { data: cargo, isLoading: isLoadingCargo } = useCargo(Number(id))
  const createCargoMutation = useCreateCargo()
  const updateCargoMutation = useUpdateCargo()

  // Preencher formulário quando editando
  useState(() => {
    if (isEditing && cargo) {
      setFormData({
        nome: cargo.nome,
        descricao: cargo.descricao || '',
        pode_registrar_dizimos: cargo.pode_registrar_dizimos,
        pode_registrar_ofertas: cargo.pode_registrar_ofertas,
        pode_gerenciar_membros: cargo.pode_gerenciar_membros,
        pode_gerenciar_eventos: cargo.pode_gerenciar_eventos,
        pode_gerenciar_financas: cargo.pode_gerenciar_financas,
        pode_gerenciar_cargos: cargo.pode_gerenciar_cargos,
        pode_gerenciar_documentos: cargo.pode_gerenciar_documentos,
        pode_visualizar_relatorios: cargo.pode_visualizar_relatorios,
      })
    }
  })

  const handleInputChange = (field: keyof CargoCreate, value: string | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
    
    // Limpar erro do campo quando usuário começar a digitar
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: undefined
      }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Partial<CargoCreate> = {}

    if (!formData.nome.trim()) {
      newErrors.nome = 'Nome é obrigatório'
    } else if (formData.nome.length < 2) {
      newErrors.nome = 'Nome deve ter pelo menos 2 caracteres'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validateForm()) {
      toast({
        title: "Erro de validação",
        description: "Por favor, corrija os erros no formulário.",
        variant: "destructive",
      })
      return
    }

    try {
      if (isEditing) {
        await updateCargoMutation.mutateAsync({
          id: Number(id),
          ...formData
        })
        toast({
          title: "Sucesso",
          description: "Cargo atualizado com sucesso!",
        })
      } else {
        await createCargoMutation.mutateAsync(formData)
        toast({
          title: "Sucesso",
          description: "Cargo criado com sucesso!",
        })
      }
      
      navigate('/cargos')
    } catch (error: any) {
      toast({
        title: "Erro",
        description: error.response?.data?.message || "Erro ao salvar cargo. Tente novamente.",
        variant: "destructive",
      })
    }
  }

  const handleCancel = () => {
    navigate('/cargos')
  }

  if (isEditing && isLoadingCargo) {
    return (
      <div className="space-y-6">
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
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-6 w-32" />
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={handleCancel}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">
            {isEditing ? 'Editar Cargo' : 'Novo Cargo'}
          </h1>
          <p className="text-muted-foreground">
            {isEditing 
              ? 'Edite as informações do cargo' 
              : 'Crie um novo cargo com suas permissões'
            }
          </p>
        </div>
      </div>

      {/* Formulário */}
      <Card>
        <CardHeader>
          <CardTitle>Informações do Cargo</CardTitle>
          <CardDescription>
            Preencha as informações básicas e defina as permissões do cargo
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Nome */}
            <div className="space-y-2">
              <Label htmlFor="nome">Nome do Cargo *</Label>
              <Input
                id="nome"
                value={formData.nome}
                onChange={(e) => handleInputChange('nome', e.target.value)}
                placeholder="Ex: Pastor, Diácono, Tesoureiro..."
                className={errors.nome ? 'border-red-500' : ''}
              />
              {errors.nome && (
                <p className="text-sm text-red-500">{errors.nome}</p>
              )}
            </div>

            {/* Descrição */}
            <div className="space-y-2">
              <Label htmlFor="descricao">Descrição</Label>
              <Textarea
                id="descricao"
                value={formData.descricao}
                onChange={(e) => handleInputChange('descricao', e.target.value)}
                placeholder="Descreva as responsabilidades e funções deste cargo..."
                rows={3}
              />
            </div>

            {/* Permissões */}
            <div className="space-y-4">
              <Label className="text-base font-medium">Permissões</Label>
              <p className="text-sm text-muted-foreground">
                Selecione as permissões que este cargo terá no sistema
              </p>
              
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="pode_registrar_dizimos"
                    checked={formData.pode_registrar_dizimos}
                    onCheckedChange={(checked) => 
                      handleInputChange('pode_registrar_dizimos', !!checked)
                    }
                  />
                  <Label htmlFor="pode_registrar_dizimos" className="text-sm font-medium">
                    Pode registrar dízimos
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground ml-6">
                  Permite registrar e gerenciar dízimos dos membros
                </p>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="pode_registrar_ofertas"
                    checked={formData.pode_registrar_ofertas}
                    onCheckedChange={(checked) => 
                      handleInputChange('pode_registrar_ofertas', !!checked)
                    }
                  />
                  <Label htmlFor="pode_registrar_ofertas" className="text-sm font-medium">
                    Pode registrar ofertas
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground ml-6">
                  Permite registrar e gerenciar ofertas e doações
                </p>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="pode_gerenciar_membros"
                    checked={formData.pode_gerenciar_membros}
                    onCheckedChange={(checked) => 
                      handleInputChange('pode_gerenciar_membros', !!checked)
                    }
                  />
                  <Label htmlFor="pode_gerenciar_membros" className="text-sm font-medium">
                    Pode gerenciar membros
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground ml-6">
                  Permite criar, editar e gerenciar membros da igreja
                </p>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="pode_gerenciar_eventos"
                    checked={formData.pode_gerenciar_eventos}
                    onCheckedChange={(checked) => 
                      handleInputChange('pode_gerenciar_eventos', !!checked)
                    }
                  />
                  <Label htmlFor="pode_gerenciar_eventos" className="text-sm font-medium">
                    Pode gerenciar eventos
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground ml-6">
                  Permite criar, editar e gerenciar eventos da igreja
                </p>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="pode_gerenciar_financas"
                    checked={formData.pode_gerenciar_financas}
                    onCheckedChange={(checked) => 
                      handleInputChange('pode_gerenciar_financas', !!checked)
                    }
                  />
                  <Label htmlFor="pode_gerenciar_financas" className="text-sm font-medium">
                    Pode gerenciar finanças
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground ml-6">
                  Permite gerenciar transações financeiras e relatórios
                </p>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="pode_gerenciar_cargos"
                    checked={formData.pode_gerenciar_cargos}
                    onCheckedChange={(checked) => 
                      handleInputChange('pode_gerenciar_cargos', !!checked)
                    }
                  />
                  <Label htmlFor="pode_gerenciar_cargos" className="text-sm font-medium">
                    Pode gerenciar cargos
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground ml-6">
                  Permite criar e gerenciar cargos e permissões
                </p>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="pode_gerenciar_documentos"
                    checked={formData.pode_gerenciar_documentos}
                    onCheckedChange={(checked) => 
                      handleInputChange('pode_gerenciar_documentos', !!checked)
                    }
                  />
                  <Label htmlFor="pode_gerenciar_documentos" className="text-sm font-medium">
                    Pode gerenciar documentos
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground ml-6">
                  Permite gerenciar documentos e certificados
                </p>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="pode_visualizar_relatorios"
                    checked={formData.pode_visualizar_relatorios}
                    onCheckedChange={(checked) => 
                      handleInputChange('pode_visualizar_relatorios', !!checked)
                    }
                  />
                  <Label htmlFor="pode_visualizar_relatorios" className="text-sm font-medium">
                    Pode visualizar relatórios
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground ml-6">
                  Permite visualizar relatórios e estatísticas do sistema
                </p>
              </div>
            </div>

            {/* Botões */}
            <div className="flex justify-end gap-3 pt-4">
              <Button type="button" variant="outline" onClick={handleCancel}>
                <X className="h-4 w-4 mr-2" />
                Cancelar
              </Button>
              <Button 
                type="submit" 
                disabled={createCargoMutation.isPending || updateCargoMutation.isPending}
              >
                <Save className="h-4 w-4 mr-2" />
                {createCargoMutation.isPending || updateCargoMutation.isPending 
                  ? 'Salvando...' 
                  : isEditing ? 'Atualizar' : 'Criar Cargo'
                }
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
