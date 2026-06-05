import { FormEvent, useRef, useEffect, useState } from "react";
import {
  BookOpenText,
  Bot,
  CircleHelp,
  Loader2,
  Mic,
  SquarePen,
  Plus,
  Search,
  Send,
  UserRound,
  Wifi,
  Sparkles,
  History,
  Check,
  PanelLeft,
  Copy,
  ChevronDown,
} from "lucide-react";
import { SidebarProvider, SidebarInset, useSidebar } from "@/components/ui/sidebar";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Navbar } from "@/components/Navbar";
import { useChat } from "@/hooks/use-chat";
import { ChatMessage, DebugEntry, examples, quickActions, statusLabels } from "@/schema/chat";
import { Markdown } from "@/components/Markdown";

function HamburgerIcon({
  size = 20,
  strokeWidth = 1.5,
  className,
}: {
  size?: number;
  strokeWidth?: number;
  className?: string;
}) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      <line x1="4" y1="9" x2="20" y2="9" />
      <line x1="4" y1="15" x2="14" y2="15" />
    </svg>
  );
}

function Header({
  apiHost,
  onResetChat,
}: {
  apiHost: string;
  onResetChat: () => void;
}) {
  const { toggleSidebar } = useSidebar();

  return (
    <header className="flex min-h-14 items-center justify-between border-b border-neutral-100 bg-white px-4 md:min-h-12 md:justify-end md:border-b-0 md:px-7 md:pt-3">
      {/* Mobile Left Side: Toggle Sidebar and Title */}
      <div className="flex items-center gap-2.5 md:hidden">
        <button
          className="grid size-9 place-items-center rounded-lg text-neutral-600 hover:bg-neutral-100"
          type="button"
          title="Mở thanh bên"
          onClick={toggleSidebar}
        >
          <HamburgerIcon size={20} strokeWidth={1.5} />
        </button>
        <span className="text-base font-semibold text-neutral-950">RAG Study</span>
      </div>

      {/* Right Side: Host, New Chat, and Clear Chat */}
      <div className="flex items-center gap-2 md:gap-3">
        <div className="hidden items-center gap-2 truncate rounded-full border border-neutral-200 px-3 py-2 text-xs text-neutral-600 md:inline-flex md:max-w-xs">
          <Wifi size={14} />
          <span className="truncate">{apiHost}</span>
        </div>

        {/* Mobile New Chat Button */}
        <button
          className="grid size-9 place-items-center rounded-full hover:bg-neutral-100 md:hidden"
          type="button"
          title="Tạo câu hỏi mới"
          onClick={onResetChat}
        >
          <SquarePen size={20} strokeWidth={1.5} />
        </button>
      </div>
    </header>
  );
}

