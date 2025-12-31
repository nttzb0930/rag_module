
from .corpus_build import load_or_build_lsd, load_or_build_ktct, load_or_build_triet
from pprint import pprint
import textwrap, json





if __name__ == "__main__":
    combined_docs, chapter_titles = load_or_build_lsd()
    def _j(x):
        try:
            return json.loads(x) if isinstance(x, str) and x.startswith("[") else x
        except Exception:
            return x

    def pretty_print_docs(docs, start=0, limit=999, width=110, content_chars=300):
        end = min(len(docs), start + limit)
        print(f"Total docs: {len(docs)} | Showing: [{start}:{end})\n")

        for i in range(start, end):
            d = docs[i]
            md = getattr(d, "metadata", {}) or {}
            content = (getattr(d, "page_content", "") or "").strip()

            header = (
                f"[{i}] type={md.get('type')} | ch={md.get('chapter_number')} | "
                f"num={md.get('number')} | lvl={md.get('level')}"
            )
            title = f"title: {md.get('title','')}"
            sec = f"chapter_title: {md.get('chapter_title','')}\nsection_title: {md.get('section_title','')}"
            bullet = f"bullet_title: {md.get('bullet_title','')}" if md.get("type") == "bullet" else ""
            src = f"source: {md.get('source','')}"
            path = f"path: {_j(md.get('path'))}"
            bpath = f"bullet_path: {_j(md.get('bullet_path'))}" if md.get("bullet_path") else ""

            preview = textwrap.shorten(content.replace("\n", " "), width=content_chars, placeholder="…")

            print("=" * width)
            print(header)
            print(title)
            print(sec)
            if bullet: print(bullet)
            print(src)
            if path: print(path)
            if bpath: print(bpath)
            print(f"content({len(content)}): {preview}")

    # ví dụ:
    pretty_print_docs(combined_docs, start=0, limit=100)
    # pretty_print_docs(combined_docs, start=100, limit=100)




        
