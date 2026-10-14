import { createContext, useContext, type ReactNode } from "react";
import { User } from "oidc-client-ts";
import {
    AuthProvider as OidcAuthProvider,
    useAuth as useOidcAuth,
    type AuthContextProps,
    type AuthProviderProps,
} from "react-oidc-context";

// Development-only mock auth. Must match backend security/mock_auth.py.
// The backend ignores the mock token unless MOCK_AUTH=true and ENVIRONMENT=development.
export const MOCK_AUTH =
    import.meta.env.DEV && import.meta.env.VITE_MOCK_AUTH === "true";
const MOCK_AUTH_TOKEN = "mock-auth-dev-token";

const mockUser = new User({
    access_token: MOCK_AUTH_TOKEN,
    id_token: MOCK_AUTH_TOKEN,
    token_type: "Bearer",
    expires_at: Math.floor(Date.now() / 1000) + 365 * 24 * 3600,
    profile: {
        iss: "mock-auth",
        sub: "mock-auth|test-user",
        aud: "mock-auth",
        exp: 0,
        iat: 0,
        given_name: "Mock",
        family_name: "Test User",
        preferred_username: "mock-test-user",
        email: "mock.test.user@example.invalid",
    },
});

const noop = async () => {};

const mockContext = {
    user: mockUser,
    isLoading: false,
    isAuthenticated: true,
    error: undefined,
    signinRedirect: noop,
    removeUser: noop,
} as unknown as AuthContextProps;

const MockAuthContext = createContext<AuthContextProps>(mockContext);

export function AuthProvider(props: AuthProviderProps & { children: ReactNode }) {
    if (MOCK_AUTH) {
        return (
            <MockAuthContext.Provider value={mockContext}>
                {props.children}
            </MockAuthContext.Provider>
        );
    }
    return <OidcAuthProvider {...props} />;
}

export function useAuth(): AuthContextProps {
    const mock = useContext(MockAuthContext);
    // MOCK_AUTH is a build-time constant, so the hook order never changes.
    return MOCK_AUTH ? mock : useOidcAuth();
}
