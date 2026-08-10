/* eslint-disable react-hooks/set-state-in-effect */
import { useState, useCallback, useEffect } from "react";
import tripsApi from "../services/tripsApi";
import calendarApi from "../services/calendarApi";
import itineraryStore from "../stores/itineraryStore";
import { parseApiError } from "../utils/errorHandler";

export const useItinerary = (autoFetch = false) => {
  const [trips, setTrips] = useState(itineraryStore.trips);
  const [activeTrip, setActiveTrip] = useState(itineraryStore.activeTrip);
  const [calendarEvents, setCalendarEvents] = useState(itineraryStore.calendarEvents);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const unsubscribe = itineraryStore.subscribe(() => {
      setTrips(itineraryStore.trips);
      setActiveTrip(itineraryStore.activeTrip);
      setCalendarEvents(itineraryStore.calendarEvents);
    });
    return () => unsubscribe();
  }, []);

  const fetchTrips = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await tripsApi.getTrips();
      itineraryStore.setTrips(data);
      return data;
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const createTrip = useCallback(async (tripData) => {
    setLoading(true);
    setError(null);
    try {
      const created = await tripsApi.createTrip(tripData);
      itineraryStore.addTrip(created);
      return created;
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteTrip = useCallback(async (tripId) => {
    setLoading(true);
    setError(null);
    try {
      await tripsApi.deleteTrip(tripId);
      itineraryStore.removeTrip(tripId);
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchCalendarEvents = useCallback(async () => {
    try {
      const events = await calendarApi.getCalendarEvents();
      itineraryStore.setCalendarEvents(events);
      return events;
    } catch (err) {
      console.error("Gagal memuat event kalender:", err);
      return [];
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchTrips();
      fetchCalendarEvents();
    }
  }, [autoFetch, fetchTrips, fetchCalendarEvents]);

  return {
    trips,
    activeTrip,
    calendarEvents,
    loading,
    error,
    fetchTrips,
    createTrip,
    deleteTrip,
    fetchCalendarEvents,
    setActiveTrip: (trip) => itineraryStore.setActiveTrip(trip),
  };
};

export default useItinerary;