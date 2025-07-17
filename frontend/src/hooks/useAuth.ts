import { useState, useEffect } from 'react';

export interface AuthState {
  isAuthenticated: boolean;
  username: string | null;
  isLoading: boolean;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    username: null,
    isLoading: true
  });

  useEffect(() => {
    // Check if user is authenticated on initial load
    const checkAuth = () => {
      const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
      const username = localStorage.getItem('username');
      
      setAuthState({
        isAuthenticated,
        username,
        isLoading: false
      });
    };

    checkAuth();
  }, []);

  const login = (username: string) => {
    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('username', username);
    setAuthState({
      isAuthenticated: true,
      username,
      isLoading: false
    });
  };

  const logout = () => {
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('username');
    setAuthState({
      isAuthenticated: false,
      username: null,
      isLoading: false
    });
  };

  return {
    ...authState,
    login,
    logout
  };
};