import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { UserProfile } from "@/components/ui/UserProfile";
import { 
  Church, 
  User, 
  Bell, 
  Shield, 
  Database, 
  Mail, 
  Smartphone, 
  Globe,
  Save,
  Upload,
  Loader2
} from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/hooks/use-toast";
import { Badge } from "@/components/ui/badge";

export default function Configuracoes() {
  const { toast } = useToast();
  
  // Estados para as configurações
  const [igrejaConfig, setIgrejaConfig] = useState({
    nome: "Igreja Alfa",
    endereco: "Rua das Flores, 123 - Centro",
    cidade: "São Paulo",
    estado: "SP",
    cep: "01234-567",
    telefone: "(11) 99999-9999",
    email: "contato@igrejaalfa.com",
    site: "www.igrejaalfa.com",
    pastor: "Pastor João Silva"
  });

  const [usuarioConfig, setUsuarioConfig] = useState({
    nome: "Administrador",
    email: "admin@igrejaalfa.com",
    telefone: "(11) 99999-9999",
    cargo: "Administrador"
  });

  const [notificacoes, setNotificacoes] = useState({
    emailEventos: true,
    emailMembros: true,
    emailFinanceiro: true,
    pushNotificacoes: false,
    lembretesPagamento: true
  });

  const [sistema, setSistema] = useState({
    tema: "claro",
    idioma: "pt-BR",
    timezone: "America/Sao_Paulo",
    backupAutomatico: true,
    logAtividades: true
  });

  const [loading, setLoading] = useState(false);

  const handleIgrejaChange = (field: string, value: string) => {
    setIgrejaConfig(prev => ({ ...prev, [field]: value }));
  };

  const handleUsuarioChange = (field: string, value: string) => {
    setUsuarioConfig(prev => ({ ...prev, [field]: value }));
  };

  const handleNotificacaoChange = (field: string, value: boolean) => {
    setNotificacoes(prev => ({ ...prev, [field]: value }));
  };

  const handleSistemaChange = (field: string, value: string | boolean) => {
    setSistema(prev => ({ ...prev, [field]: value }));
  };

  const handleSaveIgreja = async () => {
    setLoading(true);
    try {
      // Aqui seria a integração com a API
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simular API call
      
      toast({
        title: "Configurações salvas!",
        description: "As configurações da igreja foram atualizadas com sucesso.",
      });
    } catch (error) {
      toast({
        title: "Erro ao salvar",
        description: "Não foi possível salvar as configurações. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveUsuario = async () => {
    setLoading(true);
    try {
      // Aqui seria a integração com a API
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simular API call
      
      toast({
        title: "Perfil atualizado!",
        description: "Suas informações pessoais foram atualizadas com sucesso.",
      });
    } catch (error) {
      toast({
        title: "Erro ao atualizar",
        description: "Não foi possível atualizar seu perfil. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveNotificacoes = async () => {
    setLoading(true);
    try {
      // Aqui seria a integração com a API
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simular API call
      
      toast({
        title: "Preferências salvas!",
        description: "Suas preferências de notificação foram atualizadas.",
      });
    } catch (error) {
      toast({
        title: "Erro ao salvar",
        description: "Não foi possível salvar as preferências. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSistema = async () => {
    setLoading(true);
    try {
      // Aqui seria a integração com a API
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simular API call
      
      toast({
        title: "Configurações do sistema salvas!",
        description: "As configurações do sistema foram atualizadas com sucesso.",
      });
    } catch (error) {
      toast({
        title: "Erro ao salvar",
        description: "Não foi possível salvar as configurações. Tente novamente.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Configurações</h1>
        <p className="text-muted-foreground">
          Configure sua igreja e personalize o sistema
        </p>
      </div>

      {/* Perfil do Usuário */}
      <UserProfile />

      <div className="grid gap-6">
        {/* Configurações da Igreja */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Church className="h-5 w-5" />
              Informações da Igreja
            </CardTitle>
            <CardDescription>
              Configure os dados da sua igreja
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="nome-igreja">Nome da Igreja</Label>
                <Input
                  id="nome-igreja"
                  value={igrejaConfig.nome}
                  onChange={(e) => handleIgrejaChange("nome", e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="pastor">Pastor Responsável</Label>
                <Input
                  id="pastor"
                  value={igrejaConfig.pastor}
                  onChange={(e) => handleIgrejaChange("pastor", e.target.value)}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="endereco">Endereço</Label>
              <Input
                id="endereco"
                value={igrejaConfig.endereco}
                onChange={(e) => handleIgrejaChange("endereco", e.target.value)}
              />
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              <div className="space-y-2">
                <Label htmlFor="cidade">Cidade</Label>
                <Input
                  id="cidade"
                  value={igrejaConfig.cidade}
                  onChange={(e) => handleIgrejaChange("cidade", e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="estado">Estado</Label>
                <Input
                  id="estado"
                  value={igrejaConfig.estado}
                  onChange={(e) => handleIgrejaChange("estado", e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="cep">CEP</Label>
                <Input
                  id="cep"
                  value={igrejaConfig.cep}
                  onChange={(e) => handleIgrejaChange("cep", e.target.value)}
                />
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="telefone-igreja">Telefone</Label>
                <Input
                  id="telefone-igreja"
                  value={igrejaConfig.telefone}
                  onChange={(e) => handleIgrejaChange("telefone", e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email-igreja">Email</Label>
                <Input
                  id="email-igreja"
                  type="email"
                  value={igrejaConfig.email}
                  onChange={(e) => handleIgrejaChange("email", e.target.value)}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="site">Site</Label>
              <Input
                id="site"
                value={igrejaConfig.site}
                onChange={(e) => handleIgrejaChange("site", e.target.value)}
              />
            </div>

            <div className="flex justify-end">
              <Button onClick={handleSaveIgreja} disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4 mr-2" />
                    Salvar Configurações
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

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
            <div className="flex items-center gap-4">
              <Avatar className="h-20 w-20">
                <AvatarImage src="" alt={usuarioConfig.nome} />
                <AvatarFallback>
                  {usuarioConfig.nome.split(' ').map(n => n[0]).join('').toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div>
                <h3 className="text-lg font-semibold">{usuarioConfig.nome}</h3>
                <Badge variant="secondary">{usuarioConfig.cargo}</Badge>
                <Button variant="outline" size="sm" className="mt-2">
                  <Upload className="h-4 w-4 mr-2" />
                  Alterar Foto
                </Button>
              </div>
            </div>

            <Separator />

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="nome-usuario">Nome Completo</Label>
                <Input
                  id="nome-usuario"
                  value={usuarioConfig.nome}
                  onChange={(e) => handleUsuarioChange("nome", e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email-usuario">Email</Label>
                <Input
                  id="email-usuario"
                  type="email"
                  value={usuarioConfig.email}
                  onChange={(e) => handleUsuarioChange("email", e.target.value)}
                />
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="telefone-usuario">Telefone</Label>
                <Input
                  id="telefone-usuario"
                  value={usuarioConfig.telefone}
                  onChange={(e) => handleUsuarioChange("telefone", e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="cargo-usuario">Cargo</Label>
                <Input
                  id="cargo-usuario"
                  value={usuarioConfig.cargo}
                  onChange={(e) => handleUsuarioChange("cargo", e.target.value)}
                />
              </div>
            </div>

            <div className="flex justify-end">
              <Button onClick={handleSaveUsuario} disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4 mr-2" />
                    Salvar Perfil
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Notificações */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5" />
              Notificações
            </CardTitle>
            <CardDescription>
              Configure suas preferências de notificação
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Notificações por Email</Label>
                  <p className="text-sm text-muted-foreground">
                    Receber notificações sobre eventos por email
                  </p>
                </div>
                <Switch
                  checked={notificacoes.emailEventos}
                  onCheckedChange={(checked) => handleNotificacaoChange("emailEventos", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Notificações de Membros</Label>
                  <p className="text-sm text-muted-foreground">
                    Receber notificações sobre novos membros
                  </p>
                </div>
                <Switch
                  checked={notificacoes.emailMembros}
                  onCheckedChange={(checked) => handleNotificacaoChange("emailMembros", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Notificações Financeiras</Label>
                  <p className="text-sm text-muted-foreground">
                    Receber notificações sobre transações financeiras
                  </p>
                </div>
                <Switch
                  checked={notificacoes.emailFinanceiro}
                  onCheckedChange={(checked) => handleNotificacaoChange("emailFinanceiro", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Notificações Push</Label>
                  <p className="text-sm text-muted-foreground">
                    Receber notificações push no navegador
                  </p>
                </div>
                <Switch
                  checked={notificacoes.pushNotificacoes}
                  onCheckedChange={(checked) => handleNotificacaoChange("pushNotificacoes", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Lembretes de Pagamento</Label>
                  <p className="text-sm text-muted-foreground">
                    Receber lembretes sobre pagamentos pendentes
                  </p>
                </div>
                <Switch
                  checked={notificacoes.lembretesPagamento}
                  onCheckedChange={(checked) => handleNotificacaoChange("lembretesPagamento", checked)}
                />
              </div>
            </div>

            <div className="flex justify-end">
              <Button onClick={handleSaveNotificacoes} disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4 mr-2" />
                    Salvar Preferências
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Configurações do Sistema */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Configurações do Sistema
            </CardTitle>
            <CardDescription>
              Configurações avançadas do sistema
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="tema">Tema</Label>
                <select
                  id="tema"
                  value={sistema.tema}
                  onChange={(e) => handleSistemaChange("tema", e.target.value)}
                  className="w-full p-2 border border-input bg-background rounded-md"
                >
                  <option value="claro">Claro</option>
                  <option value="escuro">Escuro</option>
                  <option value="auto">Automático</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="idioma">Idioma</Label>
                <select
                  id="idioma"
                  value={sistema.idioma}
                  onChange={(e) => handleSistemaChange("idioma", e.target.value)}
                  className="w-full p-2 border border-input bg-background rounded-md"
                >
                  <option value="pt-BR">Português (Brasil)</option>
                  <option value="en-US">English (US)</option>
                  <option value="es-ES">Español</option>
                </select>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Backup Automático</Label>
                  <p className="text-sm text-muted-foreground">
                    Fazer backup automático dos dados diariamente
                  </p>
                </div>
                <Switch
                  checked={sistema.backupAutomatico}
                  onCheckedChange={(checked) => handleSistemaChange("backupAutomatico", checked)}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Log de Atividades</Label>
                  <p className="text-sm text-muted-foreground">
                    Registrar todas as atividades do sistema
                  </p>
                </div>
                <Switch
                  checked={sistema.logAtividades}
                  onCheckedChange={(checked) => handleSistemaChange("logAtividades", checked)}
                />
              </div>
            </div>

            <div className="flex justify-end">
              <Button onClick={handleSaveSistema} disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4 mr-2" />
                    Salvar Configurações
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}