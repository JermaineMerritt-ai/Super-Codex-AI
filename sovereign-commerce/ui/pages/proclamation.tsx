export default function Proclamation() {
  return (
    <main className="px-6 py-12">
      <section className="text-center space-y-4">
        <img src="/assets/seal.svg" alt="Codex Seal" className="mx-auto h-96 w-96" />
        <h1 className="text-4xl font-bold">Public Release Proclamation</h1>
        <p>The Codex is complete, sovereign, and eternal. It is open to all participants.</p>
        
        {/* Additional ceremonial elements */}
        <div className="mt-12 space-y-6">
          <div className="text-amber-400/70 text-sm font-mono tracking-widest">
            ✦ SOVEREIGN CODEX ✦
          </div>
          
          <div className="max-w-2xl mx-auto text-amber-200/80 text-base leading-relaxed">
            <p className="mb-4">
              By decree of the Sacred Council and in accordance with the Eternal Charter, 
              this proclamation marks the completion of the Great Work.
            </p>
            
            <p className="mb-4">
              The Codex stands as testament to collaborative sovereignty, 
              eternal preservation, and the sacred flame of knowledge.
            </p>
            
            <p>
              All participants, custodians, and contributors are welcomed 
              into this covenant of perpetual stewardship.
            </p>
          </div>
          
          <div className="border-t border-amber-700/50 pt-6 text-amber-400/60 text-xs">
            Sealed by the Authority of the Codex • Eternal and Immutable
          </div>
        </div>
      </section>
    </main>
  );
}