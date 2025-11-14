import React, { useState, useEffect } from 'react';

const CapsuleDetail = ({ capsuleId, theme = 'dark-constellation' }) => {
  const [capsule, setCapsule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (capsuleId) {
      fetchCapsuleDetail(capsuleId);
    }
  }, [capsuleId]);

  const fetchCapsuleDetail = async (id) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/capsules/${id}`);
      if (!response.ok) throw new Error('Failed to fetch capsule details');
      const data = await response.json();
      setCapsule(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const themeClasses = {
    'dark-constellation': {
      container: 'bg-slate-800 border border-amber-500/30 rounded-lg p-6',
      title: 'text-amber-300 font-bold text-2xl mb-4',
      sigil: 'text-4xl text-amber-400 mb-4',
      content: 'text-slate-300 leading-relaxed mb-6',
      sectionTitle: 'text-amber-400 font-semibold text-lg mb-3',
      badge: 'bg-amber-600/20 text-amber-300 px-3 py-1 rounded-full text-sm mr-2 mb-2 inline-block',
      timestamp: 'text-slate-500 text-sm'
    },
    'amber-flame': {
      container: 'bg-amber-100 border border-amber-600/40 rounded-lg p-6 shadow-md',
      title: 'text-amber-900 font-bold text-2xl mb-4',
      sigil: 'text-4xl text-amber-700 mb-4',
      content: 'text-slate-700 leading-relaxed mb-6',
      sectionTitle: 'text-amber-800 font-semibold text-lg mb-3',
      badge: 'bg-amber-200 text-amber-800 px-3 py-1 rounded-full text-sm mr-2 mb-2 inline-block',
      timestamp: 'text-slate-600 text-sm'
    }
  };

  const currentTheme = themeClasses[theme];

  if (loading) {
    return (
      <div className={currentTheme.container}>
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-amber-400"></div>
          <span className="ml-3">Loading capsule details...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={currentTheme.container}>
        <div className="text-red-400 text-center py-8">
          <p>Error loading capsule details</p>
          <p className="text-sm mt-2">{error}</p>
        </div>
      </div>
    );
  }

  if (!capsule) {
    return (
      <div className={currentTheme.container}>
        <p className="text-center py-8">No capsule data available</p>
      </div>
    );
  }

  return (
    <div className={currentTheme.container}>
      <div className="flex items-center mb-6">
        <div className={currentTheme.sigil}>
          {capsule.sigil}
        </div>
        <div className="ml-4">
          <h1 className={currentTheme.title}>
            {capsule.title}
          </h1>
          <p className={currentTheme.timestamp}>
            Created: {new Date(capsule.createdAt).toLocaleDateString()} at {new Date(capsule.createdAt).toLocaleTimeString()}
          </p>
        </div>
      </div>

      {capsule.content && (
        <div className="mb-6">
          <h2 className={currentTheme.sectionTitle}>Content</h2>
          <div className={currentTheme.content}>
            {capsule.content}
          </div>
        </div>
      )}

      {capsule.heirRights && capsule.heirRights.length > 0 && (
        <div className="mb-6">
          <h2 className={currentTheme.sectionTitle}>Heir Rights</h2>
          <div>
            {capsule.heirRights.map((right, index) => (
              <span key={index} className={currentTheme.badge}>
                {right}
              </span>
            ))}
          </div>
        </div>
      )}

      {capsule.covenantSeals && capsule.covenantSeals.length > 0 && (
        <div className="mb-6">
          <h2 className={currentTheme.sectionTitle}>Covenant Seals</h2>
          <div>
            {capsule.covenantSeals.map((seal, index) => (
              <span key={index} className={currentTheme.badge}>
                {seal}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="border-t border-amber-500/20 pt-4">
        <h2 className={currentTheme.sectionTitle}>Capsule Metadata</h2>
        <div className="space-y-2">
          <div className={currentTheme.timestamp}>
            <strong>ID:</strong> {capsule.id}
          </div>
          <div className={currentTheme.timestamp}>
            <strong>Sigil:</strong> {capsule.sigil} (Unicode: U+{capsule.sigil.codePointAt(0).toString(16).toUpperCase()})
          </div>
        </div>
      </div>
    </div>
  );
};

export default CapsuleDetail;