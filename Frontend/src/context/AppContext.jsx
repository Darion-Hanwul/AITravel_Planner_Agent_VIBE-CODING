/* eslint-disable react-refresh/only-export-components */
import  { createContext, useContext, useState, useEffect } from "react";
import appStore from "../stores/appStore";
import sessionStore from "../stores/sessionStore";

const AppContext = createContext(null);

export const AppProvider = ({ children }) => {
  const [appState, setAppState] = useState({
    isSidebarOpen: appStore.isSidebarOpen,
    isMobileMenuOpen: appStore.isMobileMenuOpen,
    activeModal: appStore.activeModal,
    toasts: appStore.toasts,
  });

  const [sessionState, setSessionState] = useState({
    user: sessionStore.user,
    preferences: sessionStore.preferences,
    isAuthenticated: sessionStore.isAuthenticated(),
    loading: sessionStore.loading,
  });

  useEffect(() => {
    const unsubscribeApp = appStore.subscribe(() => {
      setAppState({
        isSidebarOpen: appStore.isSidebarOpen,
        isMobileMenuOpen: appStore.isMobileMenuOpen,
        activeModal: appStore.activeModal,
        toasts: appStore.toasts,
      });
    });

    const unsubscribeSession = sessionStore.subscribe(() => {
      setSessionState({
        user: sessionStore.user,
        preferences: sessionStore.preferences,
        isAuthenticated: sessionStore.isAuthenticated(),
        loading: sessionStore.loading,
      });
    });

    if (sessionStore.isAuthenticated() && !sessionStore.user) {
      sessionStore.fetchUserProfile().catch(() => {});
    }

    return () => {
      unsubscribeApp();
      unsubscribeSession();
    };
  }, []);

  const value = {
    // App Actions & State
    isSidebarOpen: appState.isSidebarOpen,
    isMobileMenuOpen: appState.isMobileMenuOpen,
    activeModal: appState.activeModal,
    toasts: appState.toasts,
    toggleSidebar: () => appStore.toggleSidebar(),
    setSidebarOpen: (isOpen) => appStore.setSidebarOpen(isOpen),
    toggleMobileMenu: () => appStore.toggleMobileMenu(),
    setMobileMenuOpen: (isOpen) => appStore.setMobileMenuOpen(isOpen),
    openModal: (modalId, props) => appStore.openModal(modalId, props),
    closeModal: () => appStore.closeModal(),
    addToast: (toast) => appStore.addToast(toast),
    removeToast: (id) => appStore.removeToast(id),

    // Session Actions & State
    user: sessionState.user,
    preferences: sessionState.preferences,
    isAuthenticated: sessionState.isAuthenticated,
    isSessionLoading: sessionState.loading,
    logout: () => sessionStore.clearSession(),
    refreshProfile: () => sessionStore.fetchUserProfile(),
    refreshPreferences: () => sessionStore.fetchUserPreferences(),
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp harus digunakan di dalam AppProvider");
  }
  return context;
};

export default AppContext;