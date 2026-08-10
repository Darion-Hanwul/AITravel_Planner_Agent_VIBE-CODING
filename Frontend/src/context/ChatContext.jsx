/* eslint-disable react-refresh/only-export-components */
// src/context/ChatContext.jsx
import { createContext, useContext, useState } from 'react';

const ChatContext = createContext(null);

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);

  const value = {
    messages,
    setMessages,
    activeSessionId,
    setActiveSessionId,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChatContext harus digunakan di dalam ChatProvider');
  }
  return context;
};