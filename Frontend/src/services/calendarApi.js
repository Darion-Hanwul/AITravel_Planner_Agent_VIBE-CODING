import apiClient from "./apiClient";

export const createEvent = async (eventData) => {
  const response = await apiClient.post(
    "/calendar/events",
    eventData
  );

  return response.data;
};

export const getReminderEvents = async () => {
  const response = await apiClient.get(
    "/calendar/events/reminders"
  );

  return response.data;
};

export const getEventsByDate = async (date) => {
  const response = await apiClient.get(
    "/calendar/events/filter",
    {
      params: {
        date,
      },
    }
  );

  return response.data;
};

export const getEventsBetween = async (
  startDate,
  endDate
) => {
  const response = await apiClient.get(
    "/calendar/events/filter",
    {
      params: {
        start_date: startDate,
        end_date: endDate,
      },
    }
  );

  return response.data;
};

export const getEvent = async (eventId) => {
  const response = await apiClient.get(
    `/calendar/events/${eventId}`
  );

  return response.data;
};

export const updateEvent = async (
  eventId,
  eventData
) => {
  const response = await apiClient.put(
    `/calendar/events/${eventId}`,
    eventData
  );

  return response.data;
};

export const deleteEvent = async (eventId) => {
  await apiClient.delete(
    `/calendar/events/${eventId}`
  );
};

export default {
  createEvent,
  getReminderEvents,
  getEventsByDate,
  getEventsBetween,
  getEvent,
  updateEvent,
  deleteEvent,
};