function App() {
  const {
    question,
    setQuestion,
    messages,
    isLoading,
    error,
    isDebugOpen,
    setIsDebugOpen,
    debugEntries,
    currentStatus,
    canSubmit,
    hasMessages,
    apiHost,
    resetChat,
    submitQuestion,
  } = useChat();

  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (hasMessages && !isLoading) {
      textareaRef.current?.focus();
    }
  }, [hasMessages, isLoading]);

  const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      if (canSubmit) {
        void submitQuestion();
      }
    }
  };

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void submitQuestion();
  }

  return (
    <TooltipProvider>
      <SidebarProvider
        open={isSidebarOpen}
        onOpenChange={setIsSidebarOpen}
        style={
          {
            "--sidebar-width": "310px",
            "--sidebar-width-icon": "60px",
          } as React.CSSProperties
        }
      >
        <div className="flex h-[100dvh] w-full bg-white text-neutral-950 overflow-hidden">
          <Navbar
            onSelectNewChat={resetChat}
            onSubmitQuestion={(q) => void submitQuestion(q)}
            isLoading={isLoading}
            apiHost={apiHost}
          />

          <SidebarInset className="flex-1 flex flex-col h-full min-w-0 overflow-hidden">
            <section className="grid h-full min-w-0 grid-rows-[auto_1fr_auto] pb-2 md:pb-0">
              <Header
                apiHost={apiHost}
                onResetChat={resetChat}
              />

              <main className="min-h-0 flex-1 overflow-y-auto px-4 md:px-6">
                {!hasMessages ? (
                  <>
                    {/* Desktop Welcome Screen (Centered Layout) */}
                    <div className="hidden md:grid h-full place-items-center py-10">
                      <div className="grid w-full max-w-[780px] -translate-y-[3vh] justify-items-center gap-5">
                        <div className="inline-flex items-center gap-2 rounded-full border border-neutral-200 bg-white px-3 py-2 text-sm text-neutral-600 shadow-[0_12px_32px_rgba(0,0,0,0.04)]">
                          <Bot size={17} />
                          <span>RAG Study Assistant</span>
                        </div>
                        <div className="grid justify-items-center gap-2">
                          <h1 className="text-center text-[26px] font-medium leading-tight text-neutral-950">
                            Bạn đang học phần nào?
                          </h1>
                          <p className="text-center text-sm text-neutral-500">
                            Hỏi đáp trực tiếp trên tài liệu Lịch sử Đảng, Kinh tế chính trị và Triết học.
                          </p>
                        </div>

                        {/* Input form in the middle for Desktop */}
                        <form
                          className="grid min-h-14 w-full grid-cols-[38px_minmax(0,1fr)_40px] items-center rounded-[24px] border border-neutral-300 bg-white py-1.5 pl-3 pr-2 shadow-[0_26px_80px_rgba(0,0,0,0.08),0_2px_8px_rgba(0,0,0,0.04)] md:grid-cols-[42px_minmax(0,1fr)_auto_36px_42px] md:rounded-full"
                          onSubmit={handleSubmit}
                        >
                          <button
                            className="grid size-9 place-items-center rounded-full text-neutral-800 hover:bg-neutral-100"
                            type="button"
                            title="Thêm tùy chọn"
                          >
                            <Plus size={22} />
                          </button>
                          <input
                            className="h-11 min-w-0 border-0 bg-transparent text-[15px] text-neutral-950 outline-none placeholder:text-neutral-400"
                            value={question}
                            onChange={(event) => setQuestion(event.target.value)}
                            placeholder="Hỏi bất kỳ điều gì"
                            autoFocus
                          />
                          <button
                            className="hidden h-9 rounded-full px-3 text-xs text-neutral-500 hover:bg-neutral-100 md:block"
                            type="button"
                          >
                            Instant
                          </button>
                          <button
                            className="hidden size-9 place-items-center rounded-full text-neutral-800 hover:bg-neutral-100 md:grid"
                            type="button"
                            title="Nhập bằng giọng nói"
                          >
                            <Mic size={18} />
                          </button>
                          <button
                            className="grid size-9 place-items-center rounded-full bg-neutral-950 text-white disabled:opacity-50"
                            type="submit"
                            disabled={!canSubmit}
                            title="Gửi câu hỏi"
                          >
                            {isLoading ? (
                              <Loader2 className="animate-spin" size={19} />
                            ) : (
                              <Send size={18} />
                            )}
                          </button>
                        </form>

                        <div className="flex flex-wrap justify-center gap-2.5">
                          {quickActions.map((action) => {
                            const Icon = action.icon;
                            return (
                              <button
                                className="inline-flex min-h-10 items-center gap-2 rounded-full border border-neutral-200 bg-white px-4 text-sm text-neutral-700 hover:bg-neutral-100"
                                key={action.label}
                                type="button"
                              >
                                <Icon size={16} />
                                <span>{action.label}</span>
                              </button>
                            );
                          })}
                        </div>

                        <div className="grid w-full grid-cols-3 gap-2.5">
                          {examples.map((item) => (
                            <button
                              className="grid min-h-24 gap-1.5 rounded-2xl border border-neutral-200 bg-white p-3.5 text-left hover:bg-neutral-100 disabled:opacity-50"
                              key={item.question}
                              type="button"
                              onClick={() => void submitQuestion(item.question)}
                              disabled={isLoading}
                            >
                              <strong className="text-sm text-neutral-950">{item.label}</strong>
                              <span className="line-clamp-3 text-sm leading-snug text-neutral-500">
                                {item.question}
                              </span>
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Mobile Welcome Screen */}
                    <div className="md:hidden flex h-full flex-col justify-center py-6">
                      <div className="grid justify-items-center gap-2 text-center">
                        <h1 className="text-[26px] font-medium leading-tight text-neutral-950">
                          Bạn đang học phần nào?
                        </h1>
                        <p className="text-sm text-neutral-500 px-4">
                          Hỏi đáp trực tiếp trên tài liệu Lịch sử Đảng, Kinh tế chính trị và Triết học.
                        </p>
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="mx-auto flex w-full max-w-[820px] flex-col gap-6 py-6">
                    {messages.map((message) => (
                      <div
                        className={
                          message.role === "user"
                            ? "flex justify-end"
                            : "flex justify-start py-1"
                        }
                        key={message.id}
                      >
                        {message.role === "user" ? (
                          <div className="rounded-[20px] bg-neutral-100 px-4.5 py-2.5 text-[15px] text-neutral-900 max-w-[85%] md:max-w-[600px] shadow-[0_1px_2px_rgba(0,0,0,0.02)]">
                            <p className="whitespace-pre-wrap leading-6">{message.content}</p>
                          </div>
                        ) : (
                          <div className="w-full max-w-full md:max-w-[760px]">
                            <Markdown content={message.content} />
                          </div>
                        )}
                      </div>
                    ))}
                    {isLoading && (
                      <div className="flex justify-start py-2">
                        <div className="w-full max-w-[420px]">
                          <div className="flex items-center gap-2 text-sm text-neutral-400">
                            <Loader2 className="animate-spin text-neutral-400" size={15} />
                            <span>{currentStatus}</span>
                            <button
                              className="ml-1 grid size-7 place-items-center rounded-full text-neutral-500 transition hover:bg-neutral-100 hover:text-neutral-900"
                              type="button"
                              title="Mở debug"
                              onClick={() => setIsDebugOpen((current) => !current)}
                            >
                              <ChevronDown
                                className={isDebugOpen ? "rotate-180 transition-transform" : "transition-transform"}
                                size={16}
                              />
                            </button>
                          </div>
                          <div className="mt-2 flex max-w-full flex-wrap gap-1.5">
                            {debugEntries.slice(-4).map((entry) => (
                              <span
                                className="rounded-full border border-neutral-200 bg-white px-2 py-1 text-[11px] text-neutral-500"
                                key={entry.id}
                              >
                                {statusLabels[entry.message] || statusLabels[entry.event] || entry.message}
                              </span>
                            ))}
                          </div>
                          {isDebugOpen && (
                            <div className="mt-2 grid gap-1 rounded-xl border border-neutral-200 bg-neutral-50 p-3 text-xs text-neutral-600">
                              {debugEntries.map((entry) => (
                                <div className="grid grid-cols-[52px_84px_minmax(0,1fr)] gap-2" key={entry.id}>
                                  <span className="text-neutral-400">{entry.time}</span>
                                  <span className="font-medium text-neutral-700">{entry.event}</span>
                                  <span className="truncate">{entry.message}</span>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </main>

              {error && (
                <div className="mx-auto mb-2 inline-flex w-[min(820px,calc(100%-32px))] items-center gap-2 rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700 md:w-[min(820px,calc(100%-48px))]">
                  <CircleHelp size={15} />
                  <span>{error}</span>
                </div>
              )}

              {/* Bottom input bar: Always shown on mobile, and on desktop only when messages exist */}
              <form
                className={`mx-auto mb-4 grid min-h-14 w-[min(820px,calc(100%-28px))] grid-cols-[36px_minmax(0,1fr)_38px] items-center rounded-[24px] border border-neutral-300 bg-white py-2 pl-3 pr-2 shadow-[0_26px_80px_rgba(0,0,0,0.08),0_2px_8px_rgba(0,0,0,0.04)] md:mb-5 md:w-[min(820px,calc(100%-48px))] md:grid-cols-[38px_minmax(0,1fr)_auto_40px] md:rounded-full ${!hasMessages ? "md:hidden" : ""
                  }`}
                onSubmit={handleSubmit}
              >
                <button
                  className="grid size-9 place-items-center rounded-full text-neutral-800 hover:bg-neutral-100"
                  type="button"
                  title="Thêm tùy chọn"
                >
                  <Plus size={20} />
                </button>
                <textarea
                  ref={textareaRef}
                  className="max-h-32 min-w-0 resize-none border-0 bg-transparent text-[15px] leading-6 text-neutral-950 outline-none placeholder:text-neutral-400"
                  value={question}
                  onChange={(event) => setQuestion(event.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={hasMessages ? "Hỏi tiếp..." : "Hỏi bất kỳ điều gì"}
                  rows={1}
                />
                <div className="hidden items-center gap-1.5 whitespace-nowrap px-2.5 text-xs text-neutral-500 md:inline-flex">
                  <Check size={14} />
                  <span>Cache auto</span>
                </div>
                <button
                  className="grid size-9 place-items-center rounded-full bg-neutral-950 text-white disabled:opacity-50"
                  type="submit"
                  disabled={!canSubmit}
                  title="Gửi câu hỏi"
                >
                  {isLoading ? (
                    <Loader2 className="animate-spin" size={19} />
                  ) : (
                    <Send size={18} />
                  )}
                </button>
              </form>
            </section>
          </SidebarInset>
        </div>
      </SidebarProvider>
    </TooltipProvider>
  );
}

export default App;
