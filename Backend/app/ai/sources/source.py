from __future__ import annotations

from dataclasses import dataclass, field
from app.config.settings import settings


@dataclass(slots=True, frozen=True)
class Source:
    """
    Representasi satu knowledge source untuk konfigurasi data.

    Responsibility
    --------------
    - Menjadi skema data terstruktur untuk konfigurasi metadata source.
    - Mengelola informasi endpoint web untuk kebutuhan crawling dan indexing.
    - Menghasilkan URL absolut yang valid dan siap di-crawl.

    Attributes
    ----------
    name : str
        Nama unik pengenal source data.
    category : str
        Kategori domain data (e.g., 'weather', 'budget', 'visa').
    base_url : str
        Domain utama atau root URL dari website target.
    urls : list[str]
        Daftar sub-path atau endpoint spesifik yang akan dipindai.
    enabled : bool
        Menentukan status keaktifan source di dalam sistem.
    description : str
        Deskripsi fungsional singkat mengenai isi data source.
    headers : dict[str, str]
        HTTP Headers tambahan (seperti User-Agent) untuk request crawling.
    timeout : int
        Batas waktu tunggu koneksi jaringan saat memproses I/O.
    """

    name: str
    category: str
    base_url: str
    urls: list[str]
    enabled: bool = True
    description: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    # Menarik nilai default timeout dari settings.py demi kepatuhan Prinsip 4
    timeout: int = field(default_factory=lambda: getattr(settings, "CRAWLER_TIMEOUT", 30))

    def get_urls(self) -> list[str]:
        """
        Menghasilkan daftar URL lengkap yang absolut dan siap digunakan oleh WebLoader.

        Responsibility
        --------------
        Menggabungkan base_url dengan masing-masing sub-path di dalam list urls, 
        serta membersihkan karakter slash ('/') yang berlebih secara otomatis.

        Returns
        -------
        list[str]
            Daftar alamat URL absolut yang bersih dan valid.
        """
        return [
            self.base_url.rstrip("/") + "/" + url.lstrip("/")
            for url in self.urls
        ]