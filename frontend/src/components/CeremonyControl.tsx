import React, { useState, useEffect } from 'react';

interface CeremonyControlProps {
  onCeremonyComplete?: (ceremony: any) => void;
}

export default function CeremonyControl({ onCeremonyComplete }: CeremonyControlProps) {
  const [formData, setFormData] = useState({
    actor: 'Custodian',
    realm: 'PL-001',
    capsule: 'Sovereign Crown',
    intent: 'System.Invocation'
  });
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const notify = (message: string, type: string = 'info') => {
    const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
    console.log(`${icon} ${message}`);
  };

  const handleInvokeCeremony = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/ceremonial/invoke', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const result = await response.json();
      setResults(prev => [result, ...prev]);
      onCeremonyComplete?.(result);
      notify(`🔥 Ceremony dispatched: ${result.dispatch_id}`, 'success');
    } catch (error: any) {
      notify(`❌ Ceremony failed: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleReasonCeremony = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/reasoning', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const result = await response.json();
      setResults(prev => [result, ...prev]);
      notify(`💭 Reasoning completed: ${result.dispatch_id}`, 'success');
    } catch (error: any) {
      notify(`❌ Reasoning failed: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleHealthCheck = async () => {
    try {
      const response = await fetch('/health/ceremony');
      const health = await response.json();
      notify(`🏥 Ceremony Health: ${health.status}`, 'info');
    } catch (error: any) {
      notify(`⚠️ Health check failed: ${error.message}`, 'error');
    }
  };

  return (
    <div className="space-y-6">
      <div className="border rounded-lg p-4">
        <div className="mb-4">
          <h2 className="text-xl font-bold">🔥 Ceremony Control</h2>
          <p className="text-gray-600">
            Invoke ceremonial processes and manage dominion operations
          </p>
        </div>
        <div className="grid gap-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Actor</label>
              <input
                type="text"
                value={formData.actor}
                onChange={(e) => handleInputChange('actor', e.target.value)}
                placeholder="Enter actor name"
                className="w-full px-3 py-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Realm</label>
              <input
                type="text"
                value={formData.realm}
                onChange={(e) => handleInputChange('realm', e.target.value)}
                placeholder="Enter realm ID"
                className="w-full px-3 py-2 border rounded"
              />
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Capsule</label>
              <input
                type="text"
                value={formData.capsule}
                onChange={(e) => handleInputChange('capsule', e.target.value)}
                placeholder="Enter capsule type"
                className="w-full px-3 py-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Intent</label>
              <input
                type="text"
                value={formData.intent}
                onChange={(e) => handleInputChange('intent', e.target.value)}
                placeholder="Enter intent"
                className="w-full px-3 py-2 border rounded"
              />
            </div>
          </div>
          
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={handleInvokeCeremony}
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Processing...' : '🔥 Invoke Ceremony'}
            </button>
            
            <button
              onClick={handleReasonCeremony}
              disabled={loading}
              className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50"
            >
              💭 Reason Ceremony
            </button>
            
            <button
              onClick={handleHealthCheck}
              className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
            >
              🏥 Health Check
            </button>
          </div>
        </div>
      </div>
      
      {results.length > 0 && (
        <div className="border rounded-lg p-4">
          <h3 className="text-lg font-bold mb-4">📋 Recent Ceremonies</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {results.map((result, index) => (
              <div key={index} className="p-3 bg-gray-50 rounded text-sm">
                <div className="font-mono text-xs text-gray-600">
                  {result.dispatch_id} - {result.timestamp}
                </div>
                <div className="mt-1">
                  <strong>{result.actor}</strong> → <strong>{result.realm}</strong> → <strong>{result.capsule}</strong>
                </div>
                <div className="text-gray-600 text-xs mt-1">
                  Intent: {result.intent}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}