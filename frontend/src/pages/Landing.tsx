import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { 
  Users, 
  Calendar, 
  DollarSign, 
  FileText, 
  CheckCircle, 
  ArrowRight,
  Church,
  BarChart3,
  Shield,
  Star,
  Sparkles,
  Heart,
  Cross
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import logoAlfa from "@/assets/logo_alfa.png";

const features = [
  {
    icon: Users,
    title: "Gestão de Membros",
    description: "Controle completo de membros, aniversariantes, histórico e comunicação centralizada."
  },
  {
    icon: Calendar,
    title: "Organização de Eventos",
    description: "Planeje cultos, eventos especiais e acompanhe a presença em tempo real."
  },
  {
    icon: DollarSign,
    title: "Controle Financeiro",
    description: "Gerencie dízimos, ofertas, despesas e gere relatórios financeiros completos."
  },
  {
    icon: FileText,
    title: "Documentos Automatizados",
    description: "Gere certificados, declarações e relatórios com apenas alguns cliques."
  },
  {
    icon: BarChart3,
    title: "Relatórios Inteligentes",
    description: "Dashboard com métricas importantes e insights para tomada de decisão."
  },
  {
    icon: Shield,
    title: "Seguro e Confiável",
    description: "Sistema seguro com controle de permissões e backup automático de dados."
  }
];

const benefits = [
  "Economize tempo com automação de tarefas administrativas",
  "Melhore a comunicação com seus membros",
  "Tenha controle total das finanças da igreja",
  "Acompanhe o crescimento da sua comunidade",
  "Acesse de qualquer lugar, a qualquer momento"
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Header/Navbar */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src={logoAlfa} alt="ALFA +" className="h-10 w-10 object-contain" />
            <span className="font-bold text-xl">ALFA +</span>
          </div>
          <Button 
            onClick={() => navigate("/dashboard")}
            className="gradient-primary text-white"
          >
            Acessar Sistema
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 md:py-32 min-h-[80vh] flex items-center">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 gradient-hero opacity-5"></div>
          
          {/* Floating decorative elements */}
          <div className="absolute top-20 left-10 w-20 h-20 rounded-full bg-primary/10 animate-pulse"></div>
          <div className="absolute top-40 right-20 w-16 h-16 rounded-full bg-primary/5 animate-bounce" style={{animationDelay: '1s'}}></div>
          <div className="absolute bottom-40 left-20 w-12 h-12 rounded-full bg-primary/15 animate-pulse" style={{animationDelay: '2s'}}></div>
          <div className="absolute bottom-20 right-10 w-24 h-24 rounded-full bg-primary/8 animate-bounce" style={{animationDelay: '0.5s'}}></div>
          
          {/* Cross and Heart decorative elements */}
          <div className="absolute top-32 right-32 text-primary/20 animate-pulse">
            <Cross className="h-8 w-8" />
          </div>
          <div className="absolute bottom-32 left-32 text-primary/20 animate-pulse" style={{animationDelay: '1.5s'}}>
            <Heart className="h-6 w-6" />
          </div>
          <div className="absolute top-1/2 left-10 text-primary/15 animate-bounce" style={{animationDelay: '2.5s'}}>
            <Star className="h-5 w-5" />
          </div>
        </div>

        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-5xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              
              {/* Left Column - Text Content */}
              <div className="text-center lg:text-left">
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary mb-6 border border-primary/20">
                  <Church className="h-4 w-4" />
                  <span className="text-sm font-medium">Sistema de Gestão Eclesiástica</span>
                  <Sparkles className="h-3 w-3 text-yellow-500" />
                </div>
                
                <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
                  Transforme a gestão da sua{" "}
                  <span className="gradient-primary bg-clip-text text-transparent relative animate-shimmer">
                    igreja
                    <div className="absolute -bottom-2 left-0 right-0 h-1 bg-gradient-to-r from-primary/30 to-primary/60 rounded-full animate-pulse"></div>
                  </span>
                </h1>
                
                <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
                  Sistema completo para gerenciar membros, eventos, finanças e documentos. 
                  Tudo em um só lugar, simples e eficiente.
                </p>
                
                <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start mb-8">
                  <Button 
                    size="lg" 
                    onClick={() => navigate("/dashboard")}
                    className="gradient-primary text-white shadow-elegant text-lg h-14 px-8 hover:scale-105 transition-all duration-300 group"
                  >
                    Começar Agora
                    <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                  <Button 
                    size="lg" 
                    variant="outline"
                    className="text-lg h-14 px-8 hover:bg-primary/5 transition-all duration-300"
                  >
                    Ver Demonstração
                  </Button>
                </div>

                {/* Trust indicators */}
                <div className="flex flex-wrap items-center justify-center lg:justify-start gap-6 text-sm text-muted-foreground">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span>100% Seguro</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span>Fácil de usar</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span>Suporte 24/7</span>
                  </div>
                </div>
              </div>

              {/* Right Column - Visual Dashboard Preview */}
              <div className="relative">
                <div className="relative z-10 animate-float">
                  <Card className="shadow-elegant border-0 bg-gradient-to-br from-background to-muted/30 backdrop-blur-sm animate-glow">
                    <CardContent className="p-8">
                      <div className="space-y-6">
                        {/* Dashboard Header */}
                        <div className="flex items-center justify-between pb-4 border-b">
                          <div className="flex items-center gap-3">
                            <div className="h-8 w-8 rounded-lg gradient-primary flex items-center justify-center">
                              <Church className="h-4 w-4 text-white" />
                            </div>
                            <div>
                              <h3 className="font-semibold text-sm">Dashboard ALFA+</h3>
                              <p className="text-xs text-muted-foreground">Visão geral</p>
                            </div>
                          </div>
                          <div className="flex gap-1">
                            <div className="w-2 h-2 rounded-full bg-green-500"></div>
                            <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
                            <div className="w-2 h-2 rounded-full bg-red-500"></div>
                          </div>
                        </div>

                        {/* Stats Grid */}
                        <div className="grid grid-cols-2 gap-4">
                          <div className="p-4 bg-primary/5 rounded-lg border border-primary/10">
                            <div className="flex items-center gap-2 mb-2">
                              <Users className="h-4 w-4 text-primary" />
                              <span className="text-xs font-medium">Membros</span>
                            </div>
                            <p className="text-2xl font-bold text-primary">245</p>
                            <p className="text-xs text-green-600">+12 este mês</p>
                          </div>
                          
                          <div className="p-4 bg-primary/5 rounded-lg border border-primary/10">
                            <div className="flex items-center gap-2 mb-2">
                              <Calendar className="h-4 w-4 text-primary" />
                              <span className="text-xs font-medium">Eventos</span>
                            </div>
                            <p className="text-2xl font-bold text-primary">12</p>
                            <p className="text-xs text-blue-600">Este mês</p>
                          </div>
                          
                          <div className="p-4 bg-primary/5 rounded-lg border border-primary/10">
                            <div className="flex items-center gap-2 mb-2">
                              <DollarSign className="h-4 w-4 text-primary" />
                              <span className="text-xs font-medium">Receita</span>
                            </div>
                            <p className="text-2xl font-bold text-primary">R$ 45.2k</p>
                            <p className="text-xs text-green-600">+8% vs mês anterior</p>
                          </div>
                          
                          <div className="p-4 bg-primary/5 rounded-lg border border-primary/10">
                            <div className="flex items-center gap-2 mb-2">
                              <BarChart3 className="h-4 w-4 text-primary" />
                              <span className="text-xs font-medium">Crescimento</span>
                            </div>
                            <p className="text-2xl font-bold text-primary">+15%</p>
                            <p className="text-xs text-green-600">Último trimestre</p>
                          </div>
                        </div>

                        {/* Recent Activity */}
                        <div className="pt-4 border-t">
                          <h4 className="text-sm font-semibold mb-3">Atividade Recente</h4>
                          <div className="space-y-2">
                            <div className="flex items-center gap-3 text-xs">
                              <div className="w-2 h-2 rounded-full bg-green-500"></div>
                              <span>Novo membro: Maria Silva</span>
                            </div>
                            <div className="flex items-center gap-3 text-xs">
                              <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                              <span>Evento criado: Culto de Oração</span>
                            </div>
                            <div className="flex items-center gap-3 text-xs">
                              <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
                              <span>Relatório financeiro gerado</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Floating elements around the card */}
                <div className="absolute -top-4 -right-4 w-8 h-8 rounded-full gradient-primary flex items-center justify-center animate-bounce">
                  <Star className="h-4 w-4 text-white" />
                </div>
                <div className="absolute -bottom-4 -left-4 w-6 h-6 rounded-full bg-yellow-400 flex items-center justify-center animate-pulse">
                  <Sparkles className="h-3 w-3 text-white" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Tudo que você precisa para gerenciar sua igreja
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Ferramentas completas e integradas para simplificar o dia a dia da sua comunidade
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {features.map((feature, index) => (
              <Card key={index} className="shadow-card hover:shadow-elegant transition-smooth border-border/50">
                <CardContent className="p-6">
                  <div className="h-12 w-12 rounded-lg gradient-primary flex items-center justify-center mb-4">
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="grid md:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-3xl md:text-4xl font-bold mb-6">
                  Por que escolher o ALFA +?
                </h2>
                <p className="text-lg text-muted-foreground mb-8">
                  Desenvolvido especialmente para igrejas que desejam modernizar 
                  sua gestão sem complicação.
                </p>
                
                <div className="space-y-4">
                  {benefits.map((benefit, index) => (
                    <div key={index} className="flex items-start gap-3">
                      <CheckCircle className="h-6 w-6 text-primary mt-0.5 flex-shrink-0" />
                      <p className="text-foreground">{benefit}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="relative">
                <Card className="shadow-elegant">
                  <CardContent className="p-8">
                    <div className="space-y-6">
                      <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className="h-10 w-10 rounded-full gradient-primary flex items-center justify-center">
                            <Users className="h-5 w-5 text-white" />
                          </div>
                          <div>
                            <p className="font-semibold">Total de Membros</p>
                            <p className="text-2xl font-bold text-primary">245</p>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className="h-10 w-10 rounded-full gradient-primary flex items-center justify-center">
                            <Calendar className="h-5 w-5 text-white" />
                          </div>
                          <div>
                            <p className="font-semibold">Eventos este Mês</p>
                            <p className="text-2xl font-bold text-primary">12</p>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className="h-10 w-10 rounded-full gradient-primary flex items-center justify-center">
                            <DollarSign className="h-5 w-5 text-white" />
                          </div>
                          <div>
                            <p className="font-semibold">Receita Mensal</p>
                            <p className="text-2xl font-bold text-primary">R$ 45.2k</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 gradient-hero opacity-5"></div>
        <div className="container mx-auto px-4 relative">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl md:text-5xl font-bold mb-6">
              Pronto para começar?
            </h2>
            <p className="text-xl text-muted-foreground mb-8">
              Junte-se a centenas de igrejas que já modernizaram sua gestão com o ALFA +
            </p>
            <Button 
              size="lg"
              onClick={() => navigate("/dashboard")}
              className="gradient-primary text-white shadow-elegant text-lg h-14 px-8"
            >
              Acessar o Sistema Agora
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-3">
              <img src={logoAlfa} alt="ALFA +" className="h-8 w-8 object-contain" />
              <span className="font-semibold">ALFA + Sistema de Gestão</span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2025 ALFA +. Todos os direitos reservados.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}