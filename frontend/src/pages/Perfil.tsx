import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  User,
  Save,
  Upload
} from "lucide-react";
import { auth } from "@/lib/auth";
import { useState, useEffect } from "react";
import { useToast } from "@/hooks/use-toast";

export default function Perfil() {
  const { toast } = useToast();
  const [name, setName] = useState(auth.getUserName());
  const [email, setEmail] = useState(auth.getUserEmail());
  const [profileImage, setProfileImage] = useState(auth.getUserProfileImage());

  const getInitials = (name: string) => {
    const parts = name.split(' ');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const imageUrl = e.target?.result as string;
        setProfileImage(imageUrl);
        auth.setUserProfileImage(imageUrl);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = () => {
    // Update auth
    localStorage.setItem('userName', name);
    localStorage.setItem('userEmail', email);

    // Update user in localStorage if registered user
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const currentEmail = auth.getUserEmail();
    const userIndex = users.findIndex((u: any) => u.email === currentEmail);
    if (userIndex !== -1) {
      users[userIndex].name = name;
      users[userIndex].email = email;
      localStorage.setItem('users', JSON.stringify(users));
    }

    toast({
      title: "Perfil atualizado com sucesso!",
      description: "Suas informações foram salvas.",
    });
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Meu Perfil</h1>
        <p className="text-muted-foreground">
          Gerencie suas informações pessoais
        </p>
      </div>

      <Card className="shadow-card max-w-2xl">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            Informações Pessoais
          </CardTitle>
          <CardDescription>
            Atualize suas informações pessoais e foto de perfil
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center gap-6">
            <Avatar className="h-24 w-24">
              <AvatarImage src={profileImage} alt="Perfil" />
              <AvatarFallback className="gradient-primary text-white text-2xl">{getInitials(name)}</AvatarFallback>
            </Avatar>
            <div>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                style={{ display: 'none' }}
                id="profile-image-upload"
              />
              <Button variant="outline" onClick={() => document.getElementById('profile-image-upload')?.click()}>
                <Upload className="mr-2 h-4 w-4" />
                Alterar Foto
              </Button>
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="name">Nome Completo</Label>
              <Input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Seu nome completo"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seu@email.com"
              />
            </div>
          </div>

          <Button onClick={handleSave} className="gradient-primary text-white">
            <Save className="mr-2 h-4 w-4" />
            Salvar Alterações
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
