import { useEffect, useState } from "react";
import api from "../api/api";

interface Recommendation {
  id: number;
  message: string;
}

const Recommendations: React.FC = () => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    console.log("Запрос к API:", "/api/optimize?user_id=1");

    api.get("/api/optimize", { params: { user_id: 1 } }) // Передаем user_id
      .then((response) => {
        console.log("API Response:", response.data); // Логируем ответ API
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
        <div className="mt-4 w-full max-w-3xl bg-white p-4 rounded-lg shadow">
          {recommendations.length === 0 ? (
            <p className="text-gray-700">Пока рекомендаций нет.</p>
          ) : (
            <ul className="list-disc pl-5">
              {recommendations.map((rec) => (
                <li key={rec.id} className="text-gray-800">{rec.message}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default Recommendations;
