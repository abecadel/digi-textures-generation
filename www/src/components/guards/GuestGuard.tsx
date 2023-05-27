import React, {useEffect} from "react";
import {useRouter} from "next/router";

import useAuth from "../../hooks/useAuth";

interface GuestGuardType {
    children: React.ReactNode;
}

// For routes that can only be accessed by authenticated users
function GuestGuard({children}: GuestGuardType) {
    const {isAuthenticated} = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (isAuthenticated) {
            router.push("/auth/sign-in");
        }
    }, [isAuthenticated, router]);

    return !isAuthenticated ? (
        <React.Fragment>{children}</React.Fragment>
    ) : (
        <React.Fragment/>
    );
}

export default GuestGuard;
