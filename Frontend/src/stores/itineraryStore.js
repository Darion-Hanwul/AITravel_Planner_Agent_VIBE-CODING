class ItineraryStore {
  constructor() {
    this.listeners = new Set();
    this.trips = [];
    this.activeTrip = null;
    this.calendarEvents = [];
    this.reminders = [];
    this.loading = false;
    this.error = null;
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notify() {
    this.listeners.forEach((listener) => listener());
  }

  setTrips(trips) {
    this.trips = Array.isArray(trips) ? trips : [];
    this.notify();
  }

  setActiveTrip(trip) {
    this.activeTrip = trip;
    this.notify();
  }

  setCalendarEvents(events) {
    this.calendarEvents = Array.isArray(events) ? events : [];
    this.notify();
  }

  setReminders(reminders) {
    this.reminders = Array.isArray(reminders) ? reminders : [];
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

  addTrip(trip) {
    this.trips = [trip, ...this.trips];
    this.notify();
  }

  updateTripInStore(updatedTrip) {
    const id = updatedTrip.id || updatedTrip.trip_id;
    this.trips = this.trips.map((t) =>
      (t.id || t.trip_id) === id ? { ...t, ...updatedTrip } : t
    );
    if (this.activeTrip && (this.activeTrip.id || this.activeTrip.trip_id) === id) {
      this.activeTrip = { ...this.activeTrip, ...updatedTrip };
    }
    this.notify();
  }

  removeTrip(tripId) {
    this.trips = this.trips.filter((t) => (t.id || t.trip_id) !== tripId);
    if (this.activeTrip && (this.activeTrip.id || this.activeTrip.trip_id) === tripId) {
      this.activeTrip = null;
    }
    this.notify();
  }

  addCalendarEvent(event) {
    this.calendarEvents = [...this.calendarEvents, event];
    this.notify();
  }

  removeCalendarEvent(eventId) {
    this.calendarEvents = this.calendarEvents.filter(
      (e) => (e.id || e.event_id) !== eventId
    );
    this.notify();
  }
}

export const itineraryStore = new ItineraryStore();
export default itineraryStore;