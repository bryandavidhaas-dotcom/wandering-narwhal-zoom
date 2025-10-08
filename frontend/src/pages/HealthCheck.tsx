import { useState, useEffect } from 'react';

const HealthCheck = () => {
  const [status, setStatus] = useState('checking...');
  const [dbStatus, setDbStatus] = useState('checking...');

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/health');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setStatus(data.status);
        setDbStatus(data.database);
      } catch (error) {
        setStatus('error');
        setDbStatus('error');
        console.error("Failed to fetch health status:", error);
      }
    };

    fetchHealth();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-gray-800">System Status</h1>
        <div className="mt-4">
          <p className="text-lg">
            <span className="font-semibold">API Status:</span>
            <span className={`ml-2 px-2 py-1 rounded-full text-white ${status === 'ok' ? 'bg-green-500' : 'bg-red-500'}`}>
              {status}
            </span>
          </p>
          <p className="mt-2 text-lg">
            <span className="font-semibold">Database Status:</span>
            <span className={`ml-2 px-2 py-1 rounded-full text-white ${dbStatus === 'connected' ? 'bg-green-500' : 'bg-red-500'}`}>
              {dbStatus}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default HealthCheck;