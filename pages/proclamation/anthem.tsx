// pages/proclamation/anthem.tsx
import { useEffect, useState } from "react";

interface Stanza {
  title: string;
  lines: string[];
}

interface AnthemArtifact {
  id: string;
  title: string;
  stanzas: Stanza[];
  seals: {
    checksum_sha256: string | null;
    sealed_at: string | null;
  };
}

export default function AnthemProclamation() {
  const [artifact, setArtifact] = useState<AnthemArtifact | null>(null);
  const [verified, setVerified] = useState(false);

  useEffect(() => {
    async function fetchAnthem() {
      const res = await fetch("/api/artifacts/anthem-universal-adoption-v1");
      const data: AnthemArtifact = await res.json();

      // Verify checksum
      const encoder = new TextEncoder();
      const raw = JSON.stringify(data);
      const buffer = encoder.encode(raw);
      const digest = await crypto.subtle.digest("SHA-256", buffer);
      const hashArray = Array.from(new Uint8Array(digest));
      const hashHex = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");

      setVerified(hashHex === data.seals.checksum_sha256);
      setArtifact(data);
    }
    fetchAnthem();
  }, []);

  if (!artifact) return <p>Loading Anthem...</p>;

  return (
    <div className="proclamation-container">
      <h1 className="text-4xl font-bold text-center mb-6">
        {artifact.title}
      </h1>

      {artifact.stanzas.map((stanza, idx) => (
        <section key={idx} className="mb-8">
          <h2 className="text-2xl font-semibold mb-2">{stanza.title}</h2>
          <div className="pl-4 border-l-2 border-yellow-500">
            {stanza.lines.map((line, i) => (
              <p key={i} className="text-lg italic">{line}</p>
            ))}
          </div>
        </section>
      ))}

      <footer className="mt-10 text-sm text-gray-500 text-center">
        {verified ? (
          <span>✅ Anthem checksum verified — sealed at {artifact.seals.sealed_at}</span>
        ) : (
          <span>⚠️ Checksum mismatch — artifact integrity not confirmed</span>
        )}
      </footer>
    </div>
  );
}