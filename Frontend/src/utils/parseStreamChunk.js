export const parseStreamChunk = (chunk) => {
  if (typeof chunk === "string") return chunk;
  const decoder = new TextDecoder("utf-8");
  return decoder.decode(chunk, { stream: true });
};