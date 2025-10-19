import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Edit, Users, Calendar, FileText, DollarSign, Gift } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { useCargo } from '@/hooks/useCargos'
import { Skeleton } from '@/components/ui/skeleton'

export default function DetalhesCargo() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  
  const { data: cargo, isLoading, error } = useCargo(Number(id))

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Skeleton className="h-10 w-10" />
          <div>
            <Skeleton className="h-8 w-48" />
            <Skeleton className="h-4 w-64 mt-2" />
          </div>
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <Skeleton className="h-6 w-32" />
              <Skeleton className="h-4 w-48" />
            </CardHeader>
            <CardContent className="space-y-4">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-4 w-1/2" />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <Skeleton className="h-6 w-32" />
            </CardHeader>
            <CardContent className="space-y-4">
              <Skeleton className="h-6 w-24" />
              <Skeleton className="h-6 w-24" />
              <Skeleton className="h-6 w-24" />
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  if (error || !cargo) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate('/cargos')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Cargo não encontrado</h1>
            <p className="text-muted-foreground">
              O cargo solicitado não foi encontrado ou não existe.
            </p>
          </div>
        </div>
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-muted-foreground mb-4">
                Verifique se o ID do cargo está correto.
              </p>
              <Button onClick={() => navigate('/cargos')}>
                Voltar para Cargos
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const permissions = [
    {
      key: 'pode_fazer_postagens',
      label: 'Criar Postagens',
      description: 'Pode criar e gerenciar postagens e notícias',
      icon: FileText,
      enabled: cargo.pode_fazer_postagens
    },
    {
      key: 'pode_registrar_dizimos',
      label: 'Registrar Dízimos',
      description: 'Pode registrar e gerenciar dízimos dos membros',
      icon: DollarSign,
      enabled: cargo.pode_registrar_dizimos
    },
    {
      key: 'pode_registrar_ofertas',
      label: 'Registrar Ofertas',
      description: 'Pode registrar e gerenciar ofertas e doações',
      icon: Gift,
      enabled: cargo.pode_registrar_ofertas
    }
  ]

  const enabledPermissions = permissions.filter(p => p.enabled)
  const disabledPermissions = permissions.filter(p => !p.enabled)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate('/cargos')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{cargo.nome}</h1>
            <p className="text-muted-foreground">
              Detalhes e informações do cargo
            </p>
          </div>
        </div>
        <Button onClick={() => navigate(`/cargos/editar/${cargo.id}`)}>
          <Edit className="h-4 w-4 mr-2" />
          Editar Cargo
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Informações Básicas */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              Informações Básicas
            </CardTitle>
            <CardDescription>
              Dados principais do cargo
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-medium text-sm text-muted-foreground">Nome</h4>
              <p className="text-lg font-semibold">{cargo.nome}</p>
            </div>
            
            {cargo.descricao && (
              <div>
                <h4 className="font-medium text-sm text-muted-foreground">Descrição</h4>
                <p className="text-sm">{cargo.descricao}</p>
              </div>
            )}
            
            <div>
              <h4 className="font-medium text-sm text-muted-foreground">Data de Criação</h4>
              <p className="text-sm flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                {new Date(cargo.data_criacao).toLocaleDateString('pt-BR', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Permissões */}
        <Card>
          <CardHeader>
            <CardTitle>Permissões</CardTitle>
            <CardDescription>
              Permissões atribuídas a este cargo
            </CardDescription>
          </CardHeader>
          <CardContent>
            {enabledPermissions.length > 0 ? (
              <div className="space-y-3">
                {enabledPermissions.map((permission) => {
                  const Icon = permission.icon
                  return (
                    <div key={permission.key} className="flex items-start gap-3 p-3 bg-green-50 dark:bg-green-950/20 rounded-lg border border-green-200 dark:border-green-800">
                      <Icon className="h-5 w-5 text-green-600 dark:text-green-400 mt-0.5" />
                      <div>
                        <p className="font-medium text-green-900 dark:text-green-100">
                          {permission.label}
                        </p>
                        <p className="text-sm text-green-700 dark:text-green-300">
                          {permission.description}
                        </p>
                      </div>
                    </div>
                  )
                })}
              </div>
            ) : (
              <div className="text-center py-6">
                <p className="text-muted-foreground">
                  Este cargo não possui permissões especiais
                </p>
              </div>
            )}

            {disabledPermissions.length > 0 && (
              <>
                <Separator className="my-4" />
                <div>
                  <h4 className="font-medium text-sm text-muted-foreground mb-3">
                    Permissões não atribuídas
                  </h4>
                  <div className="space-y-2">
                    {disabledPermissions.map((permission) => {
                      const Icon = permission.icon
                      return (
                        <div key={permission.key} className="flex items-center gap-2 text-muted-foreground">
                          <Icon className="h-4 w-4" />
                          <span className="text-sm">{permission.label}</span>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Estatísticas */}
      <Card>
        <CardHeader>
          <CardTitle>Estatísticas</CardTitle>
          <CardDescription>
            Informações sobre o uso deste cargo
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <Users className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">0</p>
              <p className="text-sm text-muted-foreground">Administradores</p>
            </div>
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <Users className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">0</p>
              <p className="text-sm text-muted-foreground">Usuários</p>
            </div>
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <Calendar className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">
                {Math.floor((Date.now() - new Date(cargo.data_criacao).getTime()) / (1000 * 60 * 60 * 24))}
              </p>
              <p className="text-sm text-muted-foreground">Dias ativo</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
