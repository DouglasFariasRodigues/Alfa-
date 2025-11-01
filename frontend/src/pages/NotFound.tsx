import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Home, ArrowLeft, AlertTriangle } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-6">
      <Card className="w-full max-w-md shadow-card">
        <CardHeader className="text-center space-y-4">
          <div className="mx-auto w-16 h-16 bg-destructive/10 rounded-full flex items-center justify-center">
            <AlertTriangle className="h-8 w-8 text-destructive" />
          </div>
          <div>
            <CardTitle className="text-4xl font-bold text-foreground mb-2">404</CardTitle>
            <p className="text-xl text-muted-foreground">Página não encontrada</p>
          </div>
        </CardHeader>
        <CardContent className="text-center space-y-6">
          <p className="text-muted-foreground">
            A página que você está procurando não existe ou foi movida.
          </p>
          
          <div className="space-y-3">
            <Button asChild className="w-full">
              <a href="/">
                <Home className="h-4 w-4 mr-2" />
                Voltar ao Início
              </a>
            </Button>
            
            <Button variant="outline" onClick={() => window.history.back()} className="w-full">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Página Anterior
            </Button>
          </div>
          
          <div className="text-xs text-muted-foreground bg-muted p-3 rounded-lg">
            <strong>Rota tentada:</strong> {location.pathname}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default NotFound;
