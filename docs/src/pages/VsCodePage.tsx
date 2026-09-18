import React from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { CheckCircle2, XCircle } from 'lucide-react';

export const VsCodePage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Editor Tooling</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>VS Code Extension Tooling</h1>
        <p className="hero-subtitle">
          Visual Studio Code mein Hinglish <code>.hin</code> source files ke liye syntax highlighting aur configuration.
        </p>
      </div>

      {/* Extension Overview */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Extension Vivran</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.7 }}>
          Hinglish project ke sath ek dedicated VS Code extension uplabdh hai jo repository ke <code>vscode-hinglish/</code> 
          folder mein sthit hai. Yeh extension TextMate grammar ke aadhar par Hinglish vocabulary ko sundar syntax highlighting pradan karta hai.
        </p>

        <div className="apple-card" style={{ background: 'var(--bg-secondary)', marginBottom: '2rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.75rem' }}>
            VSIX Package Se Install Karein
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem' }}>
            Terminal mein neeche di gayi command chala kar extension ko sidhe install karein:
          </p>

          <CodeBlock
            code={`# VS Code CLI se pre-packaged VSIX install karein\ncode --install-extension vscode-hinglish/hinglish-1.0.0.vsix`}
            language="bash"
            filename="terminal"
          />
        </div>
      </section>

      {/* What it provides vs does NOT provide */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Extension Ki Vartaman Kshamta (Capabilities)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          Ham transparently yeh spasht karte hain ki vartaman v1.0.0 extension mein kya shamil hai aur kya abhi shamil nahi hai:
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', marginBottom: '1rem', fontWeight: 600 }}>
              <CheckCircle2 size={20} />
              <span>Kya Uplabdh Hai (Supported)</span>
            </div>
            <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.8 }}>
              <li><strong>.hin File Recognition:</strong> <code>.hin</code> extension wali files automatically Hinglish mode mein khulti hain.</li>
              <li><strong>Rich Syntax Highlighting:</strong> Keywords, control flow, functions, classes, decorators, f-strings, aur numbers ka vivid TextMate scope mapping.</li>
              <li><strong>Bracket Matching:</strong> Parentheses <code>()</code>, square brackets <code>[]</code>, curly braces <code>{}</code> auto-closing aur surrounding pairs.</li>
              <li><strong>Comments Toggle:</strong> <code>Ctrl+/</code> (ya <code>Cmd+/</code>) se Hinglish <code>#</code> comments toggle karna.</li>
            </ul>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', marginBottom: '1rem', fontWeight: 600 }}>
              <XCircle size={20} />
              <span>Kya Abhi Shamil Nahi Hai (Not Yet)</span>
            </div>
            <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: 1.8 }}>
              <li>Language Server Protocol (LSP)</li>
              <li>IntelliSense / Autocomplete</li>
              <li>Semantic real-time diagnostics / red squiggles</li>
              <li>Go to definition / Peek definition</li>
              <li>Symbol Rename (F2)</li>
              <li>Interactive Debugger (breakpoints / step-into)</li>
              <li>Auto code formatter (Prettier / Black style)</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Manual Testing File */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Manual Visual Inspection File</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Syntax highlighting ko parakhne ke liye <code>examples/editor_demo.hin</code> file ka upyog karein:
        </p>

        <CodeBlock
          code={`# VS Code mein demo file kholein
code examples/editor_demo.hin`}
          language="bash"
          filename="terminal"
        />
      </section>
    </div>
  );
};
