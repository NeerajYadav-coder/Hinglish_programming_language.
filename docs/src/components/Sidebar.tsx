import React from 'react';
import {
  Home,
  Rocket,
  BookOpen,
  Code,
  Terminal,
  FolderTree,
  FileCode2,
  Cpu,
  Layers,
  Sparkles,
  Bug
} from 'lucide-react';
import { NavSection } from '../types';

interface SidebarProps {
  currentRoute: string;
  navigate: (route: string) => void;
  mobileMenuOpen: boolean;
  setMobileMenuOpen: (val: boolean) => void;
}

export const NAV_SECTIONS: NavSection[] = [
  {
    title: 'Quick Start',
    items: [
      { id: '/', title: 'Home', titleHi: 'Home Page', iconName: 'Home' },
      { id: '/getting-started', title: 'Getting Started', titleHi: 'Shuru Kaise Karein', iconName: 'Rocket' },
      { id: '/examples', title: 'Examples', titleHi: 'Code Examples', iconName: 'Code', badge: '11 Demo' },
    ]
  },
  {
    title: 'Language aur Syntax',
    items: [
      { id: '/guide', title: 'Language Guide', titleHi: 'Language Guide', iconName: 'BookOpen' },
      { id: '/keywords', title: 'Keywords', titleHi: 'Keywords ki List', iconName: 'Sparkles', badge: '30+' },
      { id: '/python-compat', title: 'Python Semantics', titleHi: 'Python ke Sath', iconName: 'Cpu' },
    ]
  },
  {
    title: 'Developer Tools',
    items: [
      { id: '/cli', title: 'CLI Reference', titleHi: 'Terminal Commands (CLI)', iconName: 'Terminal' },
      { id: '/multi-file', title: 'Multi-File Projects', titleHi: 'Multi-File Projects', iconName: 'FolderTree' },
      { id: '/vscode', title: 'VS Code Extension', titleHi: 'VS Code Extension', iconName: 'FileCode2' },
      { id: '/debugger', title: 'Debugger (DAP)', titleHi: 'Debugger & DAP', iconName: 'Bug', badge: 'New' },
    ]
  },
  {
    title: 'Under the Hood',
    items: [
      { id: '/architecture', title: 'Architecture', titleHi: 'Kaise Kaam Karta Hai?', iconName: 'Layers' },
      { id: '/philosophy', title: 'Design Philosophy', titleHi: 'Kyun Banaya? (Story)', iconName: 'BookOpen' },
    ]
  }
];

const renderIcon = (name: string, size = 16) => {
  switch (name) {
    case 'Home': return <Home size={size} />;
    case 'Rocket': return <Rocket size={size} />;
    case 'BookOpen': return <BookOpen size={size} />;
    case 'Code': return <Code size={size} />;
    case 'Terminal': return <Terminal size={size} />;
    case 'FolderTree': return <FolderTree size={size} />;
    case 'FileCode2': return <FileCode2 size={size} />;
    case 'Cpu': return <Cpu size={size} />;
    case 'Layers': return <Layers size={size} />;
    case 'Sparkles': return <Sparkles size={size} />;
    case 'Bug': return <Bug size={size} />;
    default: return <BookOpen size={size} />;
  }
};

export const Sidebar: React.FC<SidebarProps> = ({
  currentRoute,
  navigate,
  mobileMenuOpen,
  setMobileMenuOpen
}) => {
  return (
    <aside
      className={`apple-sidebar ${mobileMenuOpen ? 'mobile-open' : ''}`}
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1.75rem'
      }}
    >
      {NAV_SECTIONS.map((section, idx) => (
        <div key={idx}>
          <div
            style={{
              fontSize: '0.72rem',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              color: 'var(--text-muted)',
              marginBottom: '0.5rem',
              paddingLeft: '0.6rem'
            }}
          >
            {section.title}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
            {section.items.map((item) => {
              const isActive = currentRoute === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    navigate(item.id);
                    setMobileMenuOpen(false);
                  }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.55rem 0.75rem',
                    borderRadius: '8px',
                    border: 'none',
                    background: isActive ? 'var(--accent-soft)' : 'transparent',
                    color: isActive ? 'var(--accent-color)' : 'var(--text-primary)',
                    fontWeight: isActive ? 600 : 400,
                    fontSize: '0.88rem',
                    cursor: 'pointer',
                    textAlign: 'left',
                    transition: 'all 0.15s ease',
                    width: '100%'
                  }}
                  className="sidebar-item-btn"
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
                    <span style={{ color: isActive ? 'var(--accent-color)' : 'var(--text-muted)' }}>
                      {renderIcon(item.iconName)}
                    </span>
                    <span>{item.titleHi}</span>
                  </div>

                  {item.badge && (
                    <span
                      style={{
                        fontSize: '0.65rem',
                        padding: '0.1rem 0.4rem',
                        borderRadius: '9999px',
                        background: isActive ? 'var(--accent-color)' : 'var(--bg-tertiary)',
                        color: isActive ? '#ffffff' : 'var(--text-muted)',
                        fontWeight: 600
                      }}
                    >
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      ))}

      <div style={{ marginTop: 'auto', paddingTop: '1.5rem', borderTop: '1px solid var(--border-color)', paddingLeft: '0.5rem' }}>
        <div
          className="apple-pill"
          style={{
            fontSize: '0.75rem',
            fontWeight: 600,
            background: 'var(--accent-soft)',
            color: 'var(--accent-color)',
            border: '1px solid rgba(0, 113, 227, 0.25)',
            width: 'fit-content'
          }}
        >
          CreatedBYNJ5.0
        </div>
      </div>
    </aside>
  );
};
