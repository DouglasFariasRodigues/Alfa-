import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppLayout } from "./components/layout/AppLayout";
import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import Membros from "./pages/Membros";
import NovoMembro from "./pages/NovoMembro";
import DetalhesMembro from "./pages/DetalhesMembro";
import EditarMembro from "./pages/EditarMembro";
import Eventos from "./pages/Eventos";
import NovoEvento from "./pages/NovoEvento";
import DetalhesEvento from "./pages/DetalhesEvento";
import EditarEvento from "./pages/EditarEvento";
import Financas from "./pages/Financas";
import NovaTransacao from "./pages/NovaTransacao";
import Documentos from "./pages/Documentos";
import Configuracoes from "./pages/Configuracoes";
import NotFound from "./pages/NotFound";
// Páginas para membros comuns (visualização)
import MembrosVisualizacao from "./pages/MembrosVisualizacao";
import EventosVisualizacao from "./pages/EventosVisualizacao";
import FinancasVisualizacao from "./pages/FinancasVisualizacao";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          {/* Landing Page */}
          <Route path="/" element={<Landing />} />
          
          {/* Rotas do Sistema */}
          <Route path="/dashboard" element={<AppLayout><Dashboard /></AppLayout>} />
          
          {/* Rotas Admin */}
          <Route path="/membros" element={<AppLayout><Membros /></AppLayout>} />
          <Route path="/membros/novo" element={<AppLayout><NovoMembro /></AppLayout>} />
          <Route path="/membros/:id" element={<AppLayout><DetalhesMembro /></AppLayout>} />
          <Route path="/membros/:id/editar" element={<AppLayout><EditarMembro /></AppLayout>} />
          <Route path="/eventos" element={<AppLayout><Eventos /></AppLayout>} />
          <Route path="/eventos/novo" element={<AppLayout><NovoEvento /></AppLayout>} />
          <Route path="/eventos/:id" element={<AppLayout><DetalhesEvento /></AppLayout>} />
          <Route path="/eventos/:id/editar" element={<AppLayout><EditarEvento /></AppLayout>} />
          <Route path="/financas" element={<AppLayout><Financas /></AppLayout>} />
          <Route path="/financas/nova-transacao" element={<AppLayout><NovaTransacao /></AppLayout>} />
          <Route path="/documentos" element={<AppLayout><Documentos /></AppLayout>} />
          <Route path="/configuracoes" element={<AppLayout><Configuracoes /></AppLayout>} />
          
          {/* Rotas para Membros Comuns (Visualização) */}
          <Route path="/membro/membros" element={<AppLayout><MembrosVisualizacao /></AppLayout>} />
          <Route path="/membro/eventos" element={<AppLayout><EventosVisualizacao /></AppLayout>} />
          <Route path="/membro/financas" element={<AppLayout><FinancasVisualizacao /></AppLayout>} />
          
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
