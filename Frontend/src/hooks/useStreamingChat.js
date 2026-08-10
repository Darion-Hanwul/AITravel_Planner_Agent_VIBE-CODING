import { useChatContext } from "../context/ChatContext";

export const useStreamingChat = () => {
  const {
    messages,
    isSending,
    streamingContent,
    error,
    sendMessage,
  } = useChatContext();

  return {
    messages,
    isSending,
    streamingContent,
    error,
    sendMessage,
  };
};

export default useStreamingChat;