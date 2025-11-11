import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Search, Edit, Trash2, Shield, FileText, DollarSign, Gift, Eye } from 'lucide-react'
import { usePermissions } from '@/hooks/usePermissions'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog'
import { useCargos, useDeleteCargo, type Cargo, type CargoFilters } from '@/hooks/useCargos'
import { toast } from 'sonner'
import { Skeleton } from '@/components/ui/skeleton'

export default function Cargos() {
  const navigate = useNavigate()
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCargo, setSelectedCargo] = useState<Cargo | null>(null)
  const [showDeleteDialog, setShowDeleteDialog] = useState(false)
  const [filters, setFilters] = useState<CargoFilters>({})
  const { canManage } = usePermissions()
  
  // Verificar se o usuário pode gerenciar cargos (criar, editar, deletar)
  const canManageCargos = canManage('cargos')

  const { data: cargos = [], isLoading, error } = useCargos(filters)
  const deleteCargoMutation = useDeleteCargo()

  // Filtrar cargos localmente por busca
  const filteredCargos = cargos.filter((cargo: Cargo) =>
    cargo.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (cargo.descricao && cargo.descricao.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  const handleDelete = async () => {
    if (!selectedCargo) return

    try {
      await deleteCargoMutation.mutateAsync(selectedCargo.id)
      toast.success("Cargo excluído com sucesso!")
      setShowDeleteDialog(false)
      setSelectedCargo(null)
    } catch (error) {
      toast.error("Erro ao excluir cargo. Tente novamente.")
    }
  }

  const handleFilterChange = (key: keyof CargoFilters, value: boolean | undefined) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const getPermissionIcon = (permission: string) => {
    switch (permission) {
      case 'postagens':
        return <FileText className="h-4 w-4" />
      case 'dizimos':
        return <DollarSign className="h-4 w-4" />
      case 'ofertas':
        return <Gift className="h-4 w-4" />
      default:
        return <Shield className="h-4 w-4" />
    }
  }

  const getPermissionLabel = (permission: string) => {
    switch (permission) {
      case 'postagens':
        return 'Postagens'
      case 'dizimos':
        return 'Dízimos'
      case 'ofertas':
        return 'Ofertas'
      default:
        return permission
    }
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <Card className="w-full max-w-md">
          <CardContent>
            <div className="text-center">
              <p className="text-red-500 mb-4">Erro ao carregar cargos</p>
              <Button onClick={() => window.location.reload()}>
                Tentar Novamente
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Cargos</h1>
          <p className="text-muted-foreground">
            Gerencie os cargos e permissões do sistema
          </p>
        </div>
        {canManageCargos && (
          <Button onClick={() => navigate('/cargos/novo')}>
            <Plus className="h-4 w-4 mr-2" />
            Novo Cargo
          </Button>
        )}
      </div>

      {/* Estatísticas */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Cargos</CardTitle>
            <Shield className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? <Skeleton className="h-8 w-16" /> : cargos.length}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Com Postagens</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? <Skeleton className="h-8 w-16" /> : cargos.filter((c: Cargo) => c.pode_fazer_postagens).length}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Com Dízimos</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? <Skeleton className="h-8 w-16" /> : cargos.filter((c: Cargo) => c.pode_registrar_dizimos).length}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Com Ofertas</CardTitle>
            <Gift className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {isLoading ? <Skeleton className="h-8 w-16" /> : cargos.filter((c: Cargo) => c.pode_registrar_ofertas).length}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filtros */}
      <Card>
        <CardHeader>
          <CardTitle>Filtros</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  placeholder="Buscar por nome ou descrição..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            
            <div className="flex gap-2 flex-wrap">
              <Button
                variant={filters.pode_fazer_postagens === true ? "default" : "outline"}
                size="sm"
                onClick={() => handleFilterChange('pode_fazer_postagens', 
                  filters.pode_fazer_postagens === true ? undefined : true
                )}
              >
                <FileText className="h-4 w-4 mr-1" />
                Postagens
              </Button>
              
              <Button
                variant={filters.pode_registrar_dizimos === true ? "default" : "outline"}
                size="sm"
                onClick={() => handleFilterChange('pode_registrar_dizimos', 
                  filters.pode_registrar_dizimos === true ? undefined : true
                )}
              >
                <DollarSign className="h-4 w-4 mr-1" />
                Dízimos
              </Button>
              
              <Button
                variant={filters.pode_registrar_ofertas === true ? "default" : "outline"}
                size="sm"
                onClick={() => handleFilterChange('pode_registrar_ofertas', 
                  filters.pode_registrar_ofertas === true ? undefined : true
                )}
              >
                <Gift className="h-4 w-4 mr-1" />
                Ofertas
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tabela de Cargos */}
      <Card>
        <CardHeader>
          <CardTitle>Cargos ({filteredCargos.length})</CardTitle>
          <CardDescription>
            Lista de todos os cargos cadastrados no sistema
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="flex items-center space-x-4">
                  <Skeleton className="h-4 w-[200px]" />
                  <Skeleton className="h-4 w-[300px]" />
                  <Skeleton className="h-4 w-[100px]" />
                </div>
              ))}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Nome</TableHead>
                  <TableHead>Descrição</TableHead>
                  <TableHead>Permissões</TableHead>
                  <TableHead>Data de Criação</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredCargos.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-8">
                      <div className="text-muted-foreground">
                        {searchTerm ? 'Nenhum cargo encontrado para a busca.' : 'Nenhum cargo cadastrado.'}
                      </div>
                    </TableCell>
                  </TableRow>
                ) : (
                  filteredCargos.map((cargo: Cargo) => (
                    <TableRow key={cargo.id}>
                      <TableCell className="font-medium">{cargo.nome}</TableCell>
                      <TableCell>
                        {cargo.descricao ? (
                          <span className="text-muted-foreground">
                            {cargo.descricao.length > 50 
                              ? `${cargo.descricao.substring(0, 50)}...` 
                              : cargo.descricao
                            }
                          </span>
                        ) : (
                          <span className="text-muted-foreground">-</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="flex gap-1 flex-wrap">
                          {cargo.pode_fazer_postagens && (
                            <Badge variant="secondary" className="text-xs">
                              <FileText className="h-3 w-3 mr-1" />
                              Postagens
                            </Badge>
                          )}
                          {cargo.pode_registrar_dizimos && (
                            <Badge variant="secondary" className="text-xs">
                              <DollarSign className="h-3 w-3 mr-1" />
                              Dízimos
                            </Badge>
                          )}
                          {cargo.pode_registrar_ofertas && (
                            <Badge variant="secondary" className="text-xs">
                              <Gift className="h-3 w-3 mr-1" />
                              Ofertas
                            </Badge>
                          )}
                          {!cargo.pode_fazer_postagens && !cargo.pode_registrar_dizimos && !cargo.pode_registrar_ofertas && (
                            <Badge variant="outline" className="text-xs">
                              Sem permissões especiais
                            </Badge>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        {new Date(cargo.data_criacao).toLocaleDateString('pt-BR')}
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              Ações
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem onClick={() => navigate(`/cargos/${cargo.id}`)}>
                              <Eye className="h-4 w-4 mr-2" />
                              Ver Detalhes
                            </DropdownMenuItem>
                            {canManageCargos && (
                              <>
                                <DropdownMenuItem onClick={() => navigate(`/cargos/editar/${cargo.id}`)}>
                                  <Edit className="h-4 w-4 mr-2" />
                                  Editar
                                </DropdownMenuItem>
                                <DropdownMenuItem
                                  className="text-red-600"
                                  onClick={() => {
                                    setSelectedCargo(cargo)
                                    setShowDeleteDialog(true)
                                  }}
                                >
                                  <Trash2 className="h-4 w-4 mr-2" />
                                  Excluir
                                </DropdownMenuItem>
                              </>
                            )}
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Dialog de Confirmação de Exclusão */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Confirmar Exclusão</AlertDialogTitle>
            <AlertDialogDescription>
              Tem certeza que deseja excluir o cargo "{selectedCargo?.nome}"? 
              Esta ação não pode ser desfeita e pode afetar usuários associados a este cargo.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDelete}
              className="bg-red-600 hover:bg-red-700"
              disabled={deleteCargoMutation.isPending}
            >
              {deleteCargoMutation.isPending ? 'Excluindo...' : 'Excluir'}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
