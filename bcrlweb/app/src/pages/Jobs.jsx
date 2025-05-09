import { useState } from 'react';
import { Link } from 'react-router-dom';

function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // ジョブ一覧を取得
  const fetchJobs = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/jobs');
      if (!response.ok) throw new Error('データの取得に失敗しました');
      const data = await response.json();
      const jobArray = Object.values(data.jobs || {});
      setJobs(jobArray);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ジョブを削除
  const handleDelete = async (req_id) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/jobs/delete/${req_id}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('削除に失敗しました');

      setJobs(prevJobs => prevJobs.filter(job => job.req_id !== req_id));
      alert('ジョブが削除されました');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>ジョブ一覧</h1>
      <button onClick={fetchJobs}>ジョブ一覧を取得</button>

      {loading && <p>読み込み中...</p>}
      {error && <p style={{ color: 'red' }}>エラー: {error}</p>}

      <ul>
        {jobs.map(job => (
          <li key={job.req_id}>
            <p><strong>Req ID:</strong> {job.req_id}</p>
            <p><strong>API:</strong> {job.api}</p>
            <p><strong>Status:</strong> {job.status}</p>
            <p><strong>Req Date:</strong> {job.req_date}</p>
            <Link to={`/jobs/${job.req_id}`}>Result</Link>
            <div>
              <button onClick={() => handleDelete(job.req_id)}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Jobs;
