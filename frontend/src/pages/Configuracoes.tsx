import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
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
  Upload
} from "lucide-react";
import { Separator } from "@/components/ui/separator";

export default function Configuracoes() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Configurações</h1>
        <p className="text-muted-foreground">
          Configure sua igreja e personalize o sistema
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Church Information */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Church className="h-5 w-5" />
                Informações da Igreja
              </CardTitle>
              <CardDescription>
                Configure os dados básicos da sua igreja
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="nome-igreja">Nome da Igreja</Label>
                  <Input 
                    id="nome-igreja" 
                    defaultValue="Igreja Central" 
                    placeholder="Nome da sua igreja"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="cnpj">CNPJ</Label>
                  <Input 
                    id="cnpj" 
                    defaultValue="12.345.678/0001-90" 
                    placeholder="00.000.000/0000-00"
                  />
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="endereco">Endereço Completo</Label>
                <Textarea 
                  id="endereco"
                  defaultValue="Rua das Flores, 123 - Centro, São Paulo - SP, 01234-567"
                  placeholder="Endereço completo da igreja"
                  rows={3}
                />
              </div>
              
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="telefone">Telefone</Label>
                  <Input 
                    id="telefone" 
                    defaultValue="(11) 3456-7890" 
                    placeholder="(00) 0000-0000"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input 
                    id="email" 
                    type="email"
                    defaultValue="contato@igrejacentral.com.br" 
                    placeholder="email@igreja.com"
                  />
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="site">Site</Label>
                <Input 
                  id="site" 
                  defaultValue="https://www.igrejacentral.com.br" 
                  placeholder="https://www.suaigreja.com"
                />
              </div>
              
              <Button className="gradient-primary text-white">
                <Save className="mr-2 h-4 w-4" />
                Salvar Informações
              </Button>
            </CardContent>
          </Card>

          {/* Admin Profile */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Perfil do Administrador
              </CardTitle>
              <CardDescription>
                Gerencie suas informações pessoais
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center gap-4">
                <Avatar className="h-20 w-20">
                  <AvatarImage src="" alt="Pastor" />
                  <AvatarFallback className="gradient-primary text-white text-xl">P</AvatarFallback>
                </Avatar>
                <Button variant="outline">
                  <Upload className="mr-2 h-4 w-4" />
                  Alterar Foto
                </Button>
              </div>
              
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="nome-pastor">Nome Completo</Label>
                  <Input 
                    id="nome-pastor" 
                    defaultValue="Pastor João Silva" 
                    placeholder="Seu nome completo"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="cargo">Cargo</Label>
                  <Input 
                    id="cargo" 
                    defaultValue="Pastor Principal" 
                    placeholder="Seu cargo na igreja"
                  />
                </div>
              </div>
              
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="email-pastor">Email Pessoal</Label>
                  <Input 
                    id="email-pastor" 
                    type="email"
                    defaultValue="pastor@igrejacentral.com" 
                    placeholder="seu@email.com"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="telefone-pastor">Telefone Pessoal</Label>
                  <Input 
                    id="telefone-pastor" 
                    defaultValue="(11) 99999-9999" 
                    placeholder="(00) 00000-0000"
                  />
                </div>
              </div>
              
              <Button className="gradient-primary text-white">
                <Save className="mr-2 h-4 w-4" />
                Salvar Perfil
              </Button>
            </CardContent>
          </Card>

          {/* System Settings */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" />
                Configurações do Sistema
              </CardTitle>
              <CardDescription>
                Personalize o comportamento do sistema
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Backup Automático</Label>
                  <p className="text-sm text-muted-foreground">
                    Realizar backup diário dos dados
                  </p>
                </div>
                <Switch defaultChecked />
              </div>
              
              <Separator />
              
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Modo de Manutenção</Label>
                  <p className="text-sm text-muted-foreground">
                    Ativar para realizar manutenções
                  </p>
                </div>
                <Switch />
              </div>
              
              <Separator />
              
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label>Auditoria de Ações</Label>
                  <p className="text-sm text-muted-foreground">
                    Registrar todas as ações dos usuários
                  </p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Settings Sidebar */}
        <div className="space-y-6">
          {/* Notifications */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Notificações
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label className="text-sm">Email</Label>
                  <p className="text-xs text-muted-foreground">Receber por email</p>
                </div>
                <Switch defaultChecked />
              </div>
              
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label className="text-sm">SMS</Label>
                  <p className="text-xs text-muted-foreground">Receber por SMS</p>
                </div>
                <Switch />
              </div>
              
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label className="text-sm">WhatsApp</Label>
                  <p className="text-xs text-muted-foreground">Receber no WhatsApp</p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>

          {/* Security */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                Segurança
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button variant="outline" className="w-full justify-start">
                Alterar Senha
              </Button>
              <Button variant="outline" className="w-full justify-start">
                Autenticação 2FA
              </Button>
              <Button variant="outline" className="w-full justify-start">
                Sessões Ativas
              </Button>
              <Button variant="outline" className="w-full justify-start">
                Log de Acessos
              </Button>
            </CardContent>
          </Card>

          {/* System Info */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle>Informações do Sistema</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Versão:</span>
                <span className="font-medium">v2.1.0</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Último Backup:</span>
                <span className="font-medium">Hoje, 02:00</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Usuários Ativos:</span>
                <span className="font-medium">1,247</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Armazenamento:</span>
                <span className="font-medium">2.4 GB / 10 GB</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}