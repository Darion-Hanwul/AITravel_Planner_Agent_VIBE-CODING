class AppStore {
  constructor() {
    this.listeners = new Set();
    this.isSidebarOpen = true;
    this.isMobileMenuOpen = false;
    this.activeModal = null; // { id: string, props: object }
    this.toasts = []; // [{ id, type: 'success'|'error'|'info'|'warning', message, duration }]
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notify() {
    this.listeners.forEach((listener) => listener());
  }

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
    this.notify();
  }

  setSidebarOpen(isOpen) {
    this.isSidebarOpen = Boolean(isOpen);
    this.notify();
  }

  toggleMobileMenu() {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
    this.notify();
  }

  setMobileMenuOpen(isOpen) {
    this.isMobileMenuOpen = Boolean(isOpen);
    this.notify();
  }

  openModal(modalId, props = {}) {
    this.activeModal = { id: modalId, props };
    this.notify();
  }

  closeModal() {
    this.activeModal = null;
    this.notify();
  }

  addToast({ type = "info", message, duration = 4000 }) {
    const id = Date.now() + Math.random().toString(36).substring(2, 9);
    const newToast = { id, type, message, duration };
    this.toasts = [...this.toasts, newToast];
    this.notify();

    if (duration > 0) {
      setTimeout(() => {
        this.removeToast(id);
      }, duration);
    }
    return id;
  }

  removeToast(id) {
    this.toasts = this.toasts.filter((t) => t.id !== id);
    this.notify();
  }
}

export const appStore = new AppStore();
export default appStore;