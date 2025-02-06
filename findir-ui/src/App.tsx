import { Link } from "react-router-dom";

const App: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-3xl font-bold text-blue-600">Findir.ai</h1>
      <p className="mt-2 text-gray-700">Выберите действие:</p>
      <div className="mt-4 flex gap-4">
        <Link to="/analysis" className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow">
          Анализ финансов
        </Link>
        <Link to="/recommendations" className="px-4 py-2 bg-green-500 text-white rounded-lg shadow">
          Рекомендации
        </Link>
      </div>
    </div>
  );
};

export default App;
