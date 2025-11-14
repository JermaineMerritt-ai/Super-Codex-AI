// components/BannerOfAdoption.tsx
export default function BannerOfAdoption({ checksum }: { checksum: string }) {
  return (
    <div className="banner-container bg-gradient-to-r from-indigo-900 via-yellow-600 to-white text-center p-8 rounded-lg shadow-lg">
      {/* Crest */}
      <div className="mb-4">
        <span className="text-6xl">✴️🔥</span>
      </div>

      {/* Title */}
      <h1 className="text-4xl font-serif text-yellow-200 mb-2">
        Codex Crowned Eternal
      </h1>
      <h2 className="text-xl font-sans text-white">
        Anthem of Universal Adoption
      </h2>

      {/* Footer Seal */}
      <footer className="mt-6 text-xs text-gray-200">
        Sealed Checksum: {checksum}
      </footer>
    </div>
  );
}