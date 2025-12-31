import rag_module.loaders as l
import rag_module.raw_text as r
import rag_module.parsing as p
import rag_module.text_preprocess as t
import rag_module.documents as d





class BasePdfIngestor:
    def __init__(
            self,
            path: str,
            chapter_pattern: str,
            pdf_start: int | None = None,
            pdf_end: int | None = None,
    ):
        self.path = path
        self.chapter_pattern = chapter_pattern
        self.pdf_start = pdf_start
        self.pdf_end = pdf_end
    
    def ingest(self):
        """
        1. Load And Extract PDF To Docs
        2. Cut Unused PDF Page
        3. Convert Docs To String Literal
        4. Get Chapter Title
        5. Get Summary Objective
        6. Get Detail Content
        7. Clean Chapter After Cut
        8. Fix Heading Broken Line 
        9. Parse Section Numbered
        10. Buid Metadata
        11. Parse Section Include Bullet
        12. Append Combined Docs
        """
        combined_docs = []
        
        docs = l.extract_pdf_loader(self.path)
        full_text = r.build_raw_text(docs, page_start=self.pdf_start, page_end=self.pdf_end)
        chapter_titles = p.extract_chapter_title(full_text, self.chapter_pattern)
        summaries = p.extract_summary_objective(full_text)
        detail_contents = p.extract_detail_content(full_text)


        for idx, chapter_text in enumerate(detail_contents, start=1):
            chapter_text = t.clean_text(chapter_text)
            chapter_text = t.fix_heading_broken_lines(chapter_text)

            sections = p.extract_numbered_section(chapter_text)
            sections = p.build_metadata(sections, source=self.path)

            docs_sections = d.sections_to_documents_with_bullets(
                sections,
                doc_type="content",
                chapter_number=str(idx),
                chapter_title=chapter_titles[idx-1]
            )
            combined_docs.extend(docs_sections)
            # nếu có mục tiêu chương thì thêm 
            if idx - 1 < len(summaries):
                combined_docs.extend(
                    p.objectives_to_documents(
                        summaries[idx-1],
                        chapter_number=str(idx),
                        chapter_title=chapter_titles[idx-1],
                        source=self.path
                    )
                )
        return combined_docs, chapter_titles

