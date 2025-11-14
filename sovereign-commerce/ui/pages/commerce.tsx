// Original Sovereign Commerce UI - preserved for reference
import { useState } from 'react'

interface ModuleCard {
  title: string
  description: string
  path: string
  status: 'active' | 'pending' | 'sealed'
}

export default function SovereignCommerce() {
  const [selectedModule, setSelectedModule] = useState<string | null>(null)

  const modules: ModuleCard[] = [
    {
      title: "Catalog",
      description: "Sacred inventory and covenant-bound offerings.",
      path: "/catalog",
      status: 'active'
    },
    {
      title: "Checkout",
      description: "Ceremonial exchange and radiant transactions.",
      path: "/checkout", 
      status: 'active'
    },
    {
      title: "Funder Dashboard",
      description: "Diaspora oversight and honor recognition.",
      path: "/dashboard",
      status: 'active'
    }
  ]

  const handleModuleClick = (modulePath: string) => {
    // In a real app, this would navigate to the module
    setSelectedModule(modulePath)
    console.log(`Navigating to: ${modulePath}`)
  }

  return (
    <main className="min-h-screen bg-black text-amber-200">
      <section className="max-w-4xl mx-auto py-20 px-6">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="sovereign-title mb-6">
            Sovereign Commerce — Diaspora Funders
          </h1>
          <p className="sovereign-subtitle text-xl">
            Honor, recognition, and radiant exchange.
          </p>
          <div className="mt-4 text-amber-400/70 text-sm">
            ✦ Covenant-Sealed Platform ✦
          </div>
        </div>

        {/* Module Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {modules.map((module) => (
            <div 
              key={module.title} 
              className={`sovereign-card cursor-pointer transform transition-all duration-200 hover:scale-105 ${
                selectedModule === module.path ? 'ring-2 ring-amber-500' : ''
              }`}
              onClick={() => handleModuleClick(module.path)}
            >
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-2xl font-semibold text-amber-100">
                  {module.title}
                </h2>
                <div className={`w-3 h-3 rounded-full ${
                  module.status === 'active' ? 'bg-green-400' :
                  module.status === 'pending' ? 'bg-yellow-400' : 'bg-amber-600'
                }`} />
              </div>
              <p className="text-amber-200/80 text-sm leading-relaxed">
                {module.description}
              </p>
              <div className="mt-4 text-xs text-amber-400/60 font-mono">
                {module.path}
              </div>
            </div>
          ))}
        </div>

        {/* Status Footer */}
        <div className="mt-20 text-center">
          <div className="text-amber-400/50 text-sm">
            {selectedModule ? (
              <span>Module Selected: <code className="text-amber-300">{selectedModule}</code></span>
            ) : (
              <span>Select a covenant-bound module to proceed</span>
            )}
          </div>
        </div>
      </section>
    </main>
  );
}