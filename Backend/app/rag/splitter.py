from typing import List, Optional
from app.config.settings import settings

class TextSplitter:
    def __init__(self, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None) -> None:
        self.chunk_size: int = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap: int = chunk_overlap or settings.CHUNK_OVERLAP
        
        self.separators: List[str] = ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> List[str]:
        if not text or not text.strip():
            return []

        return self._recursive_split(text, self.separators)

    def _recursive_split(self, text: str, separators: List[str]) -> List[str]:

        if len(text) <= self.chunk_size:
            return [text]

        separator = separators[0]
        next_separators = separators[1:]

        if separator == "":
            splits = list(text)
        else:
            splits = text.split(separator)

        chunks: List[str] = []
        current_chunk: List[str] = []
        current_length = 0

        for split in splits:
            split_len = len(split)
            addition = len(separator) if current_chunk else 0

            if current_length + split_len + addition <= self.chunk_size:
                current_chunk.append(split)
                current_length += split_len + addition
            else:
                if current_chunk:
                    joined_text = separator.join(current_chunk)
                    chunks.append(joined_text)

                if split_len > self.chunk_size and next_separators:
                    chunks.extend(self._recursive_split(split, next_separators))
                    current_chunk = []
                    current_length = 0
                else:
                    current_chunk = [split]
                    current_length = split_len

        if current_chunk:
            chunks.append(separator.join(current_chunk))

        return self._handle_overlap(chunks)

    def _handle_overlap(self, chunks: List[str]) -> List[str]:

        if len(chunks) <= 1 or self.chunk_overlap <= 0:
            return chunks

        overlapped_chunks: List[str] = [chunks[0]]

        for i in range(1, len(chunks)):
            prev_chunk = chunks[i - 1]
            current_chunk = chunks[i]

            overlap_prefix = prev_chunk[-self.chunk_overlap:]
            
            new_chunk = overlap_prefix + current_chunk
            overlapped_chunks.append(new_chunk)

        return overlapped_chunks