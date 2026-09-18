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
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
      setResults([]);
    }
  }, [isOpen]);

  // Keyboard shortcut listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else {
          // Open triggered by parent
        }
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
  }, [query]);

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
            placeholder="Keyword, topic, ya udaharan khojein (jaise: agar, varg, run, loop)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: 'var(--text-muted)'
            }}
          >
            <X size={18} />
          </button>
        </div>

        <div className="spotlight-results">
          {query.trim() && results.length === 0 && (
            <div style={{ padding: '2rem 1rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
              Koi parinam nahi mila "{query}" ke liye.
            </div>
          )}

          {!query.trim() && (
            <div style={{ padding: '1.5rem 1rem', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              <div style={{ fontWeight: 600, marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
                Lokpriya Khoj Suggestions:
              </div>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {['agar', 'kaam', 'varg', 'dikhao', 'asamanantar', 'milao', 'laao'].map((k) => (
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
              className="spotlight-item"
              onClick={() => {
                navigate(r.route);
                onClose();
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ color: 'var(--accent-color)' }}>
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

              <ArrowRight size={14} style={{ color: 'var(--text-muted)' }} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
