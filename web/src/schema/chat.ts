import { BookOpenText, SquarePen, Search } from "lucide-react";

export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
};

export type RagStreamEvent = {
  event: string;
  data: Record<string, unknown>;
};

export type DebugEntry = {
  id: string;
  event: string;
  message: string;
  time: string;
};

export const statusLabels: Record<string, string> = {
  request: "Đã nhận câu hỏi",
  routing: "Đang phân loại ý định",
  routing_chapter: "Đang xác định chương",
  retrieving: "Đang truy xuất tài liệu",
  generating: "Đang tạo câu trả lời",
  cache_hit: "Tìm thấy cache",
  cached_partial: "Có một phần từ cache",
  done: "Hoàn tất",
  error: "Có lỗi",
};

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export const examples = [
  {
    label: "Lịch sử Đảng",
    question:
      "Chủ trương của Đảng nhằm bảo vệ chính quyền cách mạng 1945-1946 là gì?",
  },
  {
    label: "Kinh tế chính trị",
    question: "Phân tích hai thuộc tính của hàng hóa trong kinh tế chính trị.",
  },
  {
    label: "Triết học",
    question: "Vật chất và ý thức có mối quan hệ như thế nào?",
  },
];

export const quickActions = [
  { label: "Ôn tập nhanh", icon: BookOpenText },
  { label: "Tạo đề cương", icon: SquarePen },
  { label: "Tra cứu tài liệu", icon: Search },
];

export function formatTime() {
  return new Intl.DateTimeFormat("vi-VN", {
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date());
}

export function createMessageId(prefix: string) {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return `${prefix}-${crypto.randomUUID()}`;
  }
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export function createDebugEntry(event: string, message: string): DebugEntry {
  return {
    id: createMessageId("debug"),
    event,
    message,
    time: formatTime(),
  };
}

export function wait(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function splitCachedAnswer(answer: string) {
  return answer.match(/\S+\s*/g) ?? [answer];
}

export function parseSseBlock(block: string): RagStreamEvent | null {
  const lines = block.split("\n");
  let event = "message";
  const dataLines: string[] = [];

  for (const line of lines) {
    if (line.startsWith("event:")) {
      event = line.slice("event:".length).trim();
    } else if (line.startsWith("data:")) {
      dataLines.push(line.slice("data:".length).trimStart());
    }
  }

  if (dataLines.length === 0) {
    return null;
  }

  try {
    return {
      event,
      data: JSON.parse(dataLines.join("\n")) as Record<string, unknown>,
    };
  } catch {
    return null;
  }
}
