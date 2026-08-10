import { useState, useCallback } from "react";
import systemApi from "../services/systemApi";

export const useHealthCheck = () => {
  const [systemStatus, setSystemStatus] = useState(null);
  const [dbStatus, setDbStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkHealth = useCallback(async () => {
    setLoading(true);
    try {
      const [health, db] = await Promise.all([
        systemApi.getHealthStatus().catch(() => ({ status: "offline" })),
        systemApi.testDatabaseConnection().catch(() => ({ status: "offline" })),
      ]);
      setSystemStatus(health);
      setDbStatus(db);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    systemStatus,
    dbStatus,
    loading,
    checkHealth,
  };
};

export default useHealthCheck;