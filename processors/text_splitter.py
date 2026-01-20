"""
Text splitting utilities for the AI Platform.

This module provides functionality to split text into chunks based on specified criteria,
using logic adapted from the SplitTextComponent.
"""

from typing import List, Dict, Any
from langchain_text_splitters import CharacterTextSplitter
from core.entities import Document as CoreDocument
from langchain_core.documents import Document
from nltk.tokenize import blankline_tokenize


class TextSplitter:
    """
    Text splitter implementation for the AI Platform.

    This class provides methods to split text documents into smaller chunks based on
    configurable parameters like chunk size, overlap, and separator.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, separator: str = "\n"):
        """
        Initialize the TextSplitter.

        Args:
            chunk_size: The maximum number of characters in each chunk.
            chunk_overlap: Number of characters to overlap between chunks.
            separator: The character to split on. Defaults to newline.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator

    def normalize(self, input_list: List[Dict[str, Any]], chunk_len: int) -> List[Dict[str, Any]]:
        """
        Merge small chunks up to chunk_len.

        Args:
            input_list: List of document chunks represented as dictionaries
            chunk_len: Target length for combined chunks

        Returns:
            List of normalized document chunks
        """
        output_list = []
        tmp_item = {}
        for i, value in enumerate(input_list):
            if tmp_item:
                page_avg = lambda a, b: (a + b) // 2
                new_item = self.merge_item(input_list[i], tmp_item, page_avg(input_list[i]["page_num"], tmp_item["page_num"]))
                if len(new_item["text"]) < chunk_len:
                    tmp_item = new_item
                else:
                    output_list.append(new_item)
                    tmp_item = {}
            elif len(value["text"]) < chunk_len:
                tmp_item = input_list[i]
            else:
                output_list.append(input_list[i])
        if tmp_item:
            output_list.append(tmp_item)
        return output_list

    def xls_normalize(self, input_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize Excel data by splitting on blank lines.

        Args:
            input_list: List of document chunks from Excel files

        Returns:
            List of normalized document chunks
        """
        output_list = []
        for item in input_list:
            rows = blankline_tokenize(item["text"])
            for row in rows:
                output_list.append({
                    "uuid": item["uuid"],
                    "file_path": item["file_path"],
                    "page_num": item["page_num"],
                    "text": row
                })
        return output_list

    def merge_item(self, a: Dict[str, Any], b: Dict[str, Any], page_num: int) -> Dict[str, Any]:
        """
        Merge two chunks.

        Args:
            a: First chunk represented as dictionary
            b: Second chunk represented as dictionary
            page_num: Page number for the merged chunk

        Returns:
            Merged chunk as dictionary
        """
        new_item = a.copy()
        new_item["text"] = "\n\n".join((a["text"], b["text"]))
        new_item["page_num"] = page_num
        return new_item

    def _docs_to_core_docs(self, docs: List[Document]) -> List[CoreDocument]:
        """
        Convert LangChain documents to core Document entities.

        Args:
            docs: List of LangChain Document objects

        Returns:
            List of core Document entities
        """
        core_docs = []
        for i, doc in enumerate(docs):
            # Create a unique ID for each chunk
            doc_id = f"{doc.metadata.get('source', 'unknown')}_{i}"
            core_doc = CoreDocument(
                id=doc_id,
                content=doc.page_content,
                metadata=doc.metadata
            )
            core_docs.append(core_doc)
        return core_docs

    def split_text(self, documents: List[Any]) -> List[CoreDocument]:
        """
        Split text into chunks based on specified criteria.

        Args:
            documents: List of documents to split (either CoreDocument or LangChain Document)

        Returns:
            List of split documents as CoreDocument
        """
        # Convert documents to LangChain documents
        lc_documents = []
        for doc in documents:
            # Check if it's a CoreDocument or LangChain Document
            if hasattr(doc, 'content'):  # It's a CoreDocument
                lc_doc = Document(
                    page_content=doc.content,
                    metadata=doc.metadata
                )
            else:  # Assume it's a LangChain Document
                lc_doc = doc
            lc_documents.append(lc_doc)

        # Apply preprocessing if needed (similar to the original component)
        preprocessed_docs = []
        for lc_doc in lc_documents:
            # Check if it's an Excel file based on metadata
            file_path = lc_doc.metadata.get('source', '')
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                # For Excel files, we need to handle the text differently
                # This is a simplified approach - in the original component,
                # the data structure was different
                text_chunks = self.xls_normalize([{
                    "uuid": "unknown",
                    "file_path": file_path,
                    "page_num": lc_doc.metadata.get('page', 0),
                    "text": lc_doc.page_content
                }])

                for chunk in text_chunks:
                    preprocessed_doc = Document(
                        page_content=chunk["text"],
                        metadata={
                            **lc_doc.metadata,
                            "page": chunk["page_num"],
                            "source": chunk["file_path"]
                        }
                    )
                    preprocessed_docs.append(preprocessed_doc)
            else:
                # For other file types, apply normalization
                temp_data = [{
                    "text": lc_doc.page_content,
                    "page_num": lc_doc.metadata.get('page', 0)
                }]
                normalized_data = self.normalize(temp_data, self.chunk_size)

                for item in normalized_data:
                    preprocessed_doc = Document(
                        page_content=item["text"],
                        metadata={
                            **lc_doc.metadata,
                            "page": item["page_num"]
                        }
                    )
                    preprocessed_docs.append(preprocessed_doc)

        # Apply CharacterTextSplitter
        splitter = CharacterTextSplitter(
            chunk_overlap=self.chunk_overlap,
            chunk_size=self.chunk_size,
            separator=self.separator,
        )
        split_docs = splitter.split_documents(preprocessed_docs)

        # Add chunk numbers to metadata
        for i, doc in enumerate(split_docs):
            doc.metadata["chunk_num"] = i + 1

        # Convert back to core documents
        core_docs = self._docs_to_core_docs(split_docs)

        return core_docs