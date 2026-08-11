import { useState, useEffect } from "react";
import { getHistoryApi, deleteHistoryItemApi } from "@/lib/api";

export function useHistory() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [historyItems, setHistoryItems] = useState<any[]>([]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await getHistoryApi(1, 50);
      const items = Array.isArray(data) ? data : data.items || [];
      setHistoryItems(items);
    } catch (err: any) {
      setError(err.message || "Failed to fetch history");
    } finally {
      setLoading(false);
    }
  };

  const deleteItem = async (taskId: string) => {
    try {
      await deleteHistoryItemApi(taskId);
      setHistoryItems((prev) => prev.filter((item) => (item.id || item.task_id) !== taskId));
    } catch (err: any) {
      setError(err.message || "Failed to delete item");
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return { loading, error, historyData: { items: historyItems, total: historyItems.length }, fetchHistory, deleteItem };
}
