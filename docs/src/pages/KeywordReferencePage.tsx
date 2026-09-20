import React, { useState, useMemo } from 'react';
import { KEYWORDS_DATA } from '../data/keywords';
import { Search, Copy, Check } from 'lucide-react';

export const KeywordReferencePage: React.FC = () => {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [copiedToken, setCopiedToken] = useState<string | null>(null);

  const categories = ['All', 'Statements', 'Operators', 'Literals', 'Builtins', 'Soft Keywords', 'Aliases'];

  const filteredKeywords = useMemo(() => {
    return KEYWORDS_DATA.filter((kw) => {
      const matchesCat = selectedCategory === 'All' || kw.category === selectedCategory;
      const q = search.toLowerCase().trim();
      const matchesSearch =
        !q ||
        kw.token.toLowerCase().includes(q) ||
        kw.python.toLowerCase().includes(q) ||
        kw.meaning.toLowerCase().includes(q) ||
        kw.description.toLowerCase().includes(q) ||
        kw.aliases?.some((a) => a.toLowerCase().includes(q));

      return matchesCat && matchesSearch;
    });
  }, [search, selectedCategory]);

  const copyKeyword = (token: string) => {
    navigator.clipboard.writeText(token);
    setCopiedToken(token);
    setTimeout(() => setCopiedToken(null), 1500);
  };

  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Keywords Reference</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Keywords Ki List</h1>
        <p className="hero-subtitle">
          Hinglish v1.1.0 ke sabhi 30+ keywords, operators, literals aur built-in functions ki searchable list.
        </p>
      </div>

      {/* Filter & Search Bar */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2rem' }}>
        <div style={{ position: 'relative' }}>
          <Search size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Koi bhi keyword ya uska Python roop search karo (jaise agar, while, def, print)..."
            style={{
              width: '100%',
              padding: '0.85rem 1rem 0.85rem 2.8rem',
              borderRadius: '12px',
              border: '1px solid var(--border-color)',
              background: 'var(--bg-secondary)',
              color: 'var(--text-primary)',
              fontSize: '1rem',
              outline: 'none',
              transition: 'border-color 0.2s ease',
            }}
          />
        </div>

        {/* Category Pills */}
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              style={{
                border: 'none',
                background: selectedCategory === cat ? 'var(--accent-color)' : 'var(--bg-tertiary)',
                color: selectedCategory === cat ? '#ffffff' : 'var(--text-secondary)',
                fontWeight: selectedCategory === cat ? 600 : 400,
                padding: '0.35rem 0.85rem',
                borderRadius: '9999px',
                fontSize: '0.82rem',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
            >
              {cat === 'All' ? 'Sabhi (All)' : cat}
            </button>
          ))}
        </div>
      </div>

      {/* Keywords Table */}
      <div className="apple-table-container">
        <table className="apple-table">
          <thead>
            <tr>
              <th>Hinglish Keyword</th>
              <th>Category</th>
              <th>Python Mein Kya Hota Hai?</th>
              <th>Matlab aur Use</th>
              <th>Code Snippet</th>
            </tr>
          </thead>
          <tbody>
            {filteredKeywords.map((kw) => (
              <tr key={kw.token}>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <code style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--accent-color)' }}>
                      {kw.token}
                    </code>
                    <button
                      onClick={() => copyKeyword(kw.token)}
                      style={{
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        color: copiedToken === kw.token ? '#10b981' : 'var(--text-muted)',
                        padding: '2px',
                        display: 'flex',
                        alignItems: 'center'
                      }}
                      title="Keyword copy karein"
                    >
                      {copiedToken === kw.token ? <Check size={12} /> : <Copy size={12} />}
                    </button>
                  </div>
                  {kw.aliases && kw.aliases.length > 0 && (
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                      Alias: {kw.aliases.map(a => <code key={a} style={{ marginRight: '4px' }}>{a}</code>)}
                    </div>
                  )}
                </td>
                <td>
                  <span className="apple-pill" style={{ fontSize: '0.72rem', padding: '0.15rem 0.55rem' }}>
                    {kw.category}
                  </span>
                </td>
                <td>
                  <code style={{ fontSize: '0.88rem', color: '#8b5cf6', fontWeight: 500 }}>
                    {kw.python}
                  </code>
                </td>
                <td style={{ maxWidth: '280px' }}>
                  <div style={{ fontWeight: 500, fontSize: '0.88rem', marginBottom: '2px' }}>{kw.meaning}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{kw.description}</div>
                </td>
                <td style={{ minWidth: '240px' }}>
                  <pre
                    style={{
                      background: 'var(--code-bg)',
                      color: 'var(--code-text)',
                      padding: '0.5rem 0.75rem',
                      borderRadius: '8px',
                      fontSize: '0.78rem',
                      overflowX: 'auto',
                      margin: 0
                    }}
                  >
                    <code>{kw.example}</code>
                  </pre>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredKeywords.length === 0 && (
        <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
          Koi keyword nahi mila. Kuch aur search karke dekhein.
        </div>
      )}
    </div>
  );
};
