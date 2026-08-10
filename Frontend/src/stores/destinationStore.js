class DestinationStore {
  constructor() {
    this.listeners = new Set();
    this.savedPlaces = [];
    this.searchResults = [];
    this.selectedPlace = null;
    this.loading = false;
    this.error = null;
    this.searchKeyword = "";
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notify() {
    this.listeners.forEach((listener) => listener());
  }

  setSavedPlaces(places) {
    this.savedPlaces = Array.isArray(places) ? places : [];
    this.notify();
  }

  setSearchResults(results) {
    this.searchResults = Array.isArray(results) ? results : [];
    this.notify();
  }

  setSelectedPlace(place) {
    this.selectedPlace = place;
    this.notify();
  }

  setLoading(loading) {
    this.loading = Boolean(loading);
    this.notify();
  }

  setError(error) {
    this.error = error;
    this.notify();
  }

  setSearchKeyword(keyword) {
    this.searchKeyword = keyword;
    this.notify();
  }

  addSavedPlace(place) {
    this.savedPlaces = [place, ...this.savedPlaces];
    this.notify();
  }

  removeSavedPlace(placeId) {
    this.savedPlaces = this.savedPlaces.filter(
      (p) => (p.id || p.place_id) !== placeId
    );
    this.notify();
  }

  updateSavedPlaceInStore(updatedPlace) {
    const id = updatedPlace.id || updatedPlace.place_id;
    this.savedPlaces = this.savedPlaces.map((p) =>
      (p.id || p.place_id) === id ? { ...p, ...updatedPlace } : p
    );
    this.notify();
  }
}

export const destinationStore = new DestinationStore();
export default destinationStore;