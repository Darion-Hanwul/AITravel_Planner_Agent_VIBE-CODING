export const parseSSEMessage = (chunk) => {
  const lines = chunk.split("\n");
  const events = [];

  for (const line of lines) {
    if (line.startsWith("data: ")) {
      const dataStr = line.replace("data: ", "").trim();
      if (dataStr === "[DONE]") {
        events.push({ isDone: true });
      } else {
        try {
          const parsed = JSON.parse(dataStr);
          events.push({ isDone: false, data: parsed });
        } catch {
          events.push({ isDone: false, text: dataStr });
        }
      }
    }
  }

  return events;
};