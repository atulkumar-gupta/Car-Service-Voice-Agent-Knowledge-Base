# """Simple RAG: split knowledge base into sections, embed, retrieve top-k."""
# from typing import List
# from langchain.text_splitter import MarkdownHeaderTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from .config import settings


# class KnowledgeBaseRAG:
#     def __init__(self):
#         with open(settings.KB_PATH, "r", encoding="utf-8") as f:
#             md = f.read()

#         splitter = MarkdownHeaderTextSplitter(
#             headers_to_split_on=[("#", "h1"), ("##", "h2")]
#         )
#         chunks = splitter.split_text(md)

#         self.embeddings = OpenAIEmbeddings(
#             model="text-embedding-3-small",
#             api_key=settings.OPENAI_API_KEY,
#         )
#         self.vectorstore = FAISS.from_documents(chunks, self.embeddings)

#     def retrieve(self, query: str, k: int = 4) -> str:
#         docs = self.vectorstore.similarity_search(query, k=k)
#         return "\n\n---\n\n".join(d.page_content for d in docs)


# _rag_instance: KnowledgeBaseRAG | None = None

# def get_rag() -> KnowledgeBaseRAG:
#     global _rag_instance
#     if _rag_instance is None:
#         _rag_instance = KnowledgeBaseRAG()
#     return _rag_instance

"""Simple RAG using keyword-based retrieval (no external embeddings needed)."""
from typing import List
from .config import settings


class KnowledgeBaseRAG:
    def __init__(self):
        with open(settings.KB_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Split by markdown h2 headers (## 1. Engine, ## 2. Battery, etc.)
        sections = []
        current_section = []
        for line in content.split("\n"):
            if line.startswith("## "):
                if current_section:
                    sections.append("\n".join(current_section))
                current_section = [line]
            else:
                current_section.append(line)
        if current_section:
            sections.append("\n".join(current_section))

        self.sections = sections

    def retrieve(self, query: str, k: int = 4) -> str:
        """Simple keyword-overlap scoring to pick top-k sections."""
        query_words = set(query.lower().split())
        scored = []
        for section in self.sections:
            section_words = set(section.lower().split())
            overlap = len(query_words & section_words)
            scored.append((overlap, section))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = [s for score, s in scored[:k] if score > 0]

        # If no keyword match, return first 4 sections (general fallback)
        if not top:
            top = self.sections[:4]

        return "\n\n---\n\n".join(top)


_rag_instance: KnowledgeBaseRAG | None = None


def get_rag() -> KnowledgeBaseRAG:
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = KnowledgeBaseRAG()
    return _rag_instance