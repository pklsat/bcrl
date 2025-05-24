import { useState } from 'react';

function Submit() {
  const [formData, setFormData] = useState({
    api: 'soc',
    current_soc: 65.3,
    year: 2022,
    day: 1,
    hour: 0,
    minute: 30,
    month: 9,
  });

  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    // 数値フィールドは float に変換
    const parsedValue = ['current_soc', 'day', 'hour', 'minute', 'month'].includes(name)
      ? parseFloat(value)
      : value;
    setFormData((prev) => ({ ...prev, [name]: parsedValue }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResponse(null);
    try {
      const res = await fetch('/api/submit', {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) throw new Error('ジョブの登録に失敗しました');

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>ジョブ登録</h1>
      <form onSubmit={handleSubmit}>
        <label>
          API:
          <input type="text" name="api" value={formData.api} onChange={handleChange} />
        </label><br />
        <label>
          Current SOC:
          <input type="number" step="0.1" name="current_soc" value={formData.current_soc} onChange={handleChange} />
        </label><br />
        <label>
          Year:
          <input type="number" name="year" value={formData.year} onChange={handleChange} />
        </label><br />
        <label>
          Month:
          <input type="number" name="month" value={formData.month} onChange={handleChange} />
        </label><br />
        <label>
          Day:
          <input type="number" name="day" value={formData.day} onChange={handleChange} />
        </label><br />
        <label>
          Hour:
          <input type="number" name="hour" value={formData.hour} onChange={handleChange} />
        </label><br />
        <label>
          Minute:
          <input type="number" name="minute" value={formData.minute} onChange={handleChange} />
        </label><br />
        <button type="submit">ジョブを送信</button>
      </form>

      {response && <pre>{JSON.stringify(response, null, 2)}</pre>}
      {error && <p style={{ color: 'red' }}>エラー: {error}</p>}
    </div>
  );
}

export default Submit;
