"""
Vector Store Manager (Weaviate v4 Edition)

Mengelola koneksi klien ke Vector Database Weaviate v4, inisialisasi koleksi,
serta operasi penyimpanan dan pencarian similarity chunk dokumen.
"""

import weaviate
import weaviate.classes.config as wvc
from app.config.settings import settings


class WeaviateVectorStore:
    def __init__(self) -> None:
        # Menggunakan koneksi v4 standar dengan mengombinasikan HTTP dan gRPC port
        self.client = weaviate.connect_to_local(
            host=settings.POSTGRES_HOST if "localhost" in settings.WEAVIATE_URL else "localhost",
            port=8080, # Default port REST Weaviate
            grpc_port=settings.WEAVIATE_GRPC_PORT
        )
        self.class_name = settings.WEAVIATE_CLASS
        self._init_collection()

    def _init_collection(self) -> None:
        """
        Membuat koleksi (skema kelas) di Weaviate v4 jika belum terdaftar.
        """
        try:
            # Memeriksa keberadaan koleksi menggunakan API v4 client.collections.exists()
            if not self.client.collections.exists(self.class_name):
                self.client.collections.create(
                    name=self.class_name,
                    description="Penyimpanan dokumen kontekstual untuk Travel Planner Agent RAG",
                    # Vectorizer diset None karena kita akan memasukkan custom vector hasil embedding Ollama
                    vectorizer_config=None,
                    properties=[
                        wvc.Property(
                            name="document_id",
                            data_type=wvc.DataType.TEXT,
                            description="ID relasi ke database SQL model Document"
                        ),
                        wvc.Property(
                            name="content",
                            data_type=wvc.DataType.TEXT,
                            description="Potongan teks (chunk) konten dokumen"
                        ),
                        wvc.Property(
                            name="source_name",
                            data_type=wvc.DataType.TEXT,
                            description="Nama file asli dokumen"
                        )
                    ]
                )
        except Exception as e:
            print(f"[Weaviate v4 Error] Gagal inisialisasi koleksi: {str(e)}")

    def add_document_chunk(self, content: str, embedding: list[float], meta_data: dict) -> bool:
        """
        Menyimpan teks chunk beserta custom vector embedding ke Weaviate v4.
        """
        try:
            collection = self.client.collections.get(self.class_name)
            
            # Perbaikan: Menggunakan .data.insert() untuk Weaviate v4
            collection.data.insert(
                properties={
                    "content": content,
                    "document_id": str(meta_data.get("document_id", "")),
                    "source_name": meta_data.get("source_name", "")
                },
                vector=embedding
            )
            return True
        except Exception as e:
            print(f"[Weaviate v4 Write Error] Gagal menyimpan chunk: {str(e)}")
            return False

    def search_similar_chunks(self, query_embedding: list[float], limit: int = 3) -> list[dict]:
        """
        Mencari potongan teks terdekat berdasarkan jarak kedekatan vektor menggunakan API v4 query.
        """
        try:
            collection = self.client.collections.get(self.class_name)
            
            # Menggunakan query.near_vector bawaan Weaviate v4
            response = collection.query.near_vector(
                near_vector=query_embedding,
                limit=limit,
                return_properties=["content", "source_name", "document_id"]
            )
            
            # Parsing hasil pencarian objek v4 ke format standar list dictionary
            results = []
            for obj in response.objects:
                results.append({
                    "content": obj.properties.get("content"),
                    "source_name": obj.properties.get("source_name"),
                    "document_id": obj.properties.get("document_id")
                })
            return results
        except Exception as e:
            print(f"[Weaviate v4 Query Error] Gagal melakukan pencarian: {str(e)}")
            return []

    def close(self) -> None:
        """
        Menutup koneksi client Weaviate dengan aman (direkomendasikan pada v4).
        """
        self.client.close()