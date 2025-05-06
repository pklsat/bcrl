import { useState } from 'react';

function JobList() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false); // ← 初期値 false に変更
  const [error, setError] = useState(null);

  // 非同期でジョブ一覧を取得する関数
  const fetchJobs = async () => {
    setLoading(true);
    setError(null); // エラーをクリア

    try {
      const response = await fetch('/api/jobs/');
      if (!response.ok) throw new Error('データの取得に失敗しました');
      const data = await response.json();
      setJobs(data); // ← 配列をそのままセット
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>ジョブ一覧</h1>

      {/* ボタンクリックで fetchJobs を実行 */}
      <button onClick={fetchJobs}>ジョブ一覧を取得</button>

      {/* 状態に応じた表示 */}
      {loading && <p>読み込み中...</p>}
      {error && <p style={{ color: 'red' }}>エラー: {error}</p>}

      <ul>
        {jobs.map(job => (
          <li key={job.req_id}>
            <p><strong>Req ID:</strong> {job.req_id}</p>
            <p><strong>API:</strong> {job.api}</p>
            <p><strong>Status:</strong> {job.status}</p>
            <p><strong>Req Date:</strong> {job.req_date}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default JobList;