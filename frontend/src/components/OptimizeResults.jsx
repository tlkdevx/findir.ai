const OptimizeResults = ({ setOptimizationResult, optimizationResult }) => {
    const handleOptimize = async () => {
      const response = await fetch("http://127.0.0.1:8000/api/optimize?user_id=1");
      if (response.ok) {
        const data = await response.json();
        setOptimizationResult(data.recommendations);
      }
    };
  
    return (
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h2 className="text-xl font-bold mb-4">Оптимизация</h2>
        <button onClick={handleOptimize} className="bg-green-500 text-white p-2 rounded">Запустить оптимизацию</button>
        {optimizationResult && (
          <ul className="mt-4">
            {optimizationResult.length > 0 ? (
              optimizationResult.map((rec, index) => <li key={index} className="border-b p-2">{rec}</li>)
            ) : (
              <p className="text-gray-500">Рекомендаций пока нет.</p>
            )}
          </ul>
        )}
      </div>
    );
  };
  
  export default OptimizeResults;
  