import React, { useState, useEffect } from 'react';

const HeirRecognition = ({ capsuleId, theme = 'dark-constellation' }) => {
  const [heirStatus, setHeirStatus] = useState(null);
  const [recognitionLevel, setRecognitionLevel] = useState('none');
  const [availableRights, setAvailableRights] = useState([]);

  useEffect(() => {
    if (capsuleId) {
      analyzeHeirRights(capsuleId);
    }
  }, [capsuleId]);

  const analyzeHeirRights = async (id) => {
    // Simulate heir recognition analysis
    try {
      const response = await fetch(`/api/capsules/${id}`);
      const capsule = await response.json();
      
      const userRole = 'custodian'; // This would come from auth context
      const capsuleRights = capsule.heirRights || [];
      
      const hasRights = capsuleRights.includes(userRole);
      const level = hasRights ? 
        (capsuleRights.includes('custodian') && capsuleRights.includes('flamekeeper') ? 'full' : 'partial') : 
        'none';
      
      setHeirStatus(hasRights ? 'recognized' : 'denied');
      setRecognitionLevel(level);
      setAvailableRights(capsuleRights);
    } catch (error) {
      console.error('Failed to analyze heir rights:', error);
    }
  };

  const themeClasses = {
    'dark-constellation': {
      container: 'bg-slate-800 border border-amber-500/30 rounded-lg p-4 mt-4',
      title: 'text-amber-400 font-semibold text-lg mb-3',
      status: {
        recognized: 'text-green-400',
        denied: 'text-red-400',
        pending: 'text-yellow-400'
      },
      badge: 'bg-amber-600/20 text-amber-300 px-2 py-1 rounded text-sm mr-2',
      icon: 'text-amber-400 text-xl mr-2'
    },
    'amber-flame': {
      container: 'bg-amber-100 border border-amber-600/40 rounded-lg p-4 mt-4 shadow-sm',
      title: 'text-amber-800 font-semibold text-lg mb-3',
      status: {
        recognized: 'text-green-700',
        denied: 'text-red-700',
        pending: 'text-yellow-700'
      },
      badge: 'bg-amber-200 text-amber-800 px-2 py-1 rounded text-sm mr-2',
      icon: 'text-amber-700 text-xl mr-2'
    }
  };

  const currentTheme = themeClasses[theme];
  
  const getRecognitionIcon = () => {
    switch (heirStatus) {
      case 'recognized': return '✓';
      case 'denied': return '✗';
      default: return '?';
    }
  };

  const getRecognitionMessage = () => {
    switch (heirStatus) {
      case 'recognized':
        return `Access granted with ${recognitionLevel} privileges`;
      case 'denied':
        return 'Access denied - insufficient heir rights';
      default:
        return 'Analyzing heir recognition...';
    }
  };

  return (
    <div className={currentTheme.container}>
      <h3 className={currentTheme.title}>
        <span className={currentTheme.icon}>👑</span>
        Heir Recognition
      </h3>
      
      <div className="flex items-center mb-4">
        <span className={currentTheme.icon}>
          {getRecognitionIcon()}
        </span>
        <span className={currentTheme.status[heirStatus] || 'text-gray-400'}>
          {getRecognitionMessage()}
        </span>
      </div>

      <div className="mb-4">
        <h4 className="text-sm font-medium mb-2">Required Rights for Access:</h4>
        <div>
          {availableRights.length > 0 ? (
            availableRights.map((right, index) => (
              <span key={index} className={currentTheme.badge}>
                {right}
              </span>
            ))
          ) : (
            <span className="text-gray-500 text-sm">No specific rights required</span>
          )}
        </div>
      </div>

      <div className="text-sm text-gray-500">
        <p>Recognition Level: <strong className={currentTheme.status[heirStatus]}>{recognitionLevel}</strong></p>
        <p className="mt-1">Current Role: <strong>custodian</strong></p>
      </div>

      {heirStatus === 'recognized' && (
        <div className="mt-4 p-3 bg-green-500/10 border border-green-500/30 rounded">
          <div className="flex items-center text-green-400">
            <span className="mr-2">🔓</span>
            <span className="font-medium">Capsule Unlocked</span>
          </div>
          <p className="text-sm text-gray-300 mt-1">
            You have been granted access to this capsule's contents and covenant seals.
          </p>
        </div>
      )}
    </div>
  );
};

export default HeirRecognition;