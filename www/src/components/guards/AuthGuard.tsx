import React, { useEffect } from "react";
import { useRouter } from "next/router";

import useAuth from "../../hooks/useAuth";

interface AuthGuardType {
  children: React.ReactNode;
}

// For routes that can only be accessed by authenticated users
function AuthGuard({ children }: AuthGuardType) {
  const { isAuthenticated} = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/");
    }
  }, [isAuthenticated, router]);

  return isAuthenticated ? (
    <React.Fragment>{children}</React.Fragment>
  ) : (
    <React.Fragment />
  );
}

export default AuthGuard;
