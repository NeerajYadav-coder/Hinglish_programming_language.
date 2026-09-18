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

  const pythonSample = `# Generated Python (Swayam Transpile Hota Hai)
naam = "Neeraj"

if naam == "Neeraj":
    print("Namaste duniya!")
else:
    print("Hello!")
`;

  return (
    <div>
      {/* Apple-style Hero Section */}
      <section style={{ textAlign: 'center', padding: '3rem 0 3.5rem' }}>
        <div style={{ display: 'inline-flex', marginBottom: '1.25rem' }}>
          <span className="apple-pill">
            <Sparkles size={13} />
            <span>Hinglish v1.0.0 Ab Uplabdh Hai</span>
          </span>
        </div>

        <h1 className="hero-title">
          Python ki shakti.<br />
          Apni bhasha ka apnaapan.
        </h1>

        <p className="hero-subtitle" style={{ margin: '0 auto 2.5rem' }}>
          Hinglish ek Python-backed programming language interface hai jismein aap 
          Hindi aur Hinglish ke sahaj shabdon se code likh sakte hain, jabki 
          CPython ka poora ecosystem aur execution transparently barkaraar rehte hain.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <button
            onClick={() => navigate('/getting-started')}
            className="apple-button-primary"
          >
            <span>Shuru Karein (Get Started)</span>
            <ArrowRight size={16} />
          </button>

          <button
            onClick={() => navigate('/keywords')}
            className="apple-button-secondary"
          >
            <span>Shabdakosh (Keywords)</span>
          </button>

          <button
            onClick={() => navigate('/guide')}
            className="apple-button-secondary"
          >
            <span>Bhasha Nirdeshika</span>
          </button>
        </div>
      </section>

      {/* Interactive Code Comparison Preview */}
      <section style={{ margin: '2rem 0 4rem' }}>
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
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Dekhein Hinglish Kaise Kaam Karti Hai</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Source code deterministic AST compiler dwara standard Python mein compile hota hai.
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
                fontSize: '0.8rem',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                boxShadow: activeTab === 'hinglish' ? '0 1px 4px rgba(0,0,0,0.08)' : 'none'
              }}
            >
              Hinglish Source (.hin)
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
                fontSize: '0.8rem',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                boxShadow: activeTab === 'python' ? '0 1px 4px rgba(0,0,0,0.08)' : 'none'
              }}
            >
              Generated Python 3
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

      {/* Apple-style Lean Feature Cards */}
      <section style={{ margin: '4rem 0' }}>
        <h2 className="section-title" style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          Mukhya Visheshtayein (Core Highlights)
        </h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.5rem' }}>
          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '1rem' }}>
              <Cpu size={24} />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              Deterministic AST Compiler
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Koi regex ya LLM guessing nahi. Hinglish source text ek formal typed AST mein parse hota hai 
              aur verified Python 3 semantics mein translate hota hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '1rem' }}>
              <ShieldCheck size={24} />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              Zero Runtime Dependency
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Bina kisi third-party external runtime library ke chalta hai. Standard CPython 3.10+ par seedha run karein.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '1rem' }}>
              <FolderTree size={24} />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              Bahu-File (Multi-File) Projects
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Ek se adhik .hin files mein modular architecture banayein. Native module import aur working directory independence shamil hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '1rem' }}>
              <Terminal size={24} />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              Shaktishali CLI aur REPL
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Console commands: <code>run</code>, <code>transpile</code>, <code>tokens</code>, <code>ast</code>, 
              interactive REPL, aur standard input pipelines (<code>cat file.hin | hinglish</code>).
            </p>
          </div>

          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '1rem' }}>
              <FileCode2 size={24} />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              VS Code Tooling
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              VS Code extension dwara .hin files ke liye full syntax highlighting, bracket auto-closing aur language configuration uplabdh hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ color: 'var(--accent-color)', marginBottom: '1rem' }}>
              <Sparkles size={24} />
            </div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              Source-Mapped Tracebacks
            </h3>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Runtime exceptions aane par accurate .hin file name, exact line number, aur code snippet dikhata hai.
            </p>
          </div>
        </div>
      </section>

      {/* Quick Setup Card */}
      <section style={{ margin: '4rem 0' }}>
        <div className="apple-card" style={{ background: 'var(--bg-secondary)', padding: '2.25rem' }}>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '0.5rem' }}>
            Turant Shuru Karein (Quick Start)
          </h2>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Hinglish package ko Python 3.10+ environment mein seedha pip dwara install karein:
          </p>

          <CodeBlock
            code={`# Repository se install karein\npip install .\n\n# Pehla program banayein aur run karein\necho 'dikhao("Namaste Duniya!")' > hello.hin\nhinglish hello.hin`}
            language="bash"
            filename="terminal"
          />

          <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem', flexWrap: 'wrap' }}>
            <button
              onClick={() => navigate('/getting-started')}
              className="apple-button-primary"
            >
              <span>Poori Getting Started Guide Dekhein</span>
              <ArrowRight size={16} />
            </button>
          </div>
        </div>
      </section>
    </div>
  );
};
