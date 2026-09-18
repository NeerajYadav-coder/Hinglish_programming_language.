import React, { useState } from 'react';
import { EXAMPLES_DATA } from '../data/examples';
import { CodeBlock } from '../components/CodeBlock';
import { ChevronRight } from 'lucide-react';

export const ExamplesPage: React.FC = () => {
  const [selectedId, setSelectedId] = useState(EXAMPLES_DATA[0].id);
  const currentExample = EXAMPLES_DATA.find((e) => e.id === selectedId) || EXAMPLES_DATA[0];

  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Code Gallery</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Working Code Examples</h1>
        <p className="hero-subtitle">
          Hello World se lekar advanced async aur pattern matching tak ke 11 real working examples.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(240px, 280px) 1fr', gap: '2rem', alignItems: 'start' }}>
        {/* Left Side: Example Selector list */}
        <div
          className="apple-card"
          style={{
            padding: '0.75rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '4px',
            position: 'sticky',
            top: '80px',
            maxHeight: 'calc(100vh - 120px)',
            overflowY: 'auto'
          }}
        >
          <div style={{ padding: '0.5rem 0.75rem', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            Example Select Karein
          </div>
          {EXAMPLES_DATA.map((ex) => {
            const isSelected = ex.id === selectedId;
            return (
              <button
                key={ex.id}
                onClick={() => setSelectedId(ex.id)}
                style={{
                  border: 'none',
                  background: isSelected ? 'var(--accent-soft)' : 'transparent',
                  color: isSelected ? 'var(--accent-color)' : 'var(--text-primary)',
                  padding: '0.6rem 0.85rem',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  textAlign: 'left',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  transition: 'all 0.15s ease',
                  fontSize: '0.85rem',
                  fontWeight: isSelected ? 600 : 400
                }}
              >
                <span>{ex.title}</span>
                {isSelected && <ChevronRight size={14} />}
              </button>
            );
          })}
        </div>

        {/* Right Side: Selected Example Details */}
        <div>
          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">{currentExample.category}</span>
            </div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.4rem' }}>
              {currentExample.title}
            </h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6 }}>
              {currentExample.description}
            </p>

            <div style={{ display: 'flex', gap: '0.4rem', marginTop: '0.75rem', flexWrap: 'wrap' }}>
              {currentExample.keyConcepts.map((concept) => (
                <span
                  key={concept}
                  style={{
                    fontSize: '0.75rem',
                    padding: '0.15rem 0.5rem',
                    borderRadius: '6px',
                    background: 'var(--bg-tertiary)',
                    color: 'var(--text-muted)'
                  }}
                >
                  #{concept}
                </span>
              ))}
            </div>
          </div>

          <h3 className="subsection-title">Hinglish Code (.hin)</h3>
          <CodeBlock
            code={currentExample.hinglishCode}
            language="hin"
            filename="example.hin"
          />

          <h3 className="subsection-title">Generated Python Code</h3>
          <CodeBlock
            code={currentExample.pythonCode}
            language="python"
            filename="example.py"
          />

          <h3 className="subsection-title">Terminal Output (Result)</h3>
          <div
            style={{
              background: 'var(--code-bg)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              borderRadius: '12px',
              padding: '1rem 1.25rem',
              color: '#10b981',
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: '0.88rem',
              lineHeight: 1.6,
              whiteSpace: 'pre-wrap'
            }}
          >
            {currentExample.output}
          </div>
        </div>
      </div>
    </div>
  );
};
