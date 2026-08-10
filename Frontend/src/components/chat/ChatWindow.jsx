import ChatHeader from "./ChatHeader";
import ChatMessageList from "./ChatMessageList";
import ChatInput from "./ChatInput";

export const ChatWindow = ({
  sessionTitle = "Percakapan Baru",
  messages = [],
  streamingText = "",
  isStreaming = false,
  isLoading = false,
  onSendMessage,
  onNewSession,
  onClearChat,
}) => {
  return (
    <div className="flex flex-col h-full bg-slate-950 flex-1 relative overflow-hidden">
      <ChatHeader
        sessionTitle={sessionTitle}
        onNewSession={onNewSession}
        onClearChat={onClearChat}
        isStreaming={isStreaming}
      />
      <ChatMessageList
        messages={messages}
        streamingText={streamingText}
        isStreaming={isStreaming}
        isLoading={isLoading}
        onPromptClick={onSendMessage}
      />
      <ChatInput
        onSendMessage={onSendMessage}
        disabled={isStreaming || isLoading}
      />
    </div>
  );
};

export default ChatWindow;