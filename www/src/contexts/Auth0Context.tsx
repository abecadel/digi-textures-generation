import {createContext, ReactNode} from "react";
import {Auth0Provider} from '@auth0/auth0-react';

import {Auth0ContextType,} from "../types/auth";
import {auth0Config} from "../config";

function AuthProvider({children}: { children: ReactNode }) {
    const loc = auth0Config.redirect_url;

    return (
        <Auth0Provider
            domain={auth0Config.domain}
            clientId={auth0Config.clientId}
            authorizationParams={{
                redirect_uri: "http://localhost:3000/models",
            }}
        >
            {children}
        </Auth0Provider>
    );
}

const AuthContext = createContext<Auth0ContextType | null>(null);

export {AuthContext, AuthProvider};
