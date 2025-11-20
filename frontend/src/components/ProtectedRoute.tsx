import { Navigate } from "react-router-dom";
import { auth } from "@/lib/auth";

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: string[];
}

export function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const isLoggedIn = auth.isLoggedIn();
  const userType = auth.getUserType();

  if (!isLoggedIn) {
    return <Navigate to="/" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(userType || "")) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
}
