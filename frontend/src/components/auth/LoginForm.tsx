import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Loader2, Shield, Users } from 'lucide-react';
import { useLogin, useLoginMembro } from '@/hooks/useAuth';

const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  senha: z.string().min(1, 'Senha é obrigatória'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export const LoginForm = () => {
  const [error, setError] = useState<string>('');
  const loginMutation = useLogin();
  const loginMembroMutation = useLoginMembro();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmitAdmin = async (data: LoginFormData) => {
    setError('');
    try {
      const result = await loginMutation.mutateAsync(data);
      if (result.success) {
        // Redirecionar para página apropriada baseada no tipo de usuário
        window.location.href = '/redirect';
      } else {
        setError(result.message || 'Erro ao fazer login');
      }
    } catch (err) {
      setError('Erro ao conectar com o servidor');
      console.error('Login error:', err);
    }
  };

  const onSubmitMembro = async (data: LoginFormData) => {
    setError('');
    try {
      const result = await loginMembroMutation.mutateAsync(data);
      if (result.success) {
        // Redirecionar para página apropriada baseada no tipo de usuário
        window.location.href = '/redirect';
      } else {
        setError(result.message || 'Erro ao fazer login');
      }
    } catch (err) {
      setError('Erro ao conectar com o servidor');
      console.error('Login error:', err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">
            Sistema Alfa
          </CardTitle>
          <CardDescription className="text-center">
            Faça login para acessar o sistema
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="admin" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="admin" className="flex items-center gap-2">
                <Shield className="h-4 w-4" />
                Admin
              </TabsTrigger>
              <TabsTrigger value="membro" className="flex items-center gap-2">
                <Users className="h-4 w-4" />
                Membro
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="admin" className="space-y-4">
              <form onSubmit={handleSubmit(onSubmitAdmin)} className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="seu@email.com"
                {...register('email')}
                disabled={loginMutation.isPending}
              />
              {errors.email && (
                <p className="text-sm text-red-600">{errors.email.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="senha">Senha</Label>
              <Input
                id="senha"
                type="password"
                placeholder="Sua senha"
                {...register('senha')}
                disabled={loginMutation.isPending}
              />
              {errors.senha && (
                <p className="text-sm text-red-600">{errors.senha.message}</p>
              )}
            </div>

                <Button
                  type="submit"
                  className="w-full"
                  disabled={loginMutation.isPending}
                >
                  {loginMutation.isPending ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Entrando...
                    </>
                  ) : (
                    'Entrar como Admin'
                  )}
                </Button>
              </form>
            </TabsContent>
            
            <TabsContent value="membro" className="space-y-4">
              <form onSubmit={handleSubmit(onSubmitMembro)} className="space-y-4">
                {error && (
                  <Alert variant="destructive">
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                <div className="space-y-2">
                  <Label htmlFor="email-membro">Email</Label>
                  <Input
                    id="email-membro"
                    type="email"
                    placeholder="seu@email.com"
                    {...register('email')}
                    disabled={loginMembroMutation.isPending}
                  />
                  {errors.email && (
                    <p className="text-sm text-red-600">{errors.email.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="senha-membro">Senha</Label>
                  <Input
                    id="senha-membro"
                    type="password"
                    placeholder="Sua senha"
                    {...register('senha')}
                    disabled={loginMembroMutation.isPending}
                  />
                  {errors.senha && (
                    <p className="text-sm text-red-600">{errors.senha.message}</p>
                  )}
                </div>

                <Button
                  type="submit"
                  className="w-full"
                  disabled={loginMembroMutation.isPending}
                >
                  {loginMembroMutation.isPending ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Entrando...
                    </>
                  ) : (
                    'Entrar como Membro'
                  )}
                </Button>
              </form>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};
