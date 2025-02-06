import { useEffect, useState } from "react";
import api from "../api/api";

interface Recommendation {
  id: number;
  message: string;
  current_outcome: number;
  optimized_outcome: number;
}

const Recommendations: React.FC = () => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    console.log("Запрос к API:", "/api/optimize?user_id=1");

    api.get("/api/optimize", { params: { user_id: 1 } })
      .then((response) => {
        console.log("API Response:", response.data);
        setRecommendations(response.data);
      })
      .catch((error) => {
        console.error("Ошибка загрузки рекомендаций:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-green-600">Рекомендации по оптимизации</h1>

      {loading ? (
        <p className="mt-4 text-gray-700">Загрузка...</p>
      ) : (
        <div className="mt-4 w-full max-w-4xl bg-white p-4 rounded-lg shadow">
          {recommendations.length === 0 ? (
            <p className="text-gray-700">Пока рекомендаций нет.</p>
          ) : (
            <div>
              {recommendations.map((rec) => (
                <div key={rec.id} className="mb-6 p-4 border rounded-lg shadow">
                  <p className="text-gray-800 font-bold">{rec.message}</p>
                  <table className="w-full border-collapse border border-gray-300 mt-2">
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="border border-gray-300 px-4 py-2">Сценарий</th>
                        <th className="border border-gray-300 px-4 py-2">Финальный результат (год)</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td className="border border-gray-300 px-4 py-2">Текущая стратегия</td>
                        <td className="border border-gray-300 px-4 py-2">{rec.current_outcome.toFixed(2)} ₽</td>
                      </tr>
                      <tr>
                        <td className="border border-gray-300 px-4 py-2">Оптимизированная стратегия</td>
                        <td className="border border-gray-300 px-4 py-2">{rec.optimized_outcome.toFixed(2)} ₽</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Recommendations;
