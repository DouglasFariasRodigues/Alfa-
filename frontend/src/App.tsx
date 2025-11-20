import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { AppLayout } from "@/components/layout/AppLayout";

// Pages
import Landing from "@/pages/Landing";
import Register from "@/pages/Register";
import Dashboard from "@/pages/Dashboard";
import Membros from "@/pages/Membros";
import NovoMembro from "@/pages/NovoMembro";
import DetalhesMembro from "@/pages/DetalhesMembro";
import EditarMembro from "@/pages/EditarMembro";
import Eventos from "@/pages/Eventos";
import NovoEvento from "@/pages/NovoEvento";
import EditarEvento from "@/pages/EditarEvento";
import DetalhesEvento from "@/pages/DetalhesEvento";
import Financas from "@/pages/Financas";
import FinancasPublico from "@/pages/FinancasPublico";
import NovaTransacao from "@/pages/NovaTransacao";
import FinancasVisualizacao from "@/pages/FinancasVisualizacao";
import Documentos from "@/pages/Documentos";
import Configuracoes from "@/pages/Configuracoes";
import Perfil from "@/pages/Perfil";
import MemberView from "@/pages/MemberView";
import MemberEvents from "@/pages/MemberEvents";
import NotFound from "@/pages/NotFound";

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/register" element={<Register />} />
        <Route path="/financas-publico" element={<FinancasPublico />} />

        {/* Protected Routes */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <AppLayout>
              <Dashboard />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/posts" element={
          <ProtectedRoute>
            <AppLayout>
              <div className="p-6">
                <h1 className="text-3xl font-bold">Postagens</h1>
                <p className="text-muted-foreground">Página de postagens em desenvolvimento</p>
              </div>
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/membros" element={
          <ProtectedRoute>
            <AppLayout>
              <MemberView />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/admin/membros" element={
          <ProtectedRoute allowedRoles={["admin", "secretario", "pastor", "diacono", "presbitero", "missionario"]}>
            <AppLayout>
              <Membros />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/membros/novo" element={
          <ProtectedRoute allowedRoles={["admin", "secretario", "pastor", "diacono", "presbitero", "missionario"]}>
            <AppLayout>
              <NovoMembro />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/membros/:id" element={
          <ProtectedRoute allowedRoles={["admin", "secretario", "pastor", "diacono", "presbitero", "missionario"]}>
            <AppLayout>
              <DetalhesMembro />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/membros/:id/editar" element={
          <ProtectedRoute allowedRoles={["admin", "secretario", "pastor", "diacono", "presbitero", "missionario"]}>
            <AppLayout>
              <EditarMembro />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/eventos" element={
          <ProtectedRoute>
            <AppLayout>
              <MemberEvents />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/eventos/novo" element={
          <ProtectedRoute allowedRoles={["admin", "secretario", "pastor", "diacono", "presbitero", "missionario"]}>
            <AppLayout>
              <NovoEvento />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/eventos/:id" element={
          <ProtectedRoute>
            <AppLayout>
              <DetalhesEvento />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/eventos/:id/editar" element={
          <ProtectedRoute allowedRoles={["admin", "secretario", "pastor", "diacono", "presbitero", "missionario"]}>
            <AppLayout>
              <EditarEvento />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/financas" element={
          <AppLayout>
            <Financas />
          </AppLayout>
        } />

        <Route path="/financas/novo" element={
          <ProtectedRoute allowedRoles={["admin", "secretario", "pastor", "diacono", "presbitero", "missionario"]}>
            <AppLayout>
              <NovaTransacao />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/financas/visualizacao" element={
          <ProtectedRoute allowedRoles={["admin", "secretario", "pastor", "diacono", "presbitero", "missionario"]}>
            <AppLayout>
              <FinancasVisualizacao />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/documentos" element={
          <ProtectedRoute>
            <AppLayout>
              <Documentos />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/configuracoes" element={
          <ProtectedRoute allowedRoles={["admin"]}>
            <AppLayout>
              <Configuracoes />
            </AppLayout>
          </ProtectedRoute>
        } />

        <Route path="/perfil" element={
          <ProtectedRoute>
            <AppLayout>
              <Perfil />
            </AppLayout>
          </ProtectedRoute>
        } />

        {/* 404 Route */}
        <Route path="*" element={<NotFound />} />
      </Routes>
      <Toaster />
    </Router>
  );
}

export default App;
