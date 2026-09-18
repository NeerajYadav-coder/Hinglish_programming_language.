import React from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { CheckCircle2 } from 'lucide-react';

export const GettingStartedPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Aasan Guide</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Shuru Kaise Karein (Getting Started)</h1>
        <p className="hero-subtitle">
          Hinglish install karein, apna pehla program banayein, aur terminal se run karein.
        </p>
      </div>

      <div className="apple-callout success">
        <CheckCircle2 size={20} style={{ color: '#10b981', flexShrink: 0, marginTop: '2px' }} />
        <div>
          <strong>Sirf Python 3.10+ Chahiye:</strong> Hinglish ke liye aapke computer mein sirf standard <strong>Python 3.10 ya usse naya</strong> version hona chahiye. Koi bhi heavy external library nahi chahiye!
        </div>
      </div>

      {/* Step 1 */}
      <section style={{ margin: '2.5rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            1
          </span>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 600 }}>Hinglish Install Karein</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem', fontSize: '0.95rem' }}>
          Repository folder mein jaakar terminal par pip se seedha install karein:
        </p>

        <CodeBlock
          code={`# Folder se install karein\npip install .\n\n# Ya pre-built wheel file se install karein\npip install dist/hinglish-1.0.0-py3-none-any.whl`}
          language="bash"
          filename="terminal"
        />

        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.5rem' }}>
          Check karein ki install ho gaya ya nahi:
        </p>
        <CodeBlock
          code={`hinglish --version\n# Output: Hinglish 1.0.0`}
          language="bash"
          filename="terminal"
        />
      </section>

      {/* Step 2 */}
      <section style={{ margin: '2.5rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            2
          </span>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 600 }}>Pehli .hin File Banayein</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem', fontSize: '0.95rem' }}>
          Hinglish code ko <code>.hin</code> extension wali file mein likhte hain. Ek nayi file banayein <code>hello.hin</code>:
        </p>

        <CodeBlock
          code={`# hello.hin
naam = "Neeraj"

agar naam == "Neeraj":
    dikhao("Namaste duniya!")
warna:
    dikhao("Hello!")`}
          language="hin"
          filename="hello.hin"
        />
      </section>

      {/* Step 3 */}
      <section style={{ margin: '2.5rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            3
          </span>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 600 }}>File Run Karein</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem', fontSize: '0.95rem' }}>
          File chalane ke liye terminal par <code>hinglish hello.hin</code> likhein:
        </p>

        <CodeBlock
          code={`# Seedha file ka naam dekar run karein\nhinglish hello.hin\n\n# Ya Python module se run karein\npython3 -m hinglish hello.hin`}
          language="bash"
          filename="terminal"
        />

        <div className="apple-card" style={{ background: 'var(--bg-secondary)', padding: '0.85rem 1.2rem' }}>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '2px' }}>Output:</div>
          <code style={{ fontSize: '0.95rem', color: '#10b981' }}>Namaste duniya!</code>
        </div>
      </section>

      {/* Step 4 */}
      <section style={{ margin: '2.5rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            4
          </span>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 600 }}>Interactive REPL (Direct Terminal Shell)</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem', fontSize: '0.95rem' }}>
          Bina file banaye code test karne ke liye terminal par seedha <code>hinglish</code> chalao:
        </p>

        <CodeBlock
          code={`$ hinglish\nHinglish 1.0.0 Interactive REPL\nBahar aane ke liye "exit()" likhein ya Ctrl-D dabayein.\n\n>>> x = 10\n>>> agar x > 5:\n...     dikhao(f"Badi sankhya: {x}")\n...\nBadi sankhya: 10\n>>>`}
          language="text"
          filename="interactive-shell"
        />
      </section>

      {/* Step 5 */}
      <section style={{ margin: '2.5rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            5
          </span>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 600 }}>Python Code Dekhna (Transpile)</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem', fontSize: '0.95rem' }}>
          Aap dekh sakte hain ki compiler ne piche kaunsa Python code generate kiya hai:
        </p>

        <CodeBlock
          code={`# Screen par Python code dekhein\nhinglish transpile hello.hin\n\n# Python code ko nayi .py file mein save karein\nhinglish transpile hello.hin -o hello.py`}
          language="bash"
          filename="terminal"
        />
      </section>

      {/* Step 6 */}
      <section style={{ margin: '2.5rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            6
          </span>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 600 }}>Tokens aur AST Check Karna</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem', fontSize: '0.95rem' }}>
          Compiler ke internal tokens aur tree structure dekhne ke liye:
        </p>

        <CodeBlock
          code={`# Tokens stream dekhein\nhinglish tokens hello.hin\n\n# Abstract Syntax Tree (AST) dekhein\nhinglish ast hello.hin`}
          language="bash"
          filename="terminal"
        />
      </section>
    </div>
  );
};
