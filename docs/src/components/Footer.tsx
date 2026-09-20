import React from 'react';
import { ArrowLeft, ArrowRight, Github } from 'lucide-react';
import { NAV_SECTIONS } from './Sidebar';

interface FooterProps {
  currentRoute: string;
  navigate: (route: string) => void;
}

export const Footer: React.FC<FooterProps> = ({ currentRoute, navigate }) => {
  // Flatten items for prev/next
  const allItems = NAV_SECTIONS.flatMap(s => s.items);
  const currentIndex = allItems.findIndex(i => i.id === currentRoute);
  const prevItem = currentIndex > 0 ? allItems[currentIndex - 1] : null;
  const nextItem = currentIndex >= 0 && currentIndex < allItems.length - 1 ? allItems[currentIndex + 1] : null;

  return (
    <footer style={{ marginTop: '5rem', borderTop: '1px solid var(--border-color)', paddingTop: '2.5rem' }}>
      {/* Prev / Next Pagination */}
      {(prevItem || nextItem) && (
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '1rem', marginBottom: '3rem', flexWrap: 'wrap' }}>
          {prevItem ? (
            <button
              onClick={() => navigate(prevItem.id)}
              className="apple-card"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                cursor: 'pointer',
                border: '1px solid var(--border-color)',
                padding: '1rem 1.4rem',
                textAlign: 'left',
                flex: 1,
                minWidth: '220px',
                background: 'var(--bg-card)'
              }}
            >
              <ArrowLeft size={18} style={{ color: 'var(--accent-color)' }} />
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Pichhla Adhyay</div>
                <div style={{ fontWeight: 600, fontSize: '0.95rem', color: 'var(--text-primary)' }}>{prevItem.titleHi}</div>
              </div>
            </button>
          ) : <div style={{ flex: 1 }} />}

          {nextItem ? (
            <button
              onClick={() => navigate(nextItem.id)}
              className="apple-card"
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                gap: '0.75rem',
                cursor: 'pointer',
                border: '1px solid var(--border-color)',
                padding: '1rem 1.4rem',
                textAlign: 'right',
                flex: 1,
                minWidth: '220px',
                background: 'var(--bg-card)'
              }}
            >
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Agla Adhyay</div>
                <div style={{ fontWeight: 600, fontSize: '0.95rem', color: 'var(--text-primary)' }}>{nextItem.titleHi}</div>
              </div>
              <ArrowRight size={18} style={{ color: 'var(--accent-color)' }} />
            </button>
          ) : <div style={{ flex: 1 }} />}
        </div>
      )}

      {/* Apple Minimalist Footer Credits */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem',
          fontSize: '0.82rem',
          color: 'var(--text-muted)'
        }}
      >
        <div>
          <span>© 2026 Hinglish Language Project • <strong style={{ color: 'var(--text-primary)' }}>CreatedBYNJ5.0</strong> • MIT License</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
          <span>Version 1.1.0</span>
          <span>•</span>
          <span>Target: Python 3.10+</span>
          <span>•</span>
          <a
            href="https://github.com/NeerajYadav-coder/Hinglish_programming_language."
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: 'var(--text-secondary)', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}
          >
            <Github size={14} />
            <span>GitHub Repository</span>
          </a>
        </div>
      </div>
    </footer>
  );
};
