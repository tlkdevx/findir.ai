import { useEffect, useState } from "react";
import api from "../api/api";

interface FinancialData {
  id: number;
  user_id: number;
  type: "deposit" | "loan";
  bank_name: string;
  amount: number;
  interest_rate: number;
  start_date: string;
  end_date?: string;
}

const Analysis: React.FC = () => {
  const [data, setData] = useState<FinancialData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    console.log("Запрос к API:", "/users/1/finance"); // Проверяем URL
  
    api.get("/users/1/finance")
      .then((response) => {
        console.log("API Response:", response.data); // Логируем ответ API
        setData(response.data);
      })
      .catch((error) => {
        console.error("Ошибка загрузки данных:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);
  
  

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-blue-600">Анализ финансов</h1>

      {loading ? (
        <p className="mt-4 text-gray-700">Загрузка данных...</p>
      ) : (
        <div className="mt-4 w-full max-w-4xl bg-white p-4 rounded-lg shadow">
          {data.length === 0 ? (
            <p className="text-gray-700">Данных пока нет.</p>
          ) : (
            <table className="w-full border-collapse border border-gray-300">
              <thead>
                <tr className="bg-gray-200">
                  <th className="border border-gray-300 px-4 py-2">ID</th>
                  <th className="border border-gray-300 px-4 py-2">Тип</th>
                  <th className="border border-gray-300 px-4 py-2">Банк</th>
                  <th className="border border-gray-300 px-4 py-2">Сумма</th>
                  <th className="border border-gray-300 px-4 py-2">Ставка (%)</th>
                  <th className="border border-gray-300 px-4 py-2">Начало</th>
                  <th className="border border-gray-300 px-4 py-2">Окончание</th>
                </tr>
              </thead>
              <tbody>
                {data.map((item) => (
                  <tr key={item.id} className="text-center">
                    <td className="border border-gray-300 px-4 py-2">{item.id}</td>
                    <td className="border border-gray-300 px-4 py-2">
                      {item.type === "loan" ? "Кредит" : "Депозит"}
                    </td>
                    <td className="border border-gray-300 px-4 py-2">{item.bank_name}</td>
                    <td className="border border-gray-300 px-4 py-2">{item.amount} ₽</td>
                    <td className="border border-gray-300 px-4 py-2">{item.interest_rate}%</td>
                    <td className="border border-gray-300 px-4 py-2">{item.start_date.split("T")[0]}</td>
                    <td className="border border-gray-300 px-4 py-2">
                      {item.end_date ? item.end_date.split("T")[0] : "Бессрочно"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
};

export default Analysis;
