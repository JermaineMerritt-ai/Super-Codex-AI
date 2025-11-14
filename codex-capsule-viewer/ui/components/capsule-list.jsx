import React, { useState, useEffect } from 'react';
import CapsuleDetail from './capsule-detail';
import HeirRecognition from './heir-recognition';
import CovenantReplay from './covenant-replay';

const CapsuleList = ({ theme = 'dark-constellation' }) => {
  const [capsules, setCapsules] = useState([]);
  const [selectedCapsule, setSelectedCapsule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCapsules();
  }, []);

  const fetchCapsules = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/capsules');
      if (!response.ok) throw new Error('Failed to fetch capsules');
      const data = await response.json();
      setCapsules(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const themeClasses = {
    'dark-constellation': {
      container: 'bg-slate-900 text-amber-100 min-h-screen',
      card: 'bg-slate-800 border border-amber-500/30 rounded-lg p-4 hover:border-amber-400/60 transition-all cursor-pointer',
      title: 'text-amber-300 font-bold text-lg mb-2',
      sigil: 'text-2xl mb-2 text-amber-400',
      content: 'text-slate-300 text-sm',
      button: 'bg-amber-600 hover:bg-amber-700 text-slate-900 px-4 py-2 rounded font-medium transition-colors'
    },
    'amber-flame': {
      container: 'bg-amber-50 text-slate-900 min-h-screen',
      card: 'bg-amber-100 border border-amber-600/40 rounded-lg p-4 hover:border-amber-700/80 transition-all cursor-pointer shadow-md',
      title: 'text-amber-900 font-bold text-lg mb-2',
      sigil: 'text-2xl mb-2 text-amber-700',
      content: 'text-slate-700 text-sm',
      button: 'bg-amber-700 hover:bg-amber-800 text-amber-50 px-4 py-2 rounded font-medium transition-colors'
    }
  };

  const currentTheme = themeClasses[theme];

  if (loading) {
    return (
      <div className={currentTheme.container}>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-400"></div>
          <span className="ml-3">Loading capsules...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={currentTheme.container}>
        <div className="flex items-center justify-center h-64">
          <div className="text-red-400 text-center">
            <p className="mb-2">Error loading capsules</p>
            <p className="text-sm">{error}</p>
            <button 
              onClick={fetchCapsules}
              className={currentTheme.button + " mt-4"}
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={currentTheme.container}>
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-amber-300 mb-2">
            Codex Capsule Viewer
          </h1>
          <p className="text-slate-400">
            Sacred knowledge preserved in temporal capsules
          </p>
        </header>

        {selectedCapsule ? (
          <div>
            <button
              onClick={() => setSelectedCapsule(null)}
              className={currentTheme.button + " mb-6"}
            >
              ← Back to Capsules
            </button>
            <CapsuleDetail 
              capsuleId={selectedCapsule} 
              theme={theme}
            />
            <div className="mt-8 space-y-6">
              <HeirRecognition 
                capsuleId={selectedCapsule} 
                theme={theme}
              />
              <CovenantReplay 
                capsuleId={selectedCapsule} 
                theme={theme}
              />
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {capsules.map((capsule) => (
              <div
                key={capsule.id}
                className={currentTheme.card}
                onClick={() => setSelectedCapsule(capsule.id)}
              >
                <div className={currentTheme.sigil}>
                  {capsule.sigil}
                </div>
                <h2 className={currentTheme.title}>
                  {capsule.title}
                </h2>
                <p className={currentTheme.content}>
                  {capsule.summary || 'No summary available'}
                </p>
                <div className="mt-3 text-xs text-slate-500">
                  Created: {new Date(capsule.createdAt).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CapsuleList;