import { useState, useMemo } from "react";
import {
  ChatMessage,
  DebugEntry,
  statusLabels,
  API_BASE_URL,
  createMessageId,
  formatTime,
  createDebugEntry,
  wait,
  splitCachedAnswer,
  parseSseBlock,
  RagStreamEvent,
} from "@/schema/chat";

export function useChat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [isDebugOpen, setIsDebugOpen] = useState(false);
  const [debugEntries, setDebugEntries] = useState<DebugEntry[]>([]);
  const [currentStatus, setCurrentStatus] = useState("Đang gửi câu hỏi");

  const canSubmit = question.trim().length > 0 && !isLoading;
  const hasMessages = messages.length > 0;
  const apiHost = useMemo(() => API_BASE_URL.replace(/^https?:\/\//, ""), []);

  const resetChat = () => {
    setMessages([]);
    setError("");
  };

  async function submitQuestion(nextQuestion?: string) {
    const text = (nextQuestion ?? question).trim();
    if (!text || isLoading) return;

    const userId = createMessageId("user");
    const assistantId = createMessageId("assistant");
    const assistantCreatedAt = formatTime();

    const upsertAssistantMessage = (update: (content: string) => string) => {
      setMessages((current) => {
        const existing = current.find((message) => message.id === assistantId);
        if (!existing) {
          return [
            ...current,
            {
              id: assistantId,
              role: "assistant",
              content: update(""),
              createdAt: assistantCreatedAt,
            },
          ];
        }

        return current.map((message) =>
          message.id === assistantId
            ? { ...message, content: update(message.content) }
            : message,
        );
      });
    };

    setQuestion("");
    setError("");
    setCurrentStatus("Đã nhận câu hỏi");
    setDebugEntries([createDebugEntry("request", text)]);
    setIsDebugOpen(false);
    setIsLoading(true);
    setMessages((current) => [
      ...current,
      { id: userId, role: "user", content: text, createdAt: formatTime() },
    ]);

    try {
      const response = await fetch(`${API_BASE_URL}/rag/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text }),
      });

      if (!response.ok) {
        throw new Error(`API returned ${response.status}`);
      }

      if (!response.body) {
        throw new Error("API stream is empty");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      const streamCachedAnswer = async (answer: string) => {
        upsertAssistantMessage(() => "");
        for (const chunk of splitCachedAnswer(answer)) {
          upsertAssistantMessage((content) => content + chunk);
          await wait(10);
        }
      };

      const handleStreamEvent = async (streamEvent: RagStreamEvent) => {
        const textValue =
          typeof streamEvent.data.text === "string" ? streamEvent.data.text : "";
        const answerValue =
          typeof streamEvent.data.answer === "string" ? streamEvent.data.answer : "";
        const messageValue =
          typeof streamEvent.data.message === "string" ? streamEvent.data.message : "";

        if (streamEvent.event === "chunk" && textValue) {
          upsertAssistantMessage((content) => content + textValue);
          return;
        }

        if (streamEvent.event === "status") {
          setCurrentStatus(statusLabels[messageValue] || messageValue || "Đang xử lý");
          setDebugEntries((current) => [
            ...current,
            createDebugEntry("status", messageValue || "processing"),
          ]);
          return;
        }

        if (streamEvent.event === "cache_hit" && answerValue) {
          setCurrentStatus(statusLabels.cache_hit);
          setDebugEntries((current) => [
            ...current,
            createDebugEntry("cache_hit", "Answer returned from cache"),
          ]);
          await streamCachedAnswer(answerValue);
          return;
        }

        if (streamEvent.event === "cached_partial" && answerValue) {
          setCurrentStatus(statusLabels.cached_partial);
          setDebugEntries((current) => [
            ...current,
            createDebugEntry("cached_partial", "Partial cached answer rendered"),
          ]);
          upsertAssistantMessage(() => answerValue);
          return;
        }

        if (streamEvent.event === "done") {
          setCurrentStatus(statusLabels.done);
          setDebugEntries((current) => [
            ...current,
            createDebugEntry("done", answerValue ? "Final answer received" : "Stream completed"),
          ]);
          if (answerValue) {
            upsertAssistantMessage(() => answerValue);
          }
          return;
        }

        if (streamEvent.event === "error") {
          setCurrentStatus(statusLabels.error);
          setDebugEntries((current) => [
            ...current,
            createDebugEntry("error", messageValue || "Stream error"),
          ]);
          throw new Error(messageValue || "Stream error");
        }
      };

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true }).replace(/\r\n/g, "\n");
        let separatorIndex = buffer.indexOf("\n\n");
        while (separatorIndex !== -1) {
          const block = buffer.slice(0, separatorIndex).trim();
          buffer = buffer.slice(separatorIndex + 2);
          const streamEvent = parseSseBlock(block);
          if (streamEvent) {
            await handleStreamEvent(streamEvent);
          }
          separatorIndex = buffer.indexOf("\n\n");
        }
      }

      buffer += decoder.decode();
      const tailEvent = parseSseBlock(buffer.trim());
      if (tailEvent) {
        await handleStreamEvent(tailEvent);
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : "Khong goi duoc API.";
      setError(message);
      setMessages((current) => [
        ...current,
        {
          id: createMessageId("assistant-error"),
          role: "assistant",
          content: "Không kết nối được Backend. Kiểm tra FastAPI, CORS va VITE_API_BASE_URL.",
          createdAt: formatTime(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return {
    question,
    setQuestion,
    messages,
    setMessages,
    isLoading,
    error,
    setError,
    isDebugOpen,
    setIsDebugOpen,
    debugEntries,
    currentStatus,
    canSubmit,
    hasMessages,
    apiHost,
    resetChat,
    submitQuestion,
  };
}
