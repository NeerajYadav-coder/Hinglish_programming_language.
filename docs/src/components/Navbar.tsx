import React from 'react';
import { Sun, Moon, Search, Github, Menu, X } from 'lucide-react';

interface NavbarProps {
  darkMode: boolean;
  setDarkMode: (val: boolean) => void;
  openSearch: () => void;
  mobileMenuOpen: boolean;
  setMobileMenuOpen: (val: boolean) => void;
  currentRoute: string;
  navigate: (route: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  darkMode,
  setDarkMode,
  openSearch,
  mobileMenuOpen,
  setMobileMenuOpen,
  navigate
}) => {
  return (
    <nav className="apple-navbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          style={{
            display: 'none',
            background: 'none',
            border: 'none',
            color: 'var(--text-primary)',
            cursor: 'pointer',
            padding: '4px'
          }}
          className="mobile-menu-btn"
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>

        <div
          onClick={() => navigate('/')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.65rem',
            cursor: 'pointer',
            userSelect: 'none'
          }}
        >
          <span style={{ fontSize: '1.4rem' }}>🇮🇳</span>
          <span style={{ fontWeight: 700, fontSize: '1.2rem', letterSpacing: '-0.02em', color: 'var(--text-primary)' }}>
            Hinglish
          </span>
          <span className="apple-pill" style={{ fontSize: '0.72rem', padding: '0.15rem 0.55rem' }}>
            v1.0.0
          </span>
          <span
            className="apple-pill"
            style={{
              fontSize: '0.72rem',
              padding: '0.15rem 0.6rem',
              fontWeight: 600,
              background: 'var(--accent-soft)',
              color: 'var(--accent-color)',
              letterSpacing: '0.02em',
              border: '1px solid rgba(0, 113, 227, 0.25)'
            }}
          >
            CreatedBYNJ5.0
          </span>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        {/* Apple Spotlight search trigger */}
        <button
          onClick={openSearch}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            background: 'var(--bg-tertiary)',
            border: '1px solid var(--border-color)',
            borderRadius: '9999px',
            padding: '0.45rem 0.9rem',
            fontSize: '0.85rem',
            color: 'var(--text-secondary)',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
          }}
          title="Search docs (Ctrl+K)"
        >
          <Search size={14} />
          <span>Search karo...</span>
          <kbd
            style={{
              fontSize: '0.7rem',
              padding: '0.1rem 0.35rem',
              borderRadius: '4px',
              background: 'var(--bg-primary)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-muted)'
            }}
          >
            ⌘K
          </kbd>
        </button>

        {/* Theme Toggle */}
        <button
          onClick={() => setDarkMode(!darkMode)}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--text-secondary)',
            cursor: 'pointer',
            padding: '6px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'color 0.2s ease',
          }}
          title={darkMode ? 'Light mode karein' : 'Dark mode karein'}
          aria-label="Theme toggle"
        >
          {darkMode ? <Sun size={19} /> : <Moon size={19} />}
        </button>

        {/* GitHub link from pyproject.toml */}
        <a
          href="https://github.com/NeerajYadav-coder/Hinglish_programming_language."
          target="_blank"
          rel="noopener noreferrer"
          style={{
            color: 'var(--text-secondary)',
            display: 'flex',
            alignItems: 'center',
            padding: '6px',
            transition: 'color 0.2s ease'
          }}
          title="GitHub Repository"
          aria-label="GitHub Repository"
        >
          <Github size={20} />
        </a>
      </div>
    </nav>
  );
};
