export const parseApiError = (error) => {
  if (!error) return "Terjadi kesalahan yang tidak diketahui.";

  if (typeof error === "string") return error;

  if (error.response) {
    const data = error.response.data;
    if (data && data.detail) {
      if (Array.isArray(data.detail)) {
        return data.detail.map((err) => err.msg || "Input tidak valid").join(", ");
      }
      return data.detail;
    }
    if (data && data.message) return data.message;
  }

  if (error.message) {
    if (error.message.includes("Network Error")) {
      return "Tidak dapat terhubung ke server. Periksa koneksi internet Anda.";
    }
    return error.message;
  }

  return "Gagal memproses permintaan. Silakan coba lagi nanti.";
};