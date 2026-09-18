import React from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { CheckCircle2 } from 'lucide-react';

export const GettingStartedPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Prarambhik Nirdesh</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Shuru Karein (Getting Started)</h1>
        <p className="hero-subtitle">
          Hinglish v1.0.0 ko install karein, pehla program likhein, aur shaktishali CLI tools ka upyog karein.
        </p>
      </div>

      <div className="apple-callout success">
        <CheckCircle2 size={20} style={{ color: '#10b981', flexShrink: 0, marginTop: '2px' }} />
        <div>
          <strong>Zaroori Yogyata (Prerequisites):</strong> Hinglish ke liye keval standard <strong>Python 3.10+</strong> ki aavashyakta hai. 
          Keval CPython standard library ka upyog hota hai — koi third-party heavy dependencies nahi chahiye!
        </div>
      </div>

      {/* Step 1 */}
      <section style={{ margin: '3rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            1
          </span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 600 }}>Hinglish Install Karein</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.95rem' }}>
          Repository clone karne ke baad local folder se seedha install karein ya pre-built wheel package ka upyog karein:
        </p>

        <CodeBlock
          code={`# Source folder se pip dwara install karein\npip install .\n\n# Ya pre-built wheel se install karein\npip install dist/hinglish-1.0.0-py3-none-any.whl`}
          language="bash"
          filename="terminal"
        />

        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Installation check karne ke liye version dekhein:
        </p>
        <CodeBlock
          code={`hinglish --version\n# Output: Hinglish 1.0.0`}
          language="bash"
          filename="terminal"
        />
      </section>

      {/* Step 2 */}
      <section style={{ margin: '3rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            2
          </span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 600 }}>Pehla Hinglish Source File (.hin) Banayein</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.95rem' }}>
          Hinglish programs standard UTF-8 encoded text files hoti hain jinka extension <code>.hin</code> hota hai. 
          Ek nayi file <code>hello.hin</code> banayein:
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
      <section style={{ margin: '3rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            3
          </span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 600 }}>Program Run Karein</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.95rem' }}>
          Script ko execute karne ke liye console command <code>hinglish</code> ka upyog karein:
        </p>

        <CodeBlock
          code={`# Direct shorthand syntax\nhinglish hello.hin\n\n# Explicit subcommand syntax\nhinglish run hello.hin\n\n# Python module syntax se chalana\npython3 -m hinglish hello.hin`}
          language="bash"
          filename="terminal"
        />

        <div className="apple-card" style={{ background: 'var(--bg-secondary)', padding: '1rem 1.25rem' }}>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '4px' }}>Expected Output:</div>
          <code style={{ fontSize: '0.95rem', color: '#10b981' }}>Namaste duniya!</code>
        </div>
      </section>

      {/* Step 4 */}
      <section style={{ margin: '3rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            4
          </span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 600 }}>Interactive REPL ka Upyog</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.95rem' }}>
          Terminal par seedha <code>hinglish</code> ya <code>hinglish repl</code> run karne se interactive shell shuru ho jata hai:
        </p>

        <CodeBlock
          code={`$ hinglish\nHinglish 1.0.0 Interactive REPL\nType "exit()", "quit()", or Ctrl-D to exit.\n\n>>> x = 10\n>>> agar x > 5:\n...     dikhao(f"Badi sankhya: {x}")\n...\nBadi sankhya: 10\n>>>`}
          language="text"
          filename="interactive-shell"
        />
      </section>

      {/* Step 5 */}
      <section style={{ margin: '3rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            5
          </span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 600 }}>Python Mein Transpile Karna</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.95rem' }}>
          Agar aap dekhna chahte hain ki Hinglish compiler ne kaunsa Python code generate kiya hai, 
          toh <code>transpile</code> subcommand ka upyog karein:
        </p>

        <CodeBlock
          code={`# Screen par Python code dekhein\nhinglish transpile hello.hin\n\n# Python code ko nayi file mein save karein (-o flag)\nhinglish transpile hello.hin -o hello.py`}
          language="bash"
          filename="terminal"
        />
      </section>

      {/* Step 6 */}
      <section style={{ margin: '3rem 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <span className="apple-pill" style={{ fontSize: '0.85rem', width: '28px', height: '28px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%' }}>
            6
          </span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 600 }}>Tokens aur AST Inspect Karna</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.95rem' }}>
          Developer diagnostics ke liye aap lexer ke tokens aur parser ka Abstract Syntax Tree (AST) dekh sakte hain:
        </p>

        <CodeBlock
          code={`# Lexer tokens inspect karein\nhinglish tokens hello.hin\n# ya shorthand:\nhinglish --tokens hello.hin\n\n# Abstract Syntax Tree (AST) inspect karein\nhinglish ast hello.hin\n# ya shorthand:\nhinglish --ast hello.hin`}
          language="bash"
          filename="terminal"
        />
      </section>
    </div>
  );
};
