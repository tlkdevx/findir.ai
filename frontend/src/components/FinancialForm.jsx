import { useState } from "react";

const FinancialForm = ({ setFinancialRecords }) => {
  const [formData, setFormData] = useState({
    user_id: 1,
    type: "deposit",
    bank_name: "",
    amount: "",
    interest_rate: "",
    start_date: "",
    end_date: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch(`http://127.0.0.1:8000/users/${formData.user_id}/finance`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      const newRecord = await response.json();
      setFinancialRecords((prev) => [...prev, newRecord]);
      setFormData({
        user_id: 1,
        type: "deposit",
        bank_name: "",
        amount: "",
        interest_rate: "",
        start_date: "",
        end_date: "",
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <h2 className="text-xl font-bold mb-4">Добавить финансовые данные</h2>
      <div className="mb-4">
        <label className="block text-gray-700">Тип</label>
        <select name="type" value={formData.type} onChange={handleChange} className="border p-2 w-full">
          <option value="deposit">Депозит</option>
          <option value="loan">Кредит</option>
        </select>
      </div>
      <div className="mb-4">
        <label className="block text-gray-700">Банк</label>
        <input type="text" name="bank_name" value={formData.bank_name} onChange={handleChange} className="border p-2 w-full" required />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700">Сумма</label>
        <input type="number" name="amount" value={formData.amount} onChange={handleChange} className="border p-2 w-full" required />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700">Процентная ставка</label>
        <input type="number" step="0.01" name="interest_rate" value={formData.interest_rate} onChange={handleChange} className="border p-2 w-full" required />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700">Дата начала</label>
        <input type="date" name="start_date" value={formData.start_date} onChange={handleChange} className="border p-2 w-full" required />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700">Дата окончания</label>
        <input type="date" name="end_date" value={formData.end_date} onChange={handleChange} className="border p-2 w-full" required />
      </div>
      <button type="submit" className="bg-blue-500 text-white p-2 rounded">Добавить</button>
    </form>
  );
};

export default FinancialForm;
