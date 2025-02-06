const FinancialList = ({ financialRecords }) => {
    return (
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h2 className="text-xl font-bold mb-4">Список финансовых данных</h2>
        {financialRecords.length === 0 ? (
          <p className="text-gray-500">Данных пока нет.</p>
        ) : (
          <ul>
            {financialRecords.map((record, index) => (
              <li key={index} className="border-b p-2">
                {record.type} в {record.bank_name}: {record.amount} @ {record.interest_rate}%
              </li>
            ))}
          </ul>
        )}
      </div>
    );
  };
  
  export default FinancialList;
  