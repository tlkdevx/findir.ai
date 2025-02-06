import { useEffect, useState } from "react";
import api from "../api/api";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface Recommendation {
  id: number;
  message: string;
  details: string;
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
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-2">
      <h1 className="text-xl font-bold text-green-600">Рекомендации по оптимизации</h1>

      {loading ? (
        <p className="mt-4 text-gray-700">Загрузка...</p>
      ) : (
        <div className="mt-4 w-full max-w-4xl bg-white p-4 rounded-lg shadow">
          {recommendations.length === 0 ? (
            <p className="text-gray-700">Пока рекомендаций нет.</p>
          ) : (
            <div>
              {recommendations.map((rec) => (
                <div key={rec.id} className="mb-6 p-4 border rounded-lg shadow bg-white w-full max-w-2xl">
                  <p className="text-gray-800 font-bold">{rec.message}</p>
                  <p className="text-gray-700 mt-2">{rec.details}</p>
                  
                  <table className="w-full border border-gray-300 mt-2 rounded-lg shadow text-sm">
                    <thead>
                      <tr className="bg-blue-500 text-white">
                        <th className="border border-gray-300 px-3 py-1">Сценарий</th>
                        <th className="border border-gray-300 px-3 py-1">Финальный результат (год)</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="bg-gray-100">
                        <td className="border border-gray-300 px-3 py-1">Текущая стратегия</td>
                        <td className="border border-gray-300 px-3 py-1 font-bold">{rec.current_outcome.toFixed(2)} ₽</td>
                      </tr>
                      <tr className="bg-green-100">
                        <td className="border border-gray-300 px-3 py-1">Оптимизированная стратегия</td>
                        <td className="border border-gray-300 px-3 py-1 font-bold">{rec.optimized_outcome.toFixed(2)} ₽</td>
                      </tr>
                    </tbody>
                  </table>

                  {/* График для каждого сценария */}
                  <div className="mt-4 w-full">
  <h2 className="text-md font-bold text-gray-800 mb-1">График: {rec.message}</h2>
  <ResponsiveContainer width="100%" height={250}>
    <LineChart
      data={[
        { period: "Месяц 1", current: rec.current_outcome * 0.98, optimized: rec.optimized_outcome * 0.99 },
        { period: "Месяц 2", current: rec.current_outcome * 0.96, optimized: rec.optimized_outcome * 0.98 },
        { period: "Месяц 3", current: rec.current_outcome * 0.94, optimized: rec.optimized_outcome * 0.97 },
        { period: "Месяц 4", current: rec.current_outcome * 0.92, optimized: rec.optimized_outcome * 0.96 },
        { period: "Месяц 5", current: rec.current_outcome * 0.90, optimized: rec.optimized_outcome * 0.95 },
        { period: "Месяц 6", current: rec.current_outcome * 0.88, optimized: rec.optimized_outcome * 0.94 }
      ]}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="period" />
      <YAxis domain={['dataMin - 5000', 'dataMax + 5000']} />
      <Tooltip />
      <Line type="monotone" dataKey="current" stroke="#FF5733" strokeWidth={2} name="Текущая стратегия" />
      <Line type="monotone" dataKey="optimized" stroke="#28A745" strokeWidth={2} name="Оптимизированная стратегия" />
    </LineChart>
  </ResponsiveContainer>
</div>

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
