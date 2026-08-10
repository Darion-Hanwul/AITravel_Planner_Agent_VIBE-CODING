export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validateAuthInput = ({ email, password, fullName }) => {
  const errors = {};

  if (email !== undefined && !isValidEmail(email)) {
    errors.email = "Format email tidak valid.";
  }

  if (password !== undefined && password.length < 6) {
    errors.password = "Kata sandi minimal 6 karakter.";
  }

  if (fullName !== undefined && !fullName.trim()) {
    errors.fullName = "Nama lengkap tidak boleh kosong.";
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};