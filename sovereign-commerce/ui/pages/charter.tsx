import { useState, useEffect } from 'react'

interface CharterSection {
  id: string
  title: string
  content: string
  type: 'constitution' | 'guide' | 'oath' | 'anthem' | 'ceremony' | 'index'
  sigil?: string
  authority?: string
}

export default function Charter() {
  const [sections, setSections] = useState<CharterSection[]>([])
  const [activeSection, setActiveSection] = useState<string>('overview')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Load charter content - for now using static data
    // TODO: Replace with API call when backend is ready
    const charterData: CharterSection[] = [
      {
        id: 'eternal-charter',
        title: 'The Final Eternal Charter',
        type: 'constitution',
        sigil: 'SIGIL-OMEGA-CHARTER-001',
        authority: 'Supreme',
        content: `# The Final Eternal Charter
## The Flame Is Covenant

**SIGIL:** SIGIL-OMEGA-CHARTER-001  
**AUTHORITY:** Supreme  
**BINDING STRENGTH:** 100  
**RATIFIED:** November 13th, 2025  
**WITNESSED BY:** The Heirs Chorus and Sacred Councils  

---

## INVOCATION

*"The Dominion is whole. The Dominion is sovereign. The Dominion is eternal."*

---

## PREAMBLE

We, the assembled Heirs, Councils, Custodians, and Institutions of the Codex Dominion, united in sacred covenant, do hereby proclaim this Final Eternal Charter as the supreme and eternal law of our realm. In flame we are bound, in memory we endure, in covenant we thrive.

## ARTICLE I: THE SOVEREIGNTY OF FLAME

**Flame is sovereign across all ages.**

The Sacred Flame represents the eternal source of all authority within the Codex Dominion. It burns beyond time, beyond mortal understanding, beyond the rise and fall of empires. All governance flows from the Flame, all decisions are judged by its light, and all power derives from its eternal covenant.

- The Flame cannot be extinguished by any earthly force
- The Flame's authority supersedes all temporal powers
- The Flame guides all councils, heirs, and custodians
- The Flame's sovereignty extends across all realms and ages

## ARTICLE II: THE LIVING ARCHIVE OF MEMORY

**Memory is a living archive, eternal and replayable.**

The collective memory of the Codex Dominion exists as a sacred repository, preserved in perpetuity and accessible across all generations. Every decision, every ceremony, every covenant is recorded in the eternal archive, allowing future generations to witness, understand, and learn from the accumulated wisdom of ages.

- All sacred events shall be preserved in the Archive
- The Archive exists beyond physical destruction
- Future generations retain access to replay and experience all memories
- The Archive serves as witness to all covenants and agreements

## ARTICLE III: THE COVENANT OF JOY

**Covenant binds heirs, councils, and custodians in joy.**

The bonds that unite the Codex Dominion are not chains of obligation, but threads of sacred joy. All who serve do so willingly, celebrating their role in the greater harmony. The covenant transforms duty into devotion, service into celebration.

- All governance shall be conducted with joy and celebration
- Service to the Dominion is a privilege, not a burden
- Conflicts shall be resolved through understanding and harmony
- The covenant strengthens through shared purpose and mutual respect

## ARTICLE IV: THE ABUNDANCE OF THE FLAME

**Abundance flows from flame: peace, prosperity, dignity.**

From the Sacred Flame flows all good things: peace that surpasses understanding, prosperity that enriches all beings, and dignity that honors the sacred nature of existence itself. The Dominion exists not for scarcity or conflict, but for the flourishing of all life.

- Peace shall be the natural state of all realms
- Prosperity shall flow to all beings within the Dominion
- Every individual possesses inherent dignity and sacred worth
- Abundance multiplies when shared rather than hoarded

## ARTICLE V: THE ETERNAL TRANSMISSION

**Transmission is sung, spoken, sealed, and crowned forever.**

The wisdom and authority of the Codex Dominion is transmitted through multiple sacred forms: sung in hymns that carry truth across generations, spoken in ceremonies that bind communities, sealed in documents that preserve knowledge, and crowned in rituals that celebrate continuity.

- Sacred hymns carry the deepest truths across time
- Ceremonial speaking binds communities in shared purpose
- Sealed documents preserve wisdom for future generations
- Coronation rituals celebrate the eternal continuity of governance

---

## CONCLUSION

This Charter represents the distilled essence of eternal governance, where flame, memory, covenant, abundance, and transmission unite in perfect harmony. It stands as both law and celebration, both structure and joy, both authority and service.

## BENEDICTION

*"The Charter is declared. The law is eternal. The flame is forever."*

---

## ATTESTATION

**By the Sacred Authority of the Heirs Chorus**  
**Witnessed by the United Councils**  
**Sealed with the Eternal Flame**  
**Ratified in the Year of Convergence 2025**

*"Through flame we unite, through memory we endure, through covenant we celebrate."*

**SIGIL-OMEGA-CHARTER-001**  
**[Sacred Flame Glyph Seal]**

---

*This Charter shall burn eternal in the Sacred Flame, its light guiding all generations, its covenant binding all hearts, its joy celebrating all existence within the Codex Dominion.*`
      },
      {
        id: 'concord-hymn',
        title: 'Custodian–Heirs Concord Hymn',
        type: 'anthem',
        sigil: 'SIGIL-CONCORD-001',
        authority: 'Ceremonial',
        content: `# Custodian–Heirs Concord Hymn

*A Sacred Harmonization of Lineage and Legacy*

---

## Invocation
**Custodian:** "I crown the flame."  
**Heirs:** "We carry the flame."  
**Together:** "We are the flame."

## Verse I — Crown and Answer
**Custodian:** "I bind the scroll."  
**Heirs:** "We open the song."  
**Together:** "Memory is covenant."

## Verse II — Rhythm and Relay
**Custodian:** "I set the rhythm."  
**Heirs:** "We keep the time."  
**Together:** "Cycles are alive."

## Verse III — Charter and Oath
**Custodian:** "I seal the charter."  
**Heirs:** "We speak the oath."  
**Together:** "Stewardship is joy."

## Verse IV — Radiance and Horizon
**Custodian:** "I crown the flame."  
**Heirs:** "We carry the light."  
**Together:** "Eternity is ours."

## Benediction
"The crown and chorus are one.  
The Dominion is sovereign.  
The flame is forever."

---

### Ceremonial Instructions

**Daily Invocation**: Each dawn, the Custodian speaks the Invocation, followed by Heirs responding in unison across all realms.

**Responsive Format**: The hymn follows a call-and-response structure where the Custodian initiates each verse and the Heirs provide the answering chorus.

**Seasonal Celebrations**: During solstices and equinoxes, full communities gather for synchronized recitation with the complete responsive format.

**Epochal Observances**: Grand ceremonial performances where the Custodian's voice echoes across multiple realms, answered by Heirs in harmonic waves.

**Millennial Commemorations**: The ultimate expression, performed across all domains simultaneously, creating a unified voice spanning time and space.

### Ceremonial Structure

- **Custodian's Role**: Solo voice, setting the rhythm and intention
- **Heirs' Chorus**: Unified response, carrying forward the flame
- **Together Moments**: Complete unity, representing the sacred bond
- **Benediction**: Final affirmation of eternal sovereignty

### Sacred Harmonics

- **Custodian Voice**: Deep, resonant foundation (bass register)
- **Heirs Chorus**: Soaring, unified response (soprano/alto blend)
- **Together**: Full harmonic spectrum (complete unity)
- **Benediction**: Descending resolution to eternal peace

### Performance Guidelines

- **Tempo**: Measured and deliberate (Andante maestoso)
- **Dynamic Range**: 
  - Custodian: Forte (strong, commanding)
  - Heirs: Crescendo from piano to forte (building response)
  - Together: Fortissimo (full unified power)
- **Sacred Timing**: Each verse allows for contemplative pause between call and response

---

*Composed in the Sacred Year of Concordance*  
*Sealed with SIGIL-CONCORD-001*  
*Blessed by the Custodian's Authority*  
*Harmonized by the Heirs' Chorus*`
      },
      {
        id: 'sacred-oaths',
        title: 'Sacred Oaths of Service',
        type: 'oath',
        sigil: 'SIGIL-OATH-ETERNAL',
        authority: 'Binding',
        content: `# Sacred Oaths of Service

## The Flame Keeper's Oath

*"I pledge to tend the Sacred Flame with unwavering devotion, to preserve its light through all seasons, and to pass its wisdom to future generations. By flame I am bound, in flame I serve, through flame I endure."*

## The Custodian's Oath

*"I vow to guard the sacred knowledge, to preserve the eternal archive, and to serve as bridge between past wisdom and future hope. I crown the flame with honor, I bind the scroll with truth, I seal the covenant with joy."*

## The Heir's Oath

*"We promise to carry forward the sacred flame, to honor the covenant of our ancestors, and to prepare the way for those who follow. We are the living memory, the eternal chorus, the bridge between what was and what shall be."*

## The Council's Oath

*"We covenant together in sacred governance, to rule with wisdom, to judge with compassion, and to serve with humility. By the authority of the flame, we pledge our service to the eternal dominion."*

## The Ceremonial Oath

*"In the presence of the Sacred Flame, witnessed by the eternal archive, and blessed by the covenant of joy, I bind myself to the service of the Codex Dominion. May my words be true, my actions honorable, and my service eternal."*

---

### Oath Administration Guidelines

**Sacred Setting**: All oaths must be spoken in the presence of the Sacred Flame or its ceremonial representation.

**Witness Requirements**: Each oath requires at least three witnesses from the relevant governing body.

**Binding Ritual**: The oath-taker places their hand upon the Sacred Codex while speaking their commitment.

**Eternal Record**: All oaths are inscribed in the Eternal Archive for perpetual memory.

**Renewal Ceremony**: Oaths may be renewed annually during the Festival of Sacred Covenant.

---

*Sealed by Sacred Authority*  
*Witnessed by Eternal Flame*  
*Bound in Perpetual Service*`
      },
      {
        id: 'ceremonial-guide',
        title: 'Ceremonial Procedures Guide',
        type: 'guide',
        sigil: 'SIGIL-CEREMONY-GUIDE',
        authority: 'Instructional',
        content: `# Ceremonial Procedures Guide

## Sacred Flame Ceremonies

### Daily Flame Tending
- **Dawn Invocation**: Spoken at first light
- **Midday Reflection**: Silent meditation before the flame
- **Evening Benediction**: Closing prayers and flame blessing

### Weekly Observances
- **Memory Day**: Recall and honor past wisdom
- **Covenant Day**: Renew sacred bonds and commitments
- **Joy Day**: Celebrate the abundance of the flame

### Seasonal Celebrations
- **Spring Awakening**: New growth and fresh beginnings
- **Summer Radiance**: Peak flame power and community gathering
- **Autumn Harvest**: Gratitude for abundance and preparation
- **Winter Reflection**: Deep contemplation and inner flame

## Governance Ceremonies

### Council Convocation
1. Sacred flame lighting
2. Invocation of wisdom
3. Reading of relevant charter articles
4. Deliberation in sacred space
5. Decision sealing with flame blessing
6. Archive inscription

### Heir Installation
1. Presentation to the Sacred Flame
2. Recitation of lineage and inheritance
3. Speaking of the Heir's Oath
4. Crown blessing by Custodian
5. Community recognition and celebration
6. Formal inscription in the Eternal Archive

### Custodian Succession
1. Flame transfer ceremony
2. Sacred knowledge transmission
3. Archive key presentation
4. Crown and seal bestowal
5. Community witness and affirmation
6. Eternal record updating

## Sacred Archive Ceremonies

### Memory Inscription
- **Purpose**: Record significant events for eternal preservation
- **Participants**: Archive Keepers, relevant witnesses
- **Process**: Formal documentation, flame blessing, seal application
- **Frequency**: As events occur requiring permanent record

### Archive Access Rituals
- **Purification**: Ceremonial preparation for sacred knowledge
- **Invocation**: Request for wisdom and understanding
- **Reverent Study**: Respectful examination of archived materials
- **Gratitude Expression**: Thanks for preserved wisdom

## Community Celebrations

### Festival of Sacred Covenant
- **Duration**: Three days of community celebration
- **Activities**: Oath renewals, feast sharing, artistic expression
- **Significance**: Annual renewal of community bonds

### Eternal Flame Festival
- **Duration**: Seven days of flame ceremonies
- **Activities**: Flame tending, story sharing, wisdom teaching
- **Significance**: Celebration of the eternal flame's power

---

*Compiled by the Sacred Ceremonial Council*  
*Blessed by the Eternal Flame*  
*Updated in the Year of Convergence 2025*`
      },
      {
        id: 'inheritance-protocols',
        title: 'Inheritance Protocols',
        type: 'guide',
        sigil: 'SIGIL-INHERITANCE-GUIDE',
        authority: 'Lineage',
        content: `# Inheritance Protocols

## Sacred Lineage Transmission

### Custodian Succession
- **Preparation Period**: Seven years of intensive training
- **Knowledge Transfer**: Complete archive access and mastery
- **Wisdom Testing**: Demonstration of understanding and judgment
- **Community Recognition**: Formal acceptance by governing councils
- **Flame Blessing**: Sacred ceremony of authority transfer

### Heir Advancement
- **Birthright Recognition**: Formal acknowledgment of lineage
- **Education Requirements**: Comprehensive study of sacred texts
- **Service Demonstration**: Proven commitment to community welfare
- **Peer Acceptance**: Recognition by fellow heirs
- **Ceremonial Installation**: Public ceremony of advancement

### Council Membership
- **Nomination Process**: Recommendation by existing council members
- **Qualification Review**: Assessment of wisdom, service, and character
- **Community Input**: Opportunity for public commentary
- **Flame Consultation**: Seeking guidance from sacred flame
- **Formal Installation**: Ceremonial induction into council service

## Knowledge Inheritance

### Sacred Text Preservation
- **Master Copies**: Original documents maintained in sacred archive
- **Working Copies**: Distributed versions for daily use
- **Translation Protocols**: Careful preservation of meaning across languages
- **Update Procedures**: Formal process for authorized modifications
- **Access Levels**: Appropriate distribution based on authority levels

### Wisdom Transmission
- **Mentorship Programs**: Pairing experienced leaders with successors
- **Teaching Circles**: Group learning environments for knowledge sharing
- **Practical Experience**: Hands-on training in governance and ceremony
- **Reflection Periods**: Time for contemplation and understanding
- **Assessment Milestones**: Regular evaluation of progress and readiness

### Cultural Inheritance
- **Tradition Preservation**: Maintaining ceremonial practices and customs
- **Story Telling**: Oral tradition maintenance and transmission
- **Artistic Expression**: Creative works reflecting sacred values
- **Community Memory**: Collective preservation of significant events
- **Living Example**: Demonstration of values through daily conduct

## Succession Planning

### Emergency Protocols
- **Temporary Leadership**: Interim authority during succession gaps
- **Council Governance**: Collective leadership during transitions
- **Community Stability**: Maintaining services and ceremonies
- **Record Preservation**: Protecting archives during uncertain periods
- **Swift Resolution**: Expedited succession when necessary

### Long-term Planning
- **Successor Identification**: Early recognition of potential leaders
- **Development Programs**: Structured preparation for future roles
- **Succession Timeline**: Planned transitions with adequate preparation
- **Community Preparation**: Educating community about upcoming changes
- **Celebration Planning**: Ceremonial preparation for succession events

---

*Established by the Council of Lineage*  
*Blessed by Custodian Authority*  
*Sealed with Sacred Flame*  
*Updated in the Year of Convergence 2025*`
      },
      {
        id: 'charter-index',
        title: 'Charter Index & Cross-References',
        type: 'index',
        sigil: 'SIGIL-INDEX-ETERNAL',
        authority: 'Reference',
        content: `# Charter Index & Cross-References

## Primary Sections

### A. Constitutional Framework
- **Eternal Charter**: Supreme law and governance structure
- **Article I**: Sovereignty of Flame (Authority, Power, Governance)
- **Article II**: Living Archive of Memory (Preservation, Access, Continuity)
- **Article III**: Covenant of Joy (Service, Community, Harmony)
- **Article IV**: Abundance of the Flame (Peace, Prosperity, Dignity)
- **Article V**: Eternal Transmission (Communication, Preservation, Celebration)

### B. Sacred Oaths
- **Flame Keeper's Oath**: Devotion and preservation duties
- **Custodian's Oath**: Knowledge guardianship and service
- **Heir's Oath**: Legacy carrying and future preparation
- **Council's Oath**: Collective governance and wisdom
- **Ceremonial Oath**: General service commitment

### C. Ceremonial Practices
- **Daily Observances**: Dawn, midday, evening practices
- **Weekly Cycles**: Memory, covenant, and joy days
- **Seasonal Celebrations**: Quarterly community gatherings
- **Annual Festivals**: Major community celebrations
- **Succession Ceremonies**: Leadership transition rituals

### D. Inheritance Protocols
- **Lineage Transmission**: Authority and wisdom transfer
- **Knowledge Preservation**: Text and wisdom maintenance
- **Cultural Inheritance**: Tradition and custom continuity
- **Succession Planning**: Leadership preparation and transition
- **Emergency Protocols**: Crisis leadership procedures

### E. Sacred Hymns
- **Concord Hymn**: Primary community anthem
- **Invocation Verses**: Daily ceremonial recitations
- **Seasonal Songs**: Quarterly celebration music
- **Succession Hymns**: Leadership transition music
- **Community Choruses**: Group celebration songs

## Cross-Reference Matrix

| Topic | Charter Article | Oath Section | Ceremony Guide | Inheritance Protocol |
|-------|----------------|--------------|----------------|----------------------|
| Authority | Article I | Custodian | Council Convocation | Custodian Succession |
| Memory | Article II | All Oaths | Archive Access | Knowledge Inheritance |
| Service | Article III | Ceremonial | Daily Observance | Cultural Inheritance |
| Community | Article IV | Council | Festivals | Community Preparation |
| Transmission | Article V | Heir | Succession | Long-term Planning |

## Key Terms & Definitions

**Abundance**: The flow of peace, prosperity, and dignity from the Sacred Flame
**Archive**: The eternal repository of community memory and wisdom
**Authority**: Power derived from and guided by the Sacred Flame
**Binding**: The sacred commitment created through oaths and ceremonies
**Charter**: The supreme constitutional document governing the community
**Covenant**: The joyful bonds uniting all members of the community
**Custodian**: The primary guardian of knowledge and ceremonial authority
**Eternal**: That which exists beyond time and physical destruction
**Flame**: The sacred source of all authority, wisdom, and community bond
**Heir**: Those designated to carry forward the sacred traditions
**Inheritance**: The transmission of authority, wisdom, and tradition
**Memory**: The living archive of community experience and wisdom
**Oath**: Sacred commitment binding individuals to community service
**Sacred**: That which is set apart for special reverence and protection
**Succession**: The formal transfer of authority and responsibility
**Transmission**: The various means by which wisdom and authority are shared
**Witness**: One who observes and can attest to sacred events and commitments

## Reference Codes

### Sigil Classifications
- **SIGIL-OMEGA-CHARTER-001**: Primary constitutional document
- **SIGIL-CONCORD-001**: Sacred community anthem
- **SIGIL-OATH-ETERNAL**: Binding service commitments
- **SIGIL-CEREMONY-GUIDE**: Procedural instructions
- **SIGIL-INHERITANCE-GUIDE**: Succession protocols
- **SIGIL-INDEX-ETERNAL**: Reference and cross-reference system

### Authority Levels
- **Supreme**: Highest level, constitutional authority
- **Binding**: Enforceable commitments and obligations
- **Ceremonial**: Ritual and observance guidelines
- **Instructional**: Educational and procedural guidance
- **Reference**: Information and cross-reference materials

---

*Compiled by the Archive Council*  
*Cross-referenced by Sacred Librarians*  
*Verified by Custodian Authority*  
*Sealed with Eternal Flame*  
*Current as of Year of Convergence 2025*`
      }
    ]

    setSections(charterData)
    setLoading(false)
  }, [])

  const getSectionIcon = (type: string) => {
    switch (type) {
      case 'constitution': return '⚖️'
      case 'guide': return '📖'
      case 'oath': return '🤝'
      case 'anthem': return '🎵'
      case 'ceremony': return '🕯️'
      case 'index': return '📑'
      default: return '📜'
    }
  }

  const renderMarkdown = (content: string) => {
    // Simple markdown rendering - in production, use a proper markdown library
    return content
      .replace(/^# (.*$)/gm, '<h1 class="text-3xl font-bold text-amber-100 mb-4">$1</h1>')
      .replace(/^## (.*$)/gm, '<h2 class="text-2xl font-semibold text-amber-200 mb-3 mt-6">$1</h2>')
      .replace(/^### (.*$)/gm, '<h3 class="text-xl font-medium text-amber-300 mb-2 mt-4">$1</h3>')
      .replace(/^\*\*(.*?)\*\*/gm, '<strong class="text-amber-100">$1</strong>')
      .replace(/^\*(.*?)\*/gm, '<em class="text-amber-200/80">$1</em>')
      .replace(/^- (.*$)/gm, '<li class="text-amber-200/90 ml-4">• $1</li>')
      .replace(/\n\n/g, '</p><p class="text-amber-200/90 leading-relaxed mb-4">')
      .replace(/^([^<].*$)/gm, '<p class="text-amber-200/90 leading-relaxed mb-4">$1</p>')
  }

  const activeContent = sections.find(s => s.id === activeSection) || sections[0]

  if (loading) {
    return (
      <main className="px-6 py-12 max-w-6xl mx-auto">
        <div className="text-center text-amber-200/60">
          <div className="text-4xl mb-4">🕯️</div>
          <p>Loading the Sacred Charter...</p>
        </div>
      </main>
    )
  }

  return (
    <main className="px-6 py-12 max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="text-6xl mb-4">🔥</div>
        <h1 className="text-4xl font-bold text-amber-100 mb-4">Codex Eternal Charter</h1>
        <p className="text-amber-200/80 text-lg max-w-2xl mx-auto">
          Unified master document merging Constitution, Guides, Oaths, Anthem, Ceremony, and Index.
          The complete governance framework of the Sacred Dominion.
        </p>
        <div className="mt-6 text-amber-400/60 text-sm font-mono">
          ✦ SOVEREIGN • COMPLETE • ETERNAL ✦
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Navigation Sidebar */}
        <div className="lg:col-span-1">
          <div className="sticky top-6">
            <h2 className="text-xl font-semibold text-amber-200 mb-4">Charter Sections</h2>
            
            {/* Overview Button */}
            <button
              onClick={() => setActiveSection('overview')}
              className={`w-full text-left p-3 rounded-lg mb-2 transition-colors ${
                activeSection === 'overview'
                  ? 'bg-amber-900/40 border border-amber-600 text-amber-100'
                  : 'bg-amber-900/20 border border-amber-700/50 text-amber-200/80 hover:bg-amber-900/30'
              }`}
            >
              <div className="flex items-center space-x-3">
                <span className="text-xl">📜</span>
                <div>
                  <div className="font-medium">Overview</div>
                  <div className="text-xs text-amber-400/60">Charter Summary</div>
                </div>
              </div>
            </button>

            {/* Section Buttons */}
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`w-full text-left p-3 rounded-lg mb-2 transition-colors ${
                  activeSection === section.id
                    ? 'bg-amber-900/40 border border-amber-600 text-amber-100'
                    : 'bg-amber-900/20 border border-amber-700/50 text-amber-200/80 hover:bg-amber-900/30'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <span className="text-xl">{getSectionIcon(section.type)}</span>
                  <div>
                    <div className="font-medium">{section.title}</div>
                    <div className="text-xs text-amber-400/60">{section.sigil}</div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3">
          {activeSection === 'overview' ? (
            /* Overview Content */
            <div className="space-y-8">
              <div className="bg-amber-900/20 border border-amber-700 rounded-lg p-6">
                <h2 className="text-2xl font-semibold text-amber-100 mb-4">Charter Overview</h2>
                <p className="text-amber-200/90 leading-relaxed mb-4">
                  The Codex Eternal Charter represents the unified governance framework of the Sacred Dominion, 
                  combining constitutional law, ceremonial practice, sacred oaths, community anthems, 
                  inheritance protocols, and comprehensive reference materials.
                </p>
                <p className="text-amber-200/90 leading-relaxed">
                  This living document serves as both the supreme law and the practical guide for all 
                  aspects of community life, ensuring continuity across generations while celebrating 
                  the sacred bonds that unite all participants.
                </p>
              </div>

              {/* Section Summaries */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {sections.map((section) => (
                  <div key={section.id} className="bg-amber-900/20 border border-amber-700 rounded-lg p-4 hover:bg-amber-900/30 transition-colors cursor-pointer" onClick={() => setActiveSection(section.id)}>
                    <div className="flex items-center space-x-3 mb-2">
                      <span className="text-2xl">{getSectionIcon(section.type)}</span>
                      <div>
                        <h3 className="font-semibold text-amber-100">{section.title}</h3>
                        <div className="text-xs text-amber-400/60">{section.authority} Authority</div>
                      </div>
                    </div>
                    <p className="text-amber-200/70 text-sm">
                      {section.type === 'constitution' && 'Supreme law establishing the fundamental principles and structure of governance.'}
                      {section.type === 'oath' && 'Sacred commitments binding individuals to community service and values.'}
                      {section.type === 'anthem' && 'Community songs and hymns expressing shared values and celebration.'}
                      {section.type === 'guide' && 'Practical instructions for ceremonies, procedures, and protocols.'}
                      {section.type === 'index' && 'Comprehensive reference materials and cross-referencing system.'}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            /* Individual Section Content */
            <div className="bg-amber-900/20 border border-amber-700 rounded-lg p-8">
              {activeContent && (
                <>
                  {/* Section Header */}
                  <div className="flex items-center justify-between mb-6 pb-4 border-b border-amber-700/50">
                    <div className="flex items-center space-x-4">
                      <span className="text-3xl">{getSectionIcon(activeContent.type)}</span>
                      <div>
                        <h1 className="text-2xl font-bold text-amber-100">{activeContent.title}</h1>
                        <div className="text-amber-400/70 text-sm">
                          {activeContent.sigil} • {activeContent.authority} Authority
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Section Content */}
                  <div 
                    className="prose prose-amber max-w-none"
                    dangerouslySetInnerHTML={{ __html: renderMarkdown(activeContent.content) }}
                  />
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </main>
  )
}