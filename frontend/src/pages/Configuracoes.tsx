import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { 
  Church, 
  User, 
  Mail,
  Phone,
  MapPin
} from "lucide-react";
import { usePermissions } from "@/hooks/usePermissions";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

export default function Configuracoes() {
  const { user, isLoading } = usePermissions();
  
  // Dados da igreja (apenas visualização)
  const igrejaConfig = {
    nome: "Igreja Alfa",
    endereco: "Rua das Flores, 123 - Centro",
    cidade: "São Paulo",
    estado: "SP",
    cep: "01234-567",
    telefone: "(11) 99999-9999",
    email: "contato@igrejaalfa.com",
    site: "www.igrejaalfa.com",
    pastor: "Pastor João Silva"
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Configurações</h1>
        <p className="text-muted-foreground">
          Visualize suas informações e dados da igreja
        </p>
      </div>

      <div className="grid gap-6">
        {/* Perfil do Usuário */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5" />
              Perfil do Usuário
            </CardTitle>
            <CardDescription>
              Suas informações pessoais
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {isLoading ? (
              <div className="space-y-4">
                <Skeleton className="h-10 w-full" />
                <Skeleton className="h-10 w-full" />
                <Skeleton className="h-10 w-full" />
                <Skeleton className="h-10 w-full" />
              </div>
            ) : (
              <>
                <div className="flex items-center gap-4 mb-4">
                  <div>
                    <h3 className="text-lg font-semibold">{user?.nome || 'Usuário'}</h3>
                    {user?.cargo && (
                      <Badge variant="secondary" className="mt-1">
                        {user.cargo.nome}
                      </Badge>
                    )}
                    {user?.is_admin && (
                      <Badge variant="default" className="mt-1 ml-2">
                        Administrador
                      </Badge>
                    )}
                  </div>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="nome-usuario">Nome Completo</Label>
                    <Input
                      id="nome-usuario"
                      value={user?.nome || ''}
                      disabled
                      readOnly
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email-usuario">Email</Label>
                    <Input
                      id="email-usuario"
                      type="email"
                      value={user?.email || ''}
                      disabled
                      readOnly
                    />
                  </div>
                </div>

                {user?.telefone && (
                  <div className="space-y-2">
                    <Label htmlFor="telefone-usuario">Telefone</Label>
                    <Input
                      id="telefone-usuario"
                      value={user.telefone}
                      disabled
                      readOnly
                    />
                  </div>
                )}

                {user?.cargo && (
                  <div className="space-y-2">
                    <Label htmlFor="cargo-usuario">Cargo</Label>
                    <Input
                      id="cargo-usuario"
                      value={user.cargo.nome}
                      disabled
                      readOnly
                    />
                  </div>
                )}
              </>
            )}
          </CardContent>
        </Card>

        {/* Informações da Igreja */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Church className="h-5 w-5" />
              Informações da Igreja
            </CardTitle>
            <CardDescription>
              Dados da sua igreja
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="nome-igreja">Nome da Igreja</Label>
                <Input
                  id="nome-igreja"
                  value={igrejaConfig.nome}
                  disabled
                  readOnly
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="pastor">Pastor Responsável</Label>
                <Input
                  id="pastor"
                  value={igrejaConfig.pastor}
                  disabled
                  readOnly
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="endereco">Endereço</Label>
              <Input
                id="endereco"
                value={igrejaConfig.endereco}
                disabled
                readOnly
              />
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              <div className="space-y-2">
                <Label htmlFor="cidade">Cidade</Label>
                <Input
                  id="cidade"
                  value={igrejaConfig.cidade}
                  disabled
                  readOnly
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="estado">Estado</Label>
                <Input
                  id="estado"
                  value={igrejaConfig.estado}
                  disabled
                  readOnly
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="cep">CEP</Label>
                <Input
                  id="cep"
                  value={igrejaConfig.cep}
                  disabled
                  readOnly
                />
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="telefone-igreja">Telefone</Label>
                <Input
                  id="telefone-igreja"
                  value={igrejaConfig.telefone}
                  disabled
                  readOnly
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email-igreja">Email</Label>
                <Input
                  id="email-igreja"
                  type="email"
                  value={igrejaConfig.email}
                  disabled
                  readOnly
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="site">Site</Label>
              <Input
                id="site"
                value={igrejaConfig.site}
                disabled
                readOnly
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
