import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { ArrowLeft, Edit, Phone, Mail, MapPin, Calendar, User, Briefcase, FileText } from "lucide-react";

// Mock data - substituir por dados reais do backend
const membroMock = {
  id: 1,
  nome: "Maria Santos",
  email: "maria.santos@email.com",
  telefone: "(11) 99999-9999",
  endereco: "Rua das Flores, 123 - Centro - São Paulo, SP",
  dataNascimento: "1985-05-15",
  estadoCivil: "Casada",
  profissao: "Professora",
  status: "Ativo",
  dataCadastro: "2023-01-15",
  cargo: "Membro",
  observacoes: "Participa do grupo de louvor e ensino infantil."
};

export default function DetalhesMembro() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [membro, setMembro] = useState(membroMock);

  useEffect(() => {
    // Aqui carregaria os dados do membro pelo ID
    console.log("Carregando membro ID:", id);
  }, [id]);

  const handleEdit = () => {
    navigate(`/membros/${id}/editar`);
  };

  const getIdade = (dataNascimento: string) => {
    const hoje = new Date();
    const nascimento = new Date(dataNascimento);
    let idade = hoje.getFullYear() - nascimento.getFullYear();
    const mesAtual = hoje.getMonth();
    const mesNascimento = nascimento.getMonth();
    
    if (mesAtual < mesNascimento || (mesAtual === mesNascimento && hoje.getDate() < nascimento.getDate())) {
      idade--;
    }
    return idade;
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="outline"
            onClick={() => navigate("/membros")}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Voltar
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Detalhes do Membro</h1>
            <p className="text-muted-foreground">
              Informações completas do membro
            </p>
          </div>
        </div>
        <Button onClick={handleEdit} className="gradient-primary text-white shadow-elegant hover:opacity-90">
          <Edit className="mr-2 h-4 w-4" />
          Editar
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {/* Informações Básicas */}
        <Card className="shadow-card md:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5" />
              Informações Pessoais
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center space-x-4">
              <Avatar className="h-20 w-20">
                <AvatarImage src="" alt={membro.nome} />
                <AvatarFallback className="gradient-primary text-white text-lg">
                  {membro.nome.split(' ').map(n => n[0]).join('')}
                </AvatarFallback>
              </Avatar>
              <div className="space-y-1">
                <h2 className="text-2xl font-bold">{membro.nome}</h2>
                <div className="flex items-center gap-2">
                  <Badge
                    variant={membro.status === "Ativo" ? "default" : "secondary"}
                    className={membro.status === "Ativo" ? "gradient-primary text-white" : ""}
                  >
                    {membro.status}
                  </Badge>
                  <Badge variant="outline">{membro.cargo}</Badge>
                </div>
              </div>
            </div>

            <Separator />

            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Email</p>
                    <p className="font-medium">{membro.email}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Phone className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Telefone</p>
                    <p className="font-medium">{membro.telefone}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Data de Nascimento</p>
                    <p className="font-medium">
                      {new Date(membro.dataNascimento).toLocaleDateString('pt-BR')} ({getIdade(membro.dataNascimento)} anos)
                    </p>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Endereço</p>
                    <p className="font-medium">{membro.endereco}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <User className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Estado Civil</p>
                    <p className="font-medium">{membro.estadoCivil}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Briefcase className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <p className="text-sm text-muted-foreground">Profissão</p>
                    <p className="font-medium">{membro.profissao}</p>
                  </div>
                </div>
              </div>
            </div>

            {membro.observacoes && (
              <>
                <Separator />
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <FileText className="h-4 w-4 text-muted-foreground" />
                    <p className="text-sm font-medium text-muted-foreground">Observações</p>
                  </div>
                  <p className="text-sm">{membro.observacoes}</p>
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Informações da Igreja */}
        <Card className="shadow-card">
          <CardHeader>
            <CardTitle>Informações da Igreja</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground">Cargo</p>
              <p className="font-medium">{membro.cargo}</p>
            </div>

            <div>
              <p className="text-sm text-muted-foreground">Data de Cadastro</p>
              <p className="font-medium">
                {new Date(membro.dataCadastro).toLocaleDateString('pt-BR')}
              </p>
            </div>

            <div>
              <p className="text-sm text-muted-foreground">Status</p>
              <Badge
                variant={membro.status === "Ativo" ? "default" : "secondary"}
                className={membro.status === "Ativo" ? "gradient-primary text-white" : ""}
              >
                {membro.status}
              </Badge>
            </div>

            <Separator />

            <div className="space-y-2">
              <Button variant="outline" className="w-full">
                Gerar Cartão
              </Button>
              <Button variant="outline" className="w-full">
                Histórico
              </Button>
              <Button variant="outline" className="w-full text-destructive hover:text-destructive">
                Desativar Membro
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}