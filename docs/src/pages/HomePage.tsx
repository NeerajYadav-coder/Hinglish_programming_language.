import React, { useState } from 'react';
import { ArrowRight, Sparkles, Terminal, Cpu, FolderTree, FileCode2, ShieldCheck } from 'lucide-react';
import { CodeBlock } from '../components/CodeBlock';

interface HomePageProps {
  navigate: (route: string) => void;
}

export const HomePage: React.FC<HomePageProps> = ({ navigate }) => {
  const [activeTab, setActiveTab] = useState<'hinglish' | 'python'>('hinglish');

  const hinglishSample = `# Hinglish Source Code (.hin)
naam = "Neeraj"

agar naam == "Neeraj":
    dikhao("Namaste duniya!")
warna:
    dikhao("Hello!")
`;

  const pythonSample = `# Generated Python (Piche yeh code banta hai)
naam = "Neeraj"

if naam == "Neeraj":
    print("Namaste duniya!")
else:
    print("Hello!")
`;

  return (
    <div>
      {/* Apple-style Hero Section */}
      <section style={{ textAlign: 'center', padding: '2.5rem 0 3rem' }}>
        <div style={{ display: 'inline-flex', gap: '0.6rem', marginBottom: '1.25rem', flexWrap: 'wrap', justifyContent: 'center' }}>
          <span className="apple-pill">
            <Sparkles size={13} />
            <span>Hinglish v1.1.0 Ab Live Hai</span>
          </span>
        </div>

        <h1 className="hero-title">
          Code likho apni Hinglish mein.
        </h1>

        <p className="hero-subtitle" style={{ margin: '0 auto 2.25rem' }}>
          Real Python programming, ab bilkul simple aur natural Hinglish syntax ke sath.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <button
            onClick={() => navigate('/getting-started')}
            className="apple-button-primary"
          >
            <span>Abhi Shuru Karein</span>
            <ArrowRight size={16} />
          </button>

          <button
            onClick={() => navigate('/keywords')}
            className="apple-button-secondary"
          >
            <span>Keywords Dekhein</span>
          </button>

          <button
            onClick={() => navigate('/guide')}
            className="apple-button-secondary"
          >
            <span>Language Guide</span>
          </button>
        </div>
      </section>

      {/* Code Comparison Box */}
      <section style={{ margin: '1.5rem 0 3.5rem' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '0.75rem',
            flexWrap: 'wrap',
            gap: '0.5rem'
          }}
        >
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Dekhein Code Kaise Kaam Karta Hai</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Aapka Hinglish code piche seedha standard Python 3 mein convert hota hai.
            </p>
          </div>

          <div
            style={{
              display: 'flex',
              background: 'var(--bg-tertiary)',
              padding: '3px',
              borderRadius: '9999px',
              border: '1px solid var(--border-color)'
            }}
          >
            <button
              onClick={() => setActiveTab('hinglish')}
              style={{
                border: 'none',
                background: activeTab === 'hinglish' ? 'var(--bg-card)' : 'transparent',
                color: activeTab === 'hinglish' ? 'var(--text-primary)' : 'var(--text-muted)',
                fontWeight: activeTab === 'hinglish' ? 600 : 400,
                padding: '0.35rem 0.9rem',
                borderRadius: '9999px',
                fontSize: '0.82rem',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                boxShadow: activeTab === 'hinglish' ? '0 1px 4px rgba(0,0,0,0.08)' : 'none'
              }}
            >
              Hinglish Code (.hin)
            </button>
            <button
              onClick={() => setActiveTab('python')}
              style={{
                border: 'none',
                background: activeTab === 'python' ? 'var(--bg-card)' : 'transparent',
                color: activeTab === 'python' ? 'var(--text-primary)' : 'var(--text-muted)',
                fontWeight: activeTab === 'python' ? 600 : 400,
                padding: '0.35rem 0.9rem',
                borderRadius: '9999px',
                fontSize: '0.82rem',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                boxShadow: activeTab === 'python' ? '0 1px 4px rgba(0,0,0,0.08)' : 'none'
              }}
            >
              Python Output
            </button>
          </div>
        </div>

        {activeTab === 'hinglish' ? (
          <CodeBlock
            code={hinglishSample}
            language="hin"
            filename="program.hin"
          />
        ) : (
          <CodeBlock
            code={pythonSample}
            language="python"
            filename="program.py"
          />
        )}
      </section>

      {/* Feature Cards in Simple Hindi */}
      <section style={{ margin: '3.5rem 0' }}>
        <h2 className="section-title" style={{ textAlign: 'center', marginBottom: '2rem' }}>
          Hinglish Ki Khas Baatein
        </h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '0.75rem' }}>
              <Cpu size={24} />
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.4rem' }}>
              Real Python Compiler
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Koi guessing ya AI model nahi hai. Ek real programming language compiler aapke code ko standard Python 3 mein convert karta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '0.75rem' }}>
              <ShieldCheck size={24} />
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.4rem' }}>
              Zero Extra Setup
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Sirf Python 3.10+ chahiye. Koi heavy external software ya extra libraries install karne ki jhanjhat nahi.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '0.75rem' }}>
              <FolderTree size={24} />
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.4rem' }}>
              Badi Apps (Multi-File)
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Ek se jyada .hin files bana kar project banayein. Files ko aapas mein <code>laao</code> se import karein.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '0.75rem' }}>
              <Terminal size={24} />
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.4rem' }}>
              Aasan Terminal Commands
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Terminal se seedha <code>hinglish file.hin</code> run karein, Python code transpile karein, ya interactive REPL use karein.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '0.75rem' }}>
              <FileCode2 size={24} />
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.4rem' }}>
              VS Code Extension
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              VS Code mein .hin files kholte hi beautiful syntax colors aur bracket auto-close ka maza lein.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '0.75rem' }}>
              <Sparkles size={24} />
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.4rem' }}>
              Aasan Error Messages
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Agar code mein koi galti ho, toh accurate file name aur line number ke sath saaf error dikhayi deta hai.
            </p>
          </div>
        </div>
      </section>

      {/* Quick Start Card */}
      <section style={{ margin: '3.5rem 0' }}>
        <div className="apple-card" style={{ background: 'var(--bg-secondary)', padding: '2rem' }}>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 700, marginBottom: '0.5rem' }}>
            Quick Start — 1 Minute Mein Shuru Karein
          </h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
            Hinglish ko apne system mein pip se install karke pehla program chalao:
          </p>

          <CodeBlock
            code={`# Install karein\npip install hinglish-lang\n\n# Pehli file banayein aur run karein\necho 'dikhao("Namaste Duniya!")' > hello.hin\nhinglish hello.hin`}
            language="bash"
            filename="terminal"
          />

          <div style={{ marginTop: '1rem' }}>
            <button
              onClick={() => navigate('/getting-started')}
              className="apple-button-primary"
            >
              <span>Full Setup Guide Dekhein</span>
              <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};
