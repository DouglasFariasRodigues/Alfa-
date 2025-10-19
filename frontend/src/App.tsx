import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppLayout } from "./components/layout/AppLayout";
import { ProtectedRoute } from "./components/auth/ProtectedRoute";
import { FallbackRedirect } from "./components/auth/FallbackRedirect";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
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
import Cargos from "./pages/Cargos";
import NovoCargo from "./pages/NovoCargo";
import DetalhesCargo from "./pages/DetalhesCargo";
import PermissionTest from "./pages/PermissionTest";
import MemberDashboard from "./pages/MemberDashboard";
import TestMemberFeatures from "./pages/TestMemberFeatures";
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
          
          {/* Login */}
          <Route path="/login" element={<Login />} />
          
          {/* Teste de Permissões */}
          <Route path="/permission-test" element={<PermissionTest />} />
          
          {/* Teste de Funcionalidades para Membros */}
          <Route path="/test-member-features" element={
            <ProtectedRoute>
              <AppLayout><TestMemberFeatures /></AppLayout>
            </ProtectedRoute>
          } />
          
          {/* Dashboard para Membros */}
          <Route path="/member-dashboard" element={
            <ProtectedRoute>
              <AppLayout><MemberDashboard /></AppLayout>
            </ProtectedRoute>
          } />
          
          
          {/* Redirecionamento Inteligente */}
          <Route path="/redirect" element={
            <ProtectedRoute>
              <FallbackRedirect />
            </ProtectedRoute>
          } />
          
          {/* Rotas Protegidas do Sistema */}
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <AppLayout><Dashboard /></AppLayout>
            </ProtectedRoute>
          } />
          
          {/* Rotas Admin Protegidas */}
          <Route path="/membros" element={
            <ProtectedRoute>
              <AppLayout><Membros /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/membros/novo" element={
            <ProtectedRoute>
              <AppLayout><NovoMembro /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/membros/:id" element={
            <ProtectedRoute>
              <AppLayout><DetalhesMembro /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/membros/:id/editar" element={
            <ProtectedRoute>
              <AppLayout><EditarMembro /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/eventos" element={
            <ProtectedRoute>
              <AppLayout><Eventos /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/eventos/novo" element={
            <ProtectedRoute>
              <AppLayout><NovoEvento /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/eventos/:id" element={
            <ProtectedRoute>
              <AppLayout><DetalhesEvento /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/eventos/:id/editar" element={
            <ProtectedRoute>
              <AppLayout><EditarEvento /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/financas" element={
            <ProtectedRoute>
              <AppLayout><Financas /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/financas/nova-transacao" element={
            <ProtectedRoute>
              <AppLayout><NovaTransacao /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/documentos" element={
            <ProtectedRoute>
              <AppLayout><Documentos /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/configuracoes" element={
            <ProtectedRoute>
              <AppLayout><Configuracoes /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/cargos" element={
            <ProtectedRoute>
              <AppLayout><Cargos /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/cargos/novo" element={
            <ProtectedRoute>
              <AppLayout><NovoCargo /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/cargos/:id" element={
            <ProtectedRoute>
              <AppLayout><DetalhesCargo /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/cargos/editar/:id" element={
            <ProtectedRoute>
              <AppLayout><NovoCargo /></AppLayout>
            </ProtectedRoute>
          } />
          
          
          {/* Rotas para Membros Comuns (Visualização) */}
          <Route path="/membro/membros" element={
            <ProtectedRoute>
              <AppLayout><MembrosVisualizacao /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/membro/eventos" element={
            <ProtectedRoute>
              <AppLayout><EventosVisualizacao /></AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/membro/financas" element={
            <ProtectedRoute>
              <AppLayout><FinancasVisualizacao /></AppLayout>
            </ProtectedRoute>
          } />
          
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
