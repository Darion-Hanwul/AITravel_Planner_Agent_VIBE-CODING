/* eslint-disable react-hooks/set-state-in-effect */
import { useState, useCallback, useEffect } from "react";
import savedPlacesApi from "../services/savedPlacesApi";
import destinationStore from "../stores/destinationStore";
import { parseApiError } from "../utils/errorHandler";

export const useDestinations = (autoFetch = false) => {
  const [savedPlaces, setSavedPlaces] = useState(destinationStore.savedPlaces);
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const unsubscribe = destinationStore.subscribe(() => {
      setSavedPlaces(destinationStore.savedPlaces);
    });
    return () => unsubscribe();
  }, []);

  const fetchSavedPlaces = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await savedPlacesApi.getSavedPlaces();
      destinationStore.setSavedPlaces(data);
      return data;
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const searchPlaces = useCallback(async (query) => {
    if (!query || !query.trim()) {
      setSearchResults([]);
      return [];
    }
    setLoading(true);
    setError(null);
    try {
      const results = await savedPlacesApi.searchSavedPlaces(query);
      setSearchResults(results);
      return results;
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const savePlace = useCallback(async (placeData) => {
    setLoading(true);
    setError(null);
    try {
      const newPlace = await savedPlacesApi.createSavedPlace(placeData);
      destinationStore.addSavedPlace(newPlace);
      return newPlace;
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const removePlace = useCallback(async (placeId) => {
    setLoading(true);
    setError(null);
    try {
      await savedPlacesApi.deleteSavedPlace(placeId);
      destinationStore.removeSavedPlace(placeId);
    } catch (err) {
      const msg = parseApiError(err);
      setError(msg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchSavedPlaces();
    }
  }, [autoFetch, fetchSavedPlaces]);

  return {
    savedPlaces,
    searchResults,
    loading,
    error,
    fetchSavedPlaces,
    searchPlaces,
    savePlace,
    removePlace,
  };
};

export default useDestinations;