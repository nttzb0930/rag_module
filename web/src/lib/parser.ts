export interface TextBlockItem {
  type:
    | "h1"
    | "h2"
    | "h3"
    | "ordered"
    | "major-bullet"
    | "bullet-l1"
    | "bullet-l2"
    | "section-colon"
    | "paragraph"
    | "space";
  num?: string;
  content: string;
}

export function parseTextBlocks(text: string): TextBlockItem[] {
  const lines = text.split("\n");
  const blocks: TextBlockItem[] = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed === "") {
      blocks.push({ type: "space", content: "" });
      continue;
    }

    let type: TextBlockItem["type"] | null = null;
    let num: string | undefined = undefined;
    let content = trimmed;

    if (trimmed.startsWith("# ")) {
      type = "h1";
      content = trimmed.slice(2);
    } else if (trimmed.startsWith("## ")) {
      type = "h2";
      content = trimmed.slice(3);
    } else if (trimmed.startsWith("### ")) {
      type = "h3";
      content = trimmed.slice(4);
    } else {
      const orderedMatch = trimmed.match(/^(\d+)\.\s(.*)/);
      if (orderedMatch) {
        type = "ordered";
        num = orderedMatch[1];
        content = orderedMatch[2];
      } else if (trimmed.startsWith("- ") || trimmed.startsWith("• ")) {
        type = "major-bullet";
        content = trimmed.slice(2).trim();
      } else if (trimmed.startsWith("+ ")) {
        type = "bullet-l1";
        content = trimmed.slice(2).trim();
      } else if (trimmed.startsWith("* ")) {
        type = "bullet-l2";
        content = trimmed.slice(2).trim();
      } else if (trimmed.endsWith(":")) {
        type = "section-colon";
        content = trimmed;
      }
    }

    if (type !== null) {
      blocks.push({ type, num, content });
    } else {
      // Continuation of previous block
      if (
        blocks.length > 0 &&
        blocks[blocks.length - 1].type !== "space" &&
        !blocks[blocks.length - 1].type.startsWith("h")
      ) {
        blocks[blocks.length - 1].content += "\n" + trimmed;
      } else {
        blocks.push({ type: "paragraph", content: trimmed });
      }
    }
  }

  return blocks;
}
