import  { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import StreamingMessage from "./StreamingMessage";
import ChatLoading from "./ChatLoading";
import ChatEmptyState from "./ChatEmptyState";

export const ChatMessageList = ({
  messages = [],
  streamingText = "",
  isStreaming = false,
  isLoading = false,
  onPromptClick,
}) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingText, isLoading, isStreaming]);

  if (messages.length === 0 && !isStreaming && !isLoading) {
    return <ChatEmptyState onPromptClick={onPromptClick} />;
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-2">
      {messages.map((msg, index) => (
        <ChatMessage key={msg.id || index} message={msg} />
      ))}

      {isStreaming && <StreamingMessage text={streamingText} />}
      {isLoading && !isStreaming && <ChatLoading />}

      <div ref={bottomRef} />
    </div>
  );
};

export default ChatMessageList;