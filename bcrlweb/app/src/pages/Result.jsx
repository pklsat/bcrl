import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function Result() {
    const { req_id } = useParams();
    const [res, setResponse] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getJobResult = async () => {
            setLoading(true);
            setError(null);
            try {
                const response = await fetch(`/api/jobs/results/${req_id}`);
                if (!response.ok) throw new Error('Failed to fetch job result');
                const data = await response.json();
                setResponse(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        getJobResult();
    }, [req_id]);


    return (
        <div>
            <h1>Results</h1>
            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>Error: {error}</p>}

            {res ? (
                <div>
                    <p><strong>req_id:</strong> {res.req_id}</p>
                    <p><strong>api:</strong> {res.api}</p>
                    <p><strong>Message:</strong> {res.message}</p>
                    <h3>Schedule</h3>
                    <ul>
                        {res.soc_response.schedule.map((entry, index) => (
                            <li key={index}>
                                <strong>Hour:</strong> {entry.hour}, <strong>Minute:</strong> {entry.minute}, <strong>SOC:</strong> {entry.soc}
                            </li>
                        ))}
                    </ul>
                    <h3>Metadata</h3>
                    <p><strong>Request SOC:</strong> {res.soc_response.metadata.request_soc}</p>
                    <p><strong>Request Date:</strong> {res.soc_response.metadata.request_date}</p>
                    <p><strong>Generated At:</strong> {res.soc_response.metadata.generated_at}</p>
                    <p><strong>Message:</strong> {res.soc_response.metadata.message}</p>
                </div>
            ) : (
                <p>No job found with this ID.</p>
            )}
        </div>
    );
}

export default Result;
