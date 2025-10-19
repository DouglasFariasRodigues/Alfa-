import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Edit, Calendar, User, FileText, Share2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { usePostagem } from '@/hooks/usePostagens'
import { Skeleton } from '@/components/ui/skeleton'

export default function DetalhesPostagem() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  
  const { data: postagem, isLoading, error } = usePostagem(Number(id))

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
      </div>
    )
  }

  if (error || !postagem) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate('/postagens')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Postagem não encontrada</h1>
            <p className="text-muted-foreground">
              A postagem solicitada não foi encontrada ou não existe.
            </p>
          </div>
        </div>
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-muted-foreground mb-4">
                Verifique se o ID da postagem está correto.
              </p>
              <Button onClick={() => navigate('/postagens')}>
                Voltar para Postagens
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getStatusColor = (dataPublicacao: string) => {
    const dataPostagem = new Date(dataPublicacao)
    const agora = new Date()
    const diffTime = agora.getTime() - dataPostagem.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays <= 1) {
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
    } else if (diffDays <= 7) {
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
    } else {
      return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }
  }

  const getStatusLabel = (dataPublicacao: string) => {
    const dataPostagem = new Date(dataPublicacao)
    const agora = new Date()
    const diffTime = agora.getTime() - dataPostagem.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays <= 1) {
      return 'Recente'
    } else if (diffDays <= 7) {
      return 'Esta semana'
    } else {
      return 'Antiga'
    }
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: postagem.titulo,
          text: postagem.conteudo.substring(0, 100) + '...',
          url: window.location.href,
        })
      } catch (error) {
        console.log('Erro ao compartilhar:', error)
      }
    } else {
      // Fallback para copiar URL
      navigator.clipboard.writeText(window.location.href)
      // Aqui você poderia mostrar um toast de sucesso
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={() => navigate('/postagens')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{postagem.titulo}</h1>
            <p className="text-muted-foreground">
              Postagem publicada por {postagem.autor_nome}
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleShare}>
            <Share2 className="h-4 w-4 mr-2" />
            Compartilhar
          </Button>
          <Button onClick={() => navigate(`/postagens/editar/${postagem.id}`)}>
            <Edit className="h-4 w-4 mr-2" />
            Editar
          </Button>
        </div>
      </div>

      {/* Informações da Postagem */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Informações da Postagem
          </CardTitle>
          <CardDescription>
            Detalhes sobre a publicação
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-4">
            <div>
              <h3 className="text-lg font-semibold">{postagem.titulo}</h3>
              <Badge className={getStatusColor(postagem.data_publicacao)}>
                {getStatusLabel(postagem.data_publicacao)}
              </Badge>
            </div>
          </div>
          
          <Separator />
          
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <User className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Autor</p>
                  <p className="text-sm text-muted-foreground">{postagem.autor_nome}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Data de Publicação</p>
                  <p className="text-sm text-muted-foreground">{formatDate(postagem.data_publicacao)}</p>
                </div>
              </div>
            </div>
            
            <div className="space-y-3">
              <div>
                <p className="text-sm font-medium">Tamanho do Conteúdo</p>
                <p className="text-sm text-muted-foreground">{postagem.conteudo.length} caracteres</p>
              </div>
              
              <div>
                <p className="text-sm font-medium">Tempo de Leitura Estimado</p>
                <p className="text-sm text-muted-foreground">
                  {Math.ceil(postagem.conteudo.length / 200)} minuto(s)
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Conteúdo da Postagem */}
      <Card>
        <CardHeader>
          <CardTitle>Conteúdo</CardTitle>
          <CardDescription>
            Texto completo da postagem
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="prose prose-sm max-w-none">
            <div className="whitespace-pre-wrap text-sm leading-relaxed">
              {postagem.conteudo}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Estatísticas */}
      <Card>
        <CardHeader>
          <CardTitle>Estatísticas</CardTitle>
          <CardDescription>
            Informações sobre a postagem
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <FileText className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">{postagem.conteudo.length}</p>
              <p className="text-sm text-muted-foreground">Caracteres</p>
            </div>
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <Calendar className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">
                {Math.ceil((Date.now() - new Date(postagem.data_publicacao).getTime()) / (1000 * 60 * 60 * 24))}
              </p>
              <p className="text-sm text-muted-foreground">Dias desde publicação</p>
            </div>
            <div className="text-center p-4 bg-muted/50 rounded-lg">
              <User className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-2xl font-bold">
                {postagem.autor_nome}
              </p>
              <p className="text-sm text-muted-foreground">Autor</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Ações */}
      <Card>
        <CardHeader>
          <CardTitle>Ações</CardTitle>
          <CardDescription>
            Opções disponíveis para esta postagem
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-3">
            <Button onClick={() => navigate(`/postagens/editar/${postagem.id}`)}>
              <Edit className="h-4 w-4 mr-2" />
              Editar Postagem
            </Button>
            <Button variant="outline" onClick={handleShare}>
              <Share2 className="h-4 w-4 mr-2" />
              Compartilhar
            </Button>
            <Button variant="outline" onClick={() => navigate('/postagens')}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar para Postagens
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
