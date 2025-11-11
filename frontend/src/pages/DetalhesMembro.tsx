import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Edit, Phone, Mail, MapPin, Calendar, User, Briefcase, FileText, Shield } from 'lucide-react'
import { usePermissions } from '@/hooks/usePermissions'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { useMembro } from '@/hooks/useMembros'
import { Skeleton } from '@/components/ui/skeleton'

export default function DetalhesMembro() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  
  const { data: membro, isLoading, error } = useMembro(Number(id))
  const { canManage, user } = usePermissions()
  
  // Verificar se o usuário pode gerenciar membros (criar, editar, deletar)
  const canManageMembers = canManage('membros')

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

  if (error || !membro) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate('/membros')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Membro não encontrado</h1>
            <p className="text-muted-foreground">
              O membro solicitado não foi encontrado ou não existe.
            </p>
          </div>
        </div>
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-muted-foreground mb-4">
                Verifique se o ID do membro está correto.
              </p>
              <Button onClick={() => navigate('/membros')}>
                Voltar para Membros
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ativo':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
      case 'inativo':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
      case 'falecido':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
      case 'afastado':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }
  }

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'ativo':
        return 'Ativo'
      case 'inativo':
        return 'Inativo'
      case 'falecido':
        return 'Falecido'
      case 'afastado':
        return 'Afastado'
      default:
        return status
    }
  }

  const formatDate = (dateString: string) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }

  const calculateAge = (birthDate: string) => {
    if (!birthDate) return '-'
    const today = new Date()
    const birth = new Date(birthDate)
    let age = today.getFullYear() - birth.getFullYear()
    const monthDiff = today.getMonth() - birth.getMonth()
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--
    }
    return age
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate('/membros')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{membro.nome}</h1>
            <p className="text-muted-foreground">
              Detalhes e informações do membro
            </p>
          </div>
        </div>
        {canManageMembers && (
          <Button onClick={() => navigate(`/membros/${membro.id}/editar`)}>
            <Edit className="h-4 w-4 mr-2" />
            Editar Membro
          </Button>
        )}
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Informações Pessoais */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5" />
              Informações Pessoais
            </CardTitle>
            <CardDescription>
              Dados pessoais do membro
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4">
              <Avatar className="h-16 w-16">
                <AvatarImage src={membro.foto} alt={membro.nome} />
                <AvatarFallback>
                  {membro.nome.split(' ').map(n => n[0]).join('').toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div>
                <h3 className="text-lg font-semibold">{membro.nome}</h3>
                <Badge className={getStatusColor(membro.status)}>
                  {getStatusLabel(membro.status)}
                </Badge>
              </div>
            </div>
            
            <Separator />
            
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <Mail className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Email</p>
                  <p className="text-sm text-muted-foreground">{membro.email || '-'}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <Phone className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Telefone</p>
                  <p className="text-sm text-muted-foreground">{membro.telefone || '-'}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <MapPin className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Endereço</p>
                  <p className="text-sm text-muted-foreground">{membro.endereco || '-'}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Data de Nascimento</p>
                  <p className="text-sm text-muted-foreground">
                    {formatDate(membro.data_nascimento)} 
                    {membro.data_nascimento && ` (${calculateAge(membro.data_nascimento)} anos)`}
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Informações Eclesiásticas */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Informações Eclesiásticas
            </CardTitle>
            <CardDescription>
              Dados relacionados à igreja
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Data de Batismo</p>
                  <p className="text-sm text-muted-foreground">{formatDate(membro.data_batismo)}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <Shield className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Igreja de Origem</p>
                  <p className="text-sm text-muted-foreground">{membro.igreja_origem || 'Esta igreja'}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Data de Cadastro</p>
                  <p className="text-sm text-muted-foreground">{formatDate(membro.created_at)}</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Documentos e Observações */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Documentos e Observações
          </CardTitle>
          <CardDescription>
            Informações adicionais sobre o membro
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            <div>
              <h4 className="font-medium text-sm text-muted-foreground mb-3">Documentos</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm">CPF:</span>
                  <span className="text-sm font-mono">{membro.cpf || '-'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">RG:</span>
                  <span className="text-sm font-mono">{membro.rg || '-'}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-sm text-muted-foreground mb-3">Observações</h4>
              <p className="text-sm text-muted-foreground">
                {membro.observacoes || 'Nenhuma observação registrada.'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Estatísticas */}
      <Card>
        <CardHeader>
          <CardTitle>Estatísticas</CardTitle>
          <CardDescription>
            Informações sobre o membro
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <Calendar className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">
                {membro.data_nascimento ? calculateAge(membro.data_nascimento) : '-'}
              </p>
              <p className="text-sm text-muted-foreground">Anos de idade</p>
            </div>
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <Calendar className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">
                {membro.created_at ? Math.floor((Date.now() - new Date(membro.created_at).getTime()) / (1000 * 60 * 60 * 24)) : '-'}
              </p>
              <p className="text-sm text-muted-foreground">Dias como membro</p>
            </div>
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <Shield className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">
                {membro.cargo_nome || '-'}
              </p>
              <p className="text-sm text-muted-foreground">Cargo</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Ações */}
      <Card>
        <CardHeader>
          <CardTitle>Ações</CardTitle>
          <CardDescription>
            Opções disponíveis para este membro
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-3">
            {canManageMembers ? (
              <>
                <Button onClick={() => navigate(`/membros/${membro.id}/editar`)}>
                  <Edit className="h-4 w-4 mr-2" />
                  Editar Membro
                </Button>
                <Button variant="outline">
                  <FileText className="h-4 w-4 mr-2" />
                  Gerar Cartão
                </Button>
              </>
            ) : (
              <div className="text-center w-full py-4">
                <p className="text-muted-foreground">
                  Você pode apenas visualizar as informações deste membro.
                </p>
              </div>
            )}
            <Button variant="outline" onClick={() => navigate('/membros')}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar para Membros
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}