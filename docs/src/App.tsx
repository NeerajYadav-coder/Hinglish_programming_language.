import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { Footer } from './components/Footer';
import { SearchModal } from './components/SearchModal';
import { HomePage } from './pages/HomePage';
import { GettingStartedPage } from './pages/GettingStartedPage';
import { LanguageGuidePage } from './pages/LanguageGuidePage';
import { CliPage } from './pages/CliPage';
import { MultiFilePage } from './pages/MultiFilePage';
import { PythonCompatPage } from './pages/PythonCompatPage';
import { VsCodePage } from './pages/VsCodePage';
import { DebuggerPage } from './pages/DebuggerPage';
import { FormatterPage } from './pages/FormatterPage';
import { ArchitecturePage } from './pages/ArchitecturePage';
import { PhilosophyPage } from './pages/PhilosophyPage';
import { KeywordReferencePage } from './pages/KeywordReferencePage';
import { ExamplesPage } from './pages/ExamplesPage';

export const App: React.FC = () => {
  // Hash router
  const [route, setRoute] = useState<string>(() => {
    const hash = window.location.hash.replace(/^#/, '');
    return hash || '/';
  });

  // Dark mode
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    const saved = localStorage.getItem('hinglish_theme');
    if (saved) return saved === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  const [searchOpen, setSearchOpen] = useState<boolean>(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState<boolean>(false);

  // Sync route with hash
  useEffect(() => {
    const handleHashChange = () => {
      const h = window.location.hash.replace(/^#/, '') || '/';
      setRoute(h);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const navigate = (newRoute: string) => {
    window.location.hash = newRoute;
    setRoute(newRoute);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Dark mode class toggle
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('hinglish_theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('hinglish_theme', 'light');
    }
  }, [darkMode]);

  const renderPage = () => {
    switch (route) {
      case '/':
        return <HomePage navigate={navigate} />;
      case '/getting-started':
        return <GettingStartedPage />;
      case '/guide':
        return <LanguageGuidePage />;
      case '/cli':
        return <CliPage />;
      case '/multi-file':
        return <MultiFilePage />;
      case '/python-compat':
        return <PythonCompatPage />;
      case '/vscode':
        return <VsCodePage />;
      case '/debugger':
        return <DebuggerPage />;
      case '/formatter':
        return <FormatterPage />;
      case '/architecture':
        return <ArchitecturePage />;
      case '/philosophy':
        return <PhilosophyPage />;
      case '/keywords':
        return <KeywordReferencePage />;
      case '/examples':
        return <ExamplesPage />;
      default:
        return <HomePage navigate={navigate} />;
    }
  };

  return (
    <div className="app-container">
      <Navbar
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        openSearch={() => setSearchOpen(true)}
        mobileMenuOpen={mobileMenuOpen}
        setMobileMenuOpen={setMobileMenuOpen}
        currentRoute={route}
        navigate={navigate}
      />

      <div className="main-layout">
        <Sidebar
          currentRoute={route}
          navigate={navigate}
          mobileMenuOpen={mobileMenuOpen}
          setMobileMenuOpen={setMobileMenuOpen}
        />

        <main className="content-area">
          {renderPage()}
          <Footer currentRoute={route} navigate={navigate} />
        </main>
      </div>

      <SearchModal
        isOpen={searchOpen}
        onClose={() => setSearchOpen(false)}
        navigate={navigate}
      />
    </div>
  );
};
