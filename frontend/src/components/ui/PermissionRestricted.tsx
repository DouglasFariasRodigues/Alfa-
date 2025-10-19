import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Lock, Shield, Users } from "lucide-react";

interface PermissionRestrictedProps {
  permission: string;
  userType: 'admin' | 'membro';
  cargo?: string;
}

export const PermissionRestricted: React.FC<PermissionRestrictedProps> = ({ 
  permission, 
  userType, 
  cargo 
}) => {
  const getPermissionMessage = () => {
    switch (permission) {
      case 'membros':
        return 'Gerenciar membros';
      case 'eventos':
        return 'Gerenciar eventos';
      case 'financas':
        return 'Gerenciar finanças';
      case 'cargos':
        return 'Gerenciar cargos';
      case 'documentos':
        return 'Gerenciar documentos';
      case 'relatorios':
        return 'Visualizar relatórios';
      default:
        return 'Esta funcionalidade';
    }
  };

  return (
    <Card className="shadow-card border-amber-200 bg-amber-50">
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-amber-100">
          <Lock className="h-6 w-6 text-amber-600" />
        </div>
        <CardTitle className="text-amber-800">
          Acesso Restrito
        </CardTitle>
        <CardDescription className="text-amber-700">
          {getPermissionMessage()} não está disponível para seu perfil
        </CardDescription>
      </CardHeader>
      <CardContent className="text-center space-y-4">
        <div className="flex items-center justify-center gap-2 text-sm text-amber-700">
          <Users className="h-4 w-4" />
          <span>
            {userType === 'membro' ? 'Membro' : 'Usuário'}: {cargo || 'Sem cargo definido'}
          </span>
        </div>
        
        <div className="text-sm text-amber-600">
          <p>
            Para acessar esta funcionalidade, você precisa ter as permissões adequadas.
            Entre em contato com o administrador do sistema.
          </p>
        </div>

        <Button 
          variant="outline" 
          className="border-amber-300 text-amber-700 hover:bg-amber-100"
          onClick={() => window.history.back()}
        >
          Voltar
        </Button>
      </CardContent>
    </Card>
  );
};
