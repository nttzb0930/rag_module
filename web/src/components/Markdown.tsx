import { useState } from "react";
import { Check, Copy } from "lucide-react";
import { parseTextBlocks } from "@/lib/parser";

function parseInline(text: string) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return (
        <strong key={i} className="font-semibold text-neutral-950">
          {part.slice(2, -2)}
        </strong>
      );
    }
    return part;
  });
}

function CodeBlock({ language, code }: { language: string; code: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="my-3 overflow-hidden rounded-2xl border border-neutral-200 bg-neutral-50 shadow-[0_1px_2px_rgba(0,0,0,0.02)]">
      {/* Top Bar */}
      <div className="flex items-center justify-between border-b border-neutral-200/50 bg-neutral-50 px-4 py-2 text-xs font-semibold text-neutral-800 select-none">
        <div className="flex items-center gap-1.5">
          <span className="text-[10px] text-neutral-500 font-mono">{"</>"}</span>
          <span>{language}</span>
        </div>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 text-neutral-500 hover:text-neutral-900 transition-colors cursor-pointer"
          type="button"
          title="Sao chép"
        >
          {copied ? (
            <Check size={14} className="text-teal-600" />
          ) : (
            <Copy size={13} strokeWidth={2} />
          )}
        </button>
      </div>
      {/* Code Area */}
      <div className="overflow-x-auto p-4 text-[13.5px] font-mono text-neutral-800 leading-relaxed bg-white">
        <pre className="whitespace-pre">{code}</pre>
      </div>
    </div>
  );
}

function TextBlock({ text }: { text: string }) {
  const blocks = parseTextBlocks(text);

  return (
    <div className="flex flex-col gap-2.5">
      {blocks.map((block, index) => {
        if (block.type === "space") {
          return <div key={index} className="h-1" />;
        }

        if (block.type === "h3") {
          return (
            <h4 key={index} className="text-base font-semibold text-neutral-950 mt-2">
              {parseInline(block.content)}
            </h4>
          );
        }

        if (block.type === "h2") {
          return (
            <h3 key={index} className="text-lg font-semibold text-neutral-950 mt-3">
              {parseInline(block.content)}
            </h3>
          );
        }

        if (block.type === "h1") {
          return (
            <h2 key={index} className="text-xl font-bold text-neutral-950 mt-4">
              {parseInline(block.content)}
            </h2>
          );
        }

        if (block.type === "ordered") {
          return (
            <div key={index} className="flex gap-2 text-[15px] leading-7 text-neutral-800 whitespace-pre-line">
              <span className="font-semibold text-neutral-950">{block.num}.</span>
              <span className="flex-1">{parseInline(block.content)}</span>
            </div>
          );
        }

        if (block.type === "major-bullet") {
          return (
            <div key={index} className="mt-4 flex gap-2 text-[15px] leading-7 text-neutral-800 whitespace-pre-line">
              <span className="pt-[1px] font-semibold text-neutral-500">-</span>
              <span className="flex-1">{parseInline(block.content)}</span>
            </div>
          );
        }

        if (block.type === "bullet-l1") {
          return (
            <div key={index} className="flex gap-2 pl-5 text-[15px] leading-7 text-neutral-800 whitespace-pre-line">
              <span className="text-neutral-400">•</span>
              <span className="flex-1">{parseInline(block.content)}</span>
            </div>
          );
        }

        if (block.type === "bullet-l2") {
          return (
            <div key={index} className="flex gap-2 pl-9 text-[15px] leading-7 text-neutral-700 whitespace-pre-line">
              <span className="text-neutral-400">◦</span>
              <span className="flex-1">{parseInline(block.content)}</span>
            </div>
          );
        }

        if (block.type === "section-colon") {
          return (
            <div key={index} className="mt-4 flex gap-2 text-base leading-7 text-neutral-950 whitespace-pre-line">
              <span className="pt-[1px] font-semibold text-neutral-500">-</span>
              <span className="flex-1 font-semibold">{parseInline(block.content)}</span>
            </div>
          );
        }

        return (
          <p key={index} className="text-[15px] leading-7 text-neutral-800 whitespace-pre-line">
            {parseInline(block.content)}
          </p>
        );
      })}
    </div>
  );
}

export function Markdown({ content }: { content: string }) {
  const parts = content.split(/```/);
  return (
    <div className="flex flex-col gap-4">
      {parts.map((part, index) => {
        // Odd indices are code blocks
        if (index % 2 === 1) {
          const lines = part.split("\n");
          const firstLine = lines[0].trim();
          const codeLines = lines.slice(1);
          if (codeLines.length > 0 && codeLines[codeLines.length - 1].trim() === "") {
            codeLines.pop();
          }
          const code = codeLines.join("\n");
          let lang = firstLine || "Code";
          if (lang.toLowerCase() === "javascript" || lang.toLowerCase() === "js") lang = "JavaScript";
          else if (lang.toLowerCase() === "css") lang = "CSS";
          else if (lang.toLowerCase() === "html") lang = "HTML";
          else if (lang.toLowerCase() === "typescript" || lang.toLowerCase() === "ts") lang = "TypeScript";
          else lang = lang.charAt(0).toUpperCase() + lang.slice(1);

          return <CodeBlock key={index} language={lang} code={code} />;
        }

        // Even indices are text blocks
        return <TextBlock key={index} text={part} />;
      })}
    </div>
  );
}
