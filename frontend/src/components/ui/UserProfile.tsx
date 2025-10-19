import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { User, Shield, Users, Calendar, Mail, Phone } from "lucide-react";
import { usePermissions } from "@/hooks/usePermissions";

export const UserProfile: React.FC = () => {
  const { user, isLoading } = usePermissions();

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Perfil do Usuário</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!user) {
    return null;
  }

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'ativo':
        return 'bg-green-100 text-green-800';
      case 'inativo':
        return 'bg-gray-100 text-gray-800';
      case 'falecido':
        return 'bg-red-100 text-red-800';
      case 'afastado':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-blue-100 text-blue-800';
    }
  };

  return (
    <Card className="shadow-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {user.user_type === 'admin' ? (
            <Shield className="h-5 w-5 text-blue-600" />
          ) : (
            <Users className="h-5 w-5 text-green-600" />
          )}
          Perfil do Usuário
        </CardTitle>
        <CardDescription>
          Informações sobre sua conta e permissões
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Avatar e Informações Básicas */}
        <div className="flex items-center gap-4">
          <Avatar className="h-16 w-16">
            <AvatarImage src="" alt={user.nome} />
            <AvatarFallback className="text-lg">
              {user.nome?.charAt(0)?.toUpperCase() || 'U'}
            </AvatarFallback>
          </Avatar>
          <div className="space-y-1">
            <h3 className="text-lg font-semibold">{user.nome}</h3>
            <div className="flex items-center gap-2">
              <Badge 
                variant="outline" 
                className={user.user_type === 'admin' ? 'border-blue-200 text-blue-700' : 'border-green-200 text-green-700'}
              >
                {user.user_type === 'admin' ? 'Administrador' : 'Membro'}
              </Badge>
              {user.status && (
                <Badge className={getStatusColor(user.status)}>
                  {user.status}
                </Badge>
              )}
            </div>
          </div>
        </div>

        {/* Informações de Contato */}
        <div className="grid gap-3">
          <div className="flex items-center gap-2 text-sm">
            <Mail className="h-4 w-4 text-muted-foreground" />
            <span>{user.email}</span>
          </div>
          {user.telefone && (
            <div className="flex items-center gap-2 text-sm">
              <Phone className="h-4 w-4 text-muted-foreground" />
              <span>{user.telefone}</span>
            </div>
          )}
        </div>

        {/* Cargo e Permissões */}
        {user.cargo && (
          <div className="space-y-3">
            <h4 className="font-medium text-sm text-muted-foreground">Cargo e Permissões</h4>
            <div className="p-3 bg-muted/50 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Shield className="h-4 w-4 text-muted-foreground" />
                <span className="font-medium">{user.cargo.nome}</span>
              </div>
              <p className="text-sm text-muted-foreground mb-3">
                {user.cargo.descricao || 'Sem descrição'}
              </p>
              
              {/* Lista de Permissões */}
              <div className="space-y-2">
                <h5 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                  Permissões Ativas
                </h5>
                <div className="grid grid-cols-2 gap-2">
                  {user.cargo.pode_registrar_dizimos && (
                    <Badge variant="secondary" className="text-xs">Dízimos</Badge>
                  )}
                  {user.cargo.pode_registrar_ofertas && (
                    <Badge variant="secondary" className="text-xs">Ofertas</Badge>
                  )}
                  {user.cargo.pode_gerenciar_membros && (
                    <Badge variant="secondary" className="text-xs">Membros</Badge>
                  )}
                  {user.cargo.pode_gerenciar_eventos && (
                    <Badge variant="secondary" className="text-xs">Eventos</Badge>
                  )}
                  {user.cargo.pode_gerenciar_financas && (
                    <Badge variant="secondary" className="text-xs">Finanças</Badge>
                  )}
                  {user.cargo.pode_gerenciar_cargos && (
                    <Badge variant="secondary" className="text-xs">Cargos</Badge>
                  )}
                  {user.cargo.pode_gerenciar_documentos && (
                    <Badge variant="secondary" className="text-xs">Documentos</Badge>
                  )}
                  {user.cargo.pode_visualizar_relatorios && (
                    <Badge variant="secondary" className="text-xs">Relatórios</Badge>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Informações de Acesso */}
        <div className="space-y-2 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            <span>
              {user.user_type === 'admin' 
                ? `Membro desde: ${new Date(user.date_joined).toLocaleDateString('pt-BR')}`
                : `Cadastrado em: ${new Date(user.created_at).toLocaleDateString('pt-BR')}`
              }
            </span>
          </div>
          {user.user_type === 'admin' && user.last_login && (
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              <span>
                Último acesso: {new Date(user.last_login).toLocaleDateString('pt-BR')}
              </span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
