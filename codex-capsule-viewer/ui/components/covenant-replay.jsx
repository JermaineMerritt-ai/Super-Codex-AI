import React, { useState, useEffect } from 'react';

const CovenantReplay = ({ capsuleId, theme = 'dark-constellation' }) => {
  const [replayData, setReplayData] = useState(null);
  const [isReplaying, setIsReplaying] = useState(false);
  const [replayProgress, setReplayProgress] = useState(0);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    if (capsuleId) {
      loadCovenantHistory(capsuleId);
    }
  }, [capsuleId]);

  const loadCovenantHistory = async (id) => {
    // Simulate loading covenant history
    const mockEvents = [
      {
        id: 'evt_001',
        timestamp: new Date(Date.now() - 86400000), // 1 day ago
        type: 'capsule_created',
        actor: 'Custodian_Alpha',
        description: 'Capsule initialized with genesis seal'
      },
      {
        id: 'evt_002',
        timestamp: new Date(Date.now() - 43200000), // 12 hours ago
        type: 'seal_applied',
        actor: 'Flamekeeper_Beta',
        description: 'Authority seal applied to covenant'
      },
      {
        id: 'evt_003',
        timestamp: new Date(Date.now() - 21600000), // 6 hours ago
        type: 'access_granted',
        actor: 'System',
        description: 'Heir rights verified and access granted'
      },
      {
        id: 'evt_004',
        timestamp: new Date(Date.now() - 3600000), // 1 hour ago
        type: 'content_viewed',
        actor: 'Custodian_Gamma',
        description: 'Capsule content accessed and viewed'
      }
    ];

    setReplayData({
      capsuleId: id,
      totalEvents: mockEvents.length,
      covenantSeals: ['genesis', 'authority', 'honor'],
      integrityHash: 'sha256:a1b2c3d4e5f6...'
    });
    setEvents(mockEvents);
  };

  const startReplay = () => {
    setIsReplaying(true);
    setReplayProgress(0);
    
    // Simulate replay progress
    const interval = setInterval(() => {
      setReplayProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsReplaying(false);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const themeClasses = {
    'dark-constellation': {
      container: 'bg-slate-800 border border-amber-500/30 rounded-lg p-4 mt-4',
      title: 'text-amber-400 font-semibold text-lg mb-3',
      button: 'bg-amber-600 hover:bg-amber-700 text-slate-900 px-4 py-2 rounded font-medium transition-colors',
      eventCard: 'bg-slate-700 border border-amber-500/20 rounded p-3 mb-3',
      eventType: 'text-amber-300 font-medium',
      eventActor: 'text-blue-300',
      eventTime: 'text-slate-400 text-xs',
      progressBar: 'bg-slate-700',
      progressFill: 'bg-amber-500',
      icon: 'text-amber-400 text-xl mr-2'
    },
    'amber-flame': {
      container: 'bg-amber-100 border border-amber-600/40 rounded-lg p-4 mt-4 shadow-sm',
      title: 'text-amber-800 font-semibold text-lg mb-3',
      button: 'bg-amber-700 hover:bg-amber-800 text-amber-50 px-4 py-2 rounded font-medium transition-colors',
      eventCard: 'bg-amber-50 border border-amber-300 rounded p-3 mb-3',
      eventType: 'text-amber-800 font-medium',
      eventActor: 'text-blue-700',
      eventTime: 'text-slate-600 text-xs',
      progressBar: 'bg-amber-200',
      progressFill: 'bg-amber-600',
      icon: 'text-amber-700 text-xl mr-2'
    }
  };

  const currentTheme = themeClasses[theme];

  const getEventIcon = (eventType) => {
    const icons = {
      capsule_created: '🏗️',
      seal_applied: '🔒',
      access_granted: '🔓',
      content_viewed: '👁️',
      default: '📝'
    };
    return icons[eventType] || icons.default;
  };

  return (
    <div className={currentTheme.container}>
      <h3 className={currentTheme.title}>
        <span className={currentTheme.icon}>⚡</span>
        Covenant Replay
      </h3>
      
      {replayData && (
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm">
              Events: {replayData.totalEvents} | Seals: {replayData.covenantSeals.join(', ')}
            </span>
            <button
              onClick={startReplay}
              disabled={isReplaying}
              className={`${currentTheme.button} ${isReplaying ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {isReplaying ? 'Replaying...' : '▶️ Start Replay'}
            </button>
          </div>
          
          {isReplaying && (
            <div className="mb-4">
              <div className="flex items-center mb-2">
                <span className="text-sm mr-2">Progress:</span>
                <span className="text-sm">{replayProgress}%</span>
              </div>
              <div className={`w-full h-2 ${currentTheme.progressBar} rounded-full overflow-hidden`}>
                <div 
                  className={`h-full ${currentTheme.progressFill} transition-all duration-200`}
                  style={{ width: `${replayProgress}%` }}
                />
              </div>
            </div>
          )}
        </div>
      )}

      <div className="space-y-3 max-h-64 overflow-y-auto">
        {events.map((event, index) => (
          <div 
            key={event.id} 
            className={`${currentTheme.eventCard} ${
              isReplaying && (index / events.length) * 100 <= replayProgress 
                ? 'opacity-100' 
                : 'opacity-50'
            } transition-opacity`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <span className="mr-2 text-lg">
                  {getEventIcon(event.type)}
                </span>
                <div>
                  <div className={currentTheme.eventType}>
                    {event.type.replace('_', ' ').toUpperCase()}
                  </div>
                  <div className="text-sm text-gray-300 mt-1">
                    {event.description}
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className={currentTheme.eventActor}>
                  {event.actor}
                </div>
                <div className={currentTheme.eventTime}>
                  {event.timestamp.toLocaleString()}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-3 border-t border-amber-500/20">
        <div className="text-xs text-gray-500">
          <p><strong>Integrity Hash:</strong> {replayData?.integrityHash}</p>
          <p className="mt-1"><strong>Covenant Status:</strong> Valid & Sealed</p>
        </div>
      </div>

      {replayProgress === 100 && (
        <div className="mt-4 p-3 bg-green-500/10 border border-green-500/30 rounded">
          <div className="flex items-center text-green-400">
            <span className="mr-2">✅</span>
            <span className="font-medium">Replay Complete</span>
          </div>
          <p className="text-sm text-gray-300 mt-1">
            All covenant events have been successfully replayed and verified.
          </p>
        </div>
      )}
    </div>
  );
};

export default CovenantReplay;