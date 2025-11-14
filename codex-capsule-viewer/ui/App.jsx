import React, { useState } from 'react';
import CapsuleList from './components/capsule-list';

const App = () => {
  const [currentTheme, setCurrentTheme] = useState('dark-constellation');

  const toggleTheme = () => {
    setCurrentTheme(current => 
      current === 'dark-constellation' ? 'amber-flame' : 'dark-constellation'
    );
  };

  const themeClasses = {
    'dark-constellation': {
      body: 'bg-slate-900 text-amber-100 min-h-screen',
      themeButton: 'fixed top-4 right-4 bg-amber-600 hover:bg-amber-700 text-slate-900 px-4 py-2 rounded-lg font-medium transition-colors z-50'
    },
    'amber-flame': {
      body: 'bg-amber-50 text-slate-900 min-h-screen',
      themeButton: 'fixed top-4 right-4 bg-amber-700 hover:bg-amber-800 text-amber-50 px-4 py-2 rounded-lg font-medium transition-colors z-50'
    }
  };

  const currentThemeClasses = themeClasses[currentTheme];

  return (
    <div className={currentThemeClasses.body}>
      <button
        onClick={toggleTheme}
        className={currentThemeClasses.themeButton}
        title="Toggle theme"
      >
        {currentTheme === 'dark-constellation' ? '🌅' : '🌌'} 
        {currentTheme === 'dark-constellation' ? 'Amber Flame' : 'Dark Constellation'}
      </button>
      
      <CapsuleList theme={currentTheme} />
    </div>
  );
};

export default App;