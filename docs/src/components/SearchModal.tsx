import React, { useState, useEffect, useRef } from 'react';
import { Search, X, ArrowRight, Sparkles, BookOpen, Code } from 'lucide-react';
import { KEYWORDS_DATA } from '../data/keywords';
import { EXAMPLES_DATA } from '../data/examples';
import { NAV_SECTIONS } from './Sidebar';

interface SearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  navigate: (route: string) => void;
}

interface SearchResult {
  type: 'keyword' | 'page' | 'example';
  title: string;
  subtitle: string;
  route: string;
}

export const SearchModal: React.FC<SearchModalProps> = ({
  isOpen,
  onClose,
  navigate
}) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const resultsContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setSelectedIndex(0);
    } else {
      setQuery('');
      setResults([]);
      setSelectedIndex(0);
    }
  }, [isOpen]);

  // Keyboard shortcut listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Filter results
  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setSelectedIndex(0);
      return;
    }

    const q = query.toLowerCase();
    const res: SearchResult[] = [];

    // Search keywords
    for (const kw of KEYWORDS_DATA) {
      if (
        kw.token.toLowerCase().includes(q) ||
        kw.python.toLowerCase().includes(q) ||
        kw.meaning.toLowerCase().includes(q) ||
        kw.aliases?.some(a => a.toLowerCase().includes(q))
      ) {
        res.push({
          type: 'keyword',
          title: `${kw.token} → ${kw.python}`,
          subtitle: kw.meaning,
          route: '/keywords'
        });
        if (res.length >= 8) break;
      }
    }

    // Search pages
    for (const section of NAV_SECTIONS) {
      for (const item of section.items) {
        if (
          item.title.toLowerCase().includes(q) ||
          item.titleHi.toLowerCase().includes(q)
        ) {
          res.push({
            type: 'page',
            title: `${item.titleHi} (${item.title})`,
            subtitle: section.title,
            route: item.id
          });
          if (res.length >= 12) break;
        }
      }
    }

    // Search examples
    for (const ex of EXAMPLES_DATA) {
      if (
        ex.title.toLowerCase().includes(q) ||
        ex.description.toLowerCase().includes(q) ||
        ex.keyConcepts.some(c => c.toLowerCase().includes(q))
      ) {
        res.push({
          type: 'example',
          title: ex.title,
          subtitle: ex.description,
          route: '/examples'
        });
        if (res.length >= 15) break;
      }
    }

    setResults(res);
    setSelectedIndex(0);
  }, [query]);

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (results.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % results.length);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + results.length) % results.length);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      const target = results[selectedIndex] || results[0];
      if (target) {
        navigate(target.route);
        onClose();
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div className="spotlight-overlay" onClick={onClose}>
      <div className="spotlight-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="spotlight-input-wrapper">
          <Search size={18} style={{ color: 'var(--text-muted)' }} />
          <input
            ref={inputRef}
            type="text"
            className="spotlight-input"
            placeholder="Search keywords, topics, guides, CLI (e.g. agar, varg, lambai, format)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleInputKeyDown}
          />
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: 'var(--text-muted)'
            }}
            aria-label="Close search"
          >
            <X size={18} />
          </button>
        </div>

        <div className="spotlight-results" ref={resultsContainerRef}>
          {query.trim() && results.length === 0 && (
            <div style={{ padding: '2rem 1rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              Koi result nahi mila "{query}" ke liye. Kuch aur try karein!
            </div>
          )}

          {!query.trim() && (
            <div style={{ padding: '1.5rem 1rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              <div style={{ fontWeight: 600, marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
                Popular Searches:
              </div>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {['agar', 'kaam', 'varg', 'dikhao', 'lambai', 'ginti', 'milao', 'laao', 'format'].map((k) => (
                  <button
                    key={k}
                    onClick={() => setQuery(k)}
                    className="apple-pill"
                    style={{ cursor: 'pointer', border: '1px solid var(--border-color)', background: 'var(--bg-tertiary)' }}
                  >
                    {k}
                  </button>
                ))}
              </div>
            </div>
          )}

          {results.map((r, i) => (
            <div
              key={i}
              className={`spotlight-item ${selectedIndex === i ? 'active' : ''}`}
              onMouseEnter={() => setSelectedIndex(i)}
              onClick={() => {
                navigate(r.route);
                onClose();
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ color: selectedIndex === i ? 'var(--accent-color)' : 'var(--text-muted)' }}>
                  {r.type === 'keyword' && <Sparkles size={16} />}
                  {r.type === 'page' && <BookOpen size={16} />}
                  {r.type === 'example' && <Code size={16} />}
                </span>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.92rem' }}>{r.title}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', maxWidth: '420px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {r.subtitle}
                  </div>
                </div>
              </div>

              <ArrowRight size={14} style={{ color: selectedIndex === i ? 'var(--accent-color)' : 'var(--text-muted)' }} />
            </div>
          ))}
        </div>

        {/* Apple Spotlight Footer */}
        <div
          style={{
            padding: '0.65rem 1.25rem',
            borderTop: '1px solid var(--border-color)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            fontSize: '0.75rem',
            color: 'var(--text-muted)',
            background: 'var(--bg-secondary)'
          }}
        >
          <div style={{ display: 'flex', gap: '0.85rem', alignItems: 'center' }}>
            <span><kbd style={{ padding: '0.1rem 0.35rem', background: 'var(--bg-tertiary)', borderRadius: '4px', border: '1px solid var(--border-color)', fontSize: '0.72rem' }}>↑</kbd> <kbd style={{ padding: '0.1rem 0.35rem', background: 'var(--bg-tertiary)', borderRadius: '4px', border: '1px solid var(--border-color)', fontSize: '0.72rem' }}>↓</kbd> navigate</span>
            <span><kbd style={{ padding: '0.1rem 0.35rem', background: 'var(--bg-tertiary)', borderRadius: '4px', border: '1px solid var(--border-color)', fontSize: '0.72rem' }}>↵</kbd> select</span>
            <span><kbd style={{ padding: '0.1rem 0.35rem', background: 'var(--bg-tertiary)', borderRadius: '4px', border: '1px solid var(--border-color)', fontSize: '0.72rem' }}>esc</kbd> close</span>
          </div>
          <span>Hinglish v1.1.0 Spotlight</span>
        </div>
      </div>
    </div>
  );
};
