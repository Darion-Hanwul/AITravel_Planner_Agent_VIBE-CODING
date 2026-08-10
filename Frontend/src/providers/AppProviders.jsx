// src/providers/AppProviders.jsx
import 'react';
import { AppProvider } from '../context/AppContext';
import { ChatProvider } from '../context/ChatContext';

export function AppProviders({ children }) {
  return (
    <AppProvider>
      <ChatProvider>
        {children}
      </ChatProvider>
    </AppProvider>
  );
}