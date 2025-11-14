import { useState, useEffect } from 'react';
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(r => r.json());

interface DashboardMetrics {
  total_artifacts: number;
  sealed_artifacts: number;
  pending_ceremonies: number;
  active_councils: number;
  recent_activities: Array<{
    id: string;
    type: string;
    description: string;
    timestamp: string;
    authority_level: string;
  }>;
}

export default function CouncilDashboard() {
  const { data: metrics, error, isLoading } = useSWR<DashboardMetrics>('/v1/dashboard/metrics', fetcher);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatDateTime = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZoneName: 'short'
    }).format(date);
  };

  const getActivityIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'ceremony': return '🕯️';
      case 'artifact': return '📜';
      case 'seal': return '🔱';
      case 'council': return '👥';
      case 'governance': return '⚖️';
      default: return '📋';
    }
  };

  const getAuthorityBadge = (level: string) => {
    const colors = {
      'Supreme': 'bg-amber-600 text-amber-100',
      'High': 'bg-amber-700 text-amber-200',
      'Standard': 'bg-amber-800 text-amber-300',
      'Basic': 'bg-amber-900 text-amber-400'
    };
    
    return (
      <span className={`px-2 py-1 rounded text-xs font-medium ${colors[level as keyof typeof colors] || colors.Basic}`}>
        {level}
      </span>
    );
  };

  if (error) {
    return (
      <main className="px-6 py-12 max-w-6xl mx-auto">
        <div className="text-center text-red-400">
          <div className="text-4xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold mb-2">Dashboard Access Error</h1>
          <p className="text-red-300">Failed to load council metrics. Please verify API connectivity.</p>
        </div>
      </main>
    );
  }

  return (
    <main className="px-6 py-12 max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="text-5xl mb-4">👑</div>
        <h1 className="text-3xl font-bold text-amber-100 mb-2">Sacred Council Dashboard</h1>
        <p className="text-amber-200/80 text-lg">
          Command center for governance, ceremonies, and archive management
        </p>
        <div className="mt-4 text-amber-400/70 text-sm font-mono">
          {formatDateTime(currentTime)}
        </div>
      </div>

      {/* Metrics Cards */}
      {isLoading ? (
        <div className="grid md:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="bg-amber-900/20 border border-amber-700 rounded-lg p-6 animate-pulse">
              <div className="h-4 bg-amber-700/30 rounded w-3/4 mb-2"></div>
              <div className="h-8 bg-amber-700/30 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      ) : metrics ? (
        <div className="grid md:grid-cols-4 gap-6">
          <div className="bg-amber-900/20 border border-amber-700 rounded-lg p-6 text-center">
            <div className="text-2xl mb-2">📚</div>
            <div className="text-2xl font-bold text-amber-100">{metrics.total_artifacts}</div>
            <div className="text-amber-200/70 text-sm">Total Artifacts</div>
          </div>
          
          <div className="bg-amber-900/20 border border-amber-700 rounded-lg p-6 text-center">
            <div className="text-2xl mb-2">🔒</div>
            <div className="text-2xl font-bold text-amber-100">{metrics.sealed_artifacts}</div>
            <div className="text-amber-200/70 text-sm">Sealed Artifacts</div>
          </div>
          
          <div className="bg-amber-900/20 border border-amber-700 rounded-lg p-6 text-center">
            <div className="text-2xl mb-2">🕯️</div>
            <div className="text-2xl font-bold text-amber-100">{metrics.pending_ceremonies}</div>
            <div className="text-amber-200/70 text-sm">Pending Ceremonies</div>
          </div>
          
          <div className="bg-amber-900/20 border border-amber-700 rounded-lg p-6 text-center">
            <div className="text-2xl mb-2">👥</div>
            <div className="text-2xl font-bold text-amber-100">{metrics.active_councils}</div>
            <div className="text-amber-200/70 text-sm">Active Councils</div>
          </div>
        </div>
      ) : null}

      {/* Navigation Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        <a 
          className="bg-amber-900/20 border border-amber-700 p-6 rounded-lg hover:bg-amber-900/30 transition-colors group" 
          href="/archive-index"
        >
          <div className="flex items-center space-x-4">
            <div className="text-3xl group-hover:scale-110 transition-transform">🏛️</div>
            <div>
              <h2 className="text-xl font-semibold text-amber-100">Archive Index</h2>
              <p className="text-amber-200/70 text-sm mt-1">
                Access sealed artifacts and legacy documents from the eternal archives
              </p>
              <div className="flex items-center space-x-2 mt-2">
                <span className="text-amber-400/60 text-xs">📜 SEALED</span>
                <span className="text-amber-400/60 text-xs">•</span>
                <span className="text-amber-400/60 text-xs">🔐 PERPETUAL</span>
              </div>
            </div>
          </div>
        </a>
        
        <a 
          className="bg-amber-900/20 border border-amber-700 p-6 rounded-lg hover:bg-amber-900/30 transition-colors group" 
          href="/ceremonies"
        >
          <div className="flex items-center space-x-4">
            <div className="text-3xl group-hover:scale-110 transition-transform">🕯️</div>
            <div>
              <h2 className="text-xl font-semibold text-amber-100">Schedule Ceremony</h2>
              <p className="text-amber-200/70 text-sm mt-1">
                Organize sacred ceremonies, oaths, and governance rituals
              </p>
              <div className="flex items-center space-x-2 mt-2">
                <span className="text-amber-400/60 text-xs">⚡ ACTIVE</span>
                <span className="text-amber-400/60 text-xs">•</span>
                <span className="text-amber-400/60 text-xs">🎭 CEREMONIAL</span>
              </div>
            </div>
          </div>
        </a>
      </div>

      {/* Additional Dashboard Sections */}
      <div className="grid md:grid-cols-3 gap-6">
        <a 
          className="bg-amber-900/20 border border-amber-700 p-4 rounded-lg hover:bg-amber-900/30 transition-colors group" 
          href="/charter"
        >
          <div className="text-center">
            <div className="text-2xl mb-2 group-hover:scale-110 transition-transform">🔥</div>
            <h3 className="font-semibold text-amber-100">Eternal Charter</h3>
            <p className="text-amber-200/60 text-xs mt-1">Sacred Constitution</p>
          </div>
        </a>
        
        <a 
          className="bg-amber-900/20 border border-amber-700 p-4 rounded-lg hover:bg-amber-900/30 transition-colors group" 
          href="/governance"
        >
          <div className="text-center">
            <div className="text-2xl mb-2 group-hover:scale-110 transition-transform">⚖️</div>
            <h3 className="font-semibold text-amber-100">Governance Rules</h3>
            <p className="text-amber-200/60 text-xs mt-1">Authority & Seals</p>
          </div>
        </a>
        
        <a 
          className="bg-amber-900/20 border border-amber-700 p-4 rounded-lg hover:bg-amber-900/30 transition-colors group" 
          href="/registry"
        >
          <div className="text-center">
            <div className="text-2xl mb-2 group-hover:scale-110 transition-transform">📋</div>
            <h3 className="font-semibold text-amber-100">Sacred Registry</h3>
            <p className="text-amber-200/60 text-xs mt-1">Realms & Capsules</p>
          </div>
        </a>
      </div>

      {/* Recent Activity */}
      {metrics?.recent_activities && metrics.recent_activities.length > 0 && (
        <div className="bg-amber-900/20 border border-amber-700 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-amber-100 mb-4 flex items-center space-x-2">
            <span>📊</span>
            <span>Recent Council Activity</span>
          </h2>
          
          <div className="space-y-4">
            {metrics.recent_activities.slice(0, 5).map((activity) => (
              <div key={activity.id} className="flex items-center justify-between p-3 bg-amber-900/30 rounded-lg">
                <div className="flex items-center space-x-3">
                  <span className="text-lg">{getActivityIcon(activity.type)}</span>
                  <div>
                    <p className="text-amber-100 text-sm font-medium">{activity.description}</p>
                    <p className="text-amber-300/60 text-xs">
                      {new Date(activity.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {getAuthorityBadge(activity.authority_level)}
                  <span className="text-amber-400/60 text-xs capitalize">{activity.type}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="text-center pt-8 border-t border-amber-700/30">
        <p className="text-amber-400/60 text-sm">
          🏛️ Sacred Council Authority • Eternal Governance • Sovereign Command 🏛️
        </p>
        <p className="text-amber-500/40 text-xs mt-2 font-mono">
          COUNCIL DASHBOARD • PERPETUAL ACCESS • SUPREME AUTHORITY
        </p>
      </div>
    </main>
  );
}