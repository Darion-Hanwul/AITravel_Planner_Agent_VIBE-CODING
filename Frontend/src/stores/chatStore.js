import { generateSessionId } from "../utils/generateSessionId";

class ChatStore {
  constructor() {
    this.listeners = new Set();
    this.sessions = [];
    this.activeSessionId = null;
    this.messages = [];
    this.isSending = false;
    this.streamingContent = "";
    this.error = null;
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notify() {
    this.listeners.forEach((listener) => listener());
  }

  setSessions(sessions) {
    this.sessions = Array.isArray(sessions) ? sessions : [];
    this.notify();
  }

  setActiveSessionId(sessionId) {
    this.activeSessionId = sessionId;
    this.notify();
  }

  setMessages(messages) {
    this.messages = Array.isArray(messages) ? messages : [];
    this.notify();
  }

  addMessage(message) {
    this.messages = [...this.messages, message];
    this.notify();
  }

  setIsSending(isSending) {
    this.isSending = Boolean(isSending);
    this.notify();
  }

  setStreamingContent(content) {
    this.streamingContent = content;
    this.notify();
  }

  appendStreamingContent(chunk) {
    this.streamingContent += chunk;
    this.notify();
  }

  clearStreamingContent() {
    this.streamingContent = "";
    this.notify();
  }

  setError(error) {
    this.error = error;
    this.notify();
  }

  startNewSession() {
    const newId = generateSessionId();
    this.activeSessionId = newId;
    this.messages = [];
    this.error = null;
    this.streamingContent = "";
    this.notify();
    return newId;
  }

  clearActiveChat() {
    this.messages = [];
    this.streamingContent = "";
    this.error = null;
    this.notify();
  }
}

export const chatStore = new ChatStore();
export default chatStore;