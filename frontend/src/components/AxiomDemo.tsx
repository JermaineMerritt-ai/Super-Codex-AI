import React, { useState, useEffect } from 'react';

interface AxiomDemoProps {
  className?: string;
}

export function AxiomDemo({ className }: AxiomDemoProps) {
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const checkHealth = async () => {
    setLoading(true);
    try {
      const response = await fetch('/health/');
      const healthData = await response.json();
      setHealth(healthData);
      console.log('✅ Axiom health check successful');
    } catch (error: any) {
      console.error('❌ Health check failed:', error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div className={`space-y-4 ${className}`}>
      <div className="border rounded-lg p-4">
        <div className="mb-4">
          <h2 className="text-xl font-bold">🔥 Axiom Flame Demo</h2>
          <p className="text-gray-600">
            Demonstrating the Super-Codex-AI ceremonial system
          </p>
        </div>
        <div className="space-y-4">
          <button
            onClick={checkHealth}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Checking...' : 'Check System Health'}
          </button>
          
          {health && (
            <div className="p-4 bg-gray-100 rounded">
              <h3 className="font-semibold mb-2">System Status</h3>
              <pre className="text-sm">
                {JSON.stringify(health, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}