import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(r => r.json());

interface Artifact {
  id: string;
  type: string;
  title: string;
  version: string;
  status: string;
  created_at?: string;
  authority_level?: string;
  seal_type?: string;
}

export default function ArchiveIndex() {
  const { data, error, isLoading } = useSWR<Artifact[]>('/v1/artifacts?status=sealed', fetcher);

  if (error) {
    return (
      <main className="px-6 py-12 max-w-4xl mx-auto">
        <div className="text-center text-red-400">
          <div className="text-4xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold mb-2">Archive Access Error</h1>
          <p className="text-red-300">Failed to load legacy archive index. Please verify API connectivity.</p>
        </div>
      </main>
    );
  }

  if (isLoading) {
    return (
      <main className="px-6 py-12 max-w-4xl mx-auto">
        <div className="text-center text-amber-200/60">
          <div className="text-4xl mb-4">📜</div>
          <h1 className="text-2xl font-bold mb-2">Loading Archive Index...</h1>
          <p>Accessing sealed artifacts from the legacy archive...</p>
          <div className="mt-4">
            <div className="animate-pulse flex space-x-4">
              <div className="flex-1 space-y-2">
                <div className="h-4 bg-amber-700/30 rounded w-3/4"></div>
                <div className="h-4 bg-amber-700/30 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        </div>
      </main>
    );
  }

  const artifactsByType = data?.reduce((acc: Record<string, Artifact[]>, artifact) => {
    if (!acc[artifact.type]) {
      acc[artifact.type] = [];
    }
    acc[artifact.type].push(artifact);
    return acc;
  }, {}) || {};

  const getTypeIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'charter': return '📜';
      case 'constitution': return '⚖️';
      case 'oath': return '🤝';
      case 'anthem': return '🎵';
      case 'ceremony': return '🕯️';
      case 'guide': return '📖';
      case 'treaty': return '🤝';
      case 'decree': return '👑';
      case 'chronicle': return '📚';
      case 'codex': return '📋';
      default: return '📄';
    }
  };

  const getAuthorityBadge = (level?: string) => {
    if (!level) return null;
    
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

  const getSealBadge = (sealType?: string) => {
    if (!sealType) return null;
    
    const sealColors = {
      'Sacred': 'bg-purple-700 text-purple-200',
      'Imperial': 'bg-red-700 text-red-200', 
      'Noble': 'bg-blue-700 text-blue-200',
      'Common': 'bg-gray-700 text-gray-200'
    };
    
    return (
      <span className={`px-2 py-1 rounded text-xs font-medium ${sealColors[sealType as keyof typeof sealColors] || sealColors.Common}`}>
        🔱 {sealType}
      </span>
    );
  };

  return (
    <main className="px-6 py-12 max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="text-6xl mb-4">🏛️</div>
        <h1 className="text-3xl font-bold text-amber-100 mb-4">Legacy Archive Index</h1>
        <p className="text-amber-200/80 text-lg max-w-2xl mx-auto">
          Sacred repository of sealed artifacts from the eternal archives. 
          These documents represent the crystallized wisdom and authority of ages past.
        </p>
        <div className="mt-4 text-amber-400/60 text-sm font-mono">
          ⚡ {data?.length || 0} SEALED ARTIFACTS ⚡ PERPETUAL ACCESS ⚡
        </div>
      </div>

      {/* Artifacts by Type */}
      {Object.keys(artifactsByType).length === 0 ? (
        <div className="text-center py-12 text-amber-200/60">
          <div className="text-4xl mb-4">📭</div>
          <h2 className="text-xl font-semibold mb-2">No Sealed Artifacts Found</h2>
          <p>The legacy archive appears to be empty or all artifacts are unsealed.</p>
        </div>
      ) : (
        <div className="space-y-8">
          {Object.entries(artifactsByType).map(([type, artifacts]) => (
            <div key={type} className="bg-amber-900/20 border border-amber-700 rounded-lg p-6">
              <div className="flex items-center space-x-3 mb-4">
                <span className="text-2xl">{getTypeIcon(type)}</span>
                <h2 className="text-xl font-semibold text-amber-100 capitalize">{type} Collection</h2>
                <span className="bg-amber-800 text-amber-200 px-2 py-1 rounded text-sm font-medium">
                  {artifacts.length}
                </span>
              </div>
              
              <div className="grid gap-4">
                {artifacts.map((artifact) => (
                  <div 
                    key={artifact.id} 
                    className="bg-amber-900/30 border border-amber-700/50 rounded-lg p-4 hover:bg-amber-900/40 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <span className="text-lg">{getTypeIcon(artifact.type)}</span>
                          <h3 className="font-semibold text-amber-100">{artifact.title}</h3>
                          <span className="text-amber-400/70 text-sm font-mono">v{artifact.version}</span>
                        </div>
                        
                        <div className="flex items-center space-x-4 text-sm text-amber-200/70">
                          <span className="font-medium capitalize">{artifact.type}</span>
                          {artifact.created_at && (
                            <span>📅 {new Date(artifact.created_at).toLocaleDateString()}</span>
                          )}
                          <span className="flex items-center space-x-1">
                            <span>🔒</span>
                            <span className="uppercase font-mono">{artifact.status}</span>
                          </span>
                        </div>
                      </div>
                      
                      <div className="flex flex-col space-y-2 ml-4">
                        {getAuthorityBadge(artifact.authority_level)}
                        {getSealBadge(artifact.seal_type)}
                      </div>
                    </div>
                    
                    <div className="mt-3 pt-3 border-t border-amber-700/30">
                      <div className="flex items-center justify-between text-xs text-amber-300/60">
                        <span className="font-mono">ID: {artifact.id}</span>
                        <span className="flex items-center space-x-1">
                          <span>🏛️</span>
                          <span>LEGACY ARCHIVE</span>
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Archive Stats */}
      {data && data.length > 0 && (
        <div className="bg-amber-900/20 border border-amber-700 rounded-lg p-6 mt-8">
          <h3 className="text-lg font-semibold text-amber-100 mb-4 flex items-center space-x-2">
            <span>📊</span>
            <span>Archive Statistics</span>
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-amber-900/30 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-amber-100">{data.length}</div>
              <div className="text-amber-200/70 text-sm">Total Sealed Artifacts</div>
            </div>
            
            <div className="bg-amber-900/30 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-amber-100">{Object.keys(artifactsByType).length}</div>
              <div className="text-amber-200/70 text-sm">Document Types</div>
            </div>
            
            <div className="bg-amber-900/30 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-amber-100">∞</div>
              <div className="text-amber-200/70 text-sm">Preservation Duration</div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="text-center pt-8 border-t border-amber-700/30">
        <p className="text-amber-400/60 text-sm">
          🔐 All artifacts in this index are permanently sealed and preserved for posterity 🔐
        </p>
        <p className="text-amber-500/40 text-xs mt-2 font-mono">
          LEGACY ARCHIVE SYSTEM • ETERNAL PRESERVATION • SOVEREIGN ACCESS
        </p>
      </div>
    </main>
  );
}