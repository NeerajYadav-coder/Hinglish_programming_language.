import React from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { CheckCircle2, Sparkles, Terminal, Cpu } from 'lucide-react';

export const VsCodePage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Code Editor Tooling</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>VS Code & Language Server (LSP)</h1>
        <p className="hero-subtitle">
          Visual Studio Code mein Hinglish <code>.hin</code> files ke liye real-time syntax checking, auto-complete, hover docs, aur cross-file navigation.
        </p>
      </div>

      {/* Extension Overview */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Extension Kaise Install Karein?</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.7 }}>
          Hinglish repository ke <code>vscode-hinglish/</code> folder mein updated LSP-enabled extension maujood hai. 
          Ise terminal se ek single command chala kar install kar sakte hain:
        </p>

        <div className="apple-card" style={{ background: 'var(--bg-secondary)', marginBottom: '2rem' }}>
          <CodeBlock
            code={`# 1. Ensure hinglish installed in python\npip install .\n\n# 2. Install VS Code extension\ncode --install-extension vscode-hinglish/hinglish-1.0.0.vsix`}
            language="bash"
            filename="terminal"
          />
        </div>
      </section>

      {/* Language Server Features */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Hinglish LSP Ke Powerful Features</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          Official Hinglish Compiler par based zero-runtime-dependency Language Server:
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', marginBottom: '1rem', fontWeight: 600 }}>
              <CheckCircle2 size={20} />
              <span>Live Error Diagnostics</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Code type karte hi red wavy underlines ke saath syntax aur indentation mistakes dikhti hain. Incomplete code type karne par editor freeze nahi hota.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#3b82f6', marginBottom: '1rem', fontWeight: 600 }}>
              <Sparkles size={20} />
              <span>Smart Autocompletion</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Keywords (<code>agar</code>, <code>kaam</code>, <code>har</code>), builtins (<code>dikhao</code>, <code>pucho</code>), snippets, aur aapke local functions/variables ka instant suggestion.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b', marginBottom: '1rem', fontWeight: 600 }}>
              <Cpu size={20} />
              <span>Hover & Go to Definition</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Kisi bhi keyword ya function par mouse le jaane par Python equivalent aur documentation dikhega. <code>F12</code> dabakar local ya sibling <code>.hin</code> files mein jump karein.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#8b5cf6', marginBottom: '1rem', fontWeight: 600 }}>
              <Terminal size={20} />
              <span>Outline & Safe Rename</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              VS Code ke Outline panel mein classes, methods aur functions ka clean tree view milta hai. <code>F2</code> dabakar variables aur functions ko safely rename karein.
            </p>
          </div>
        </div>
      </section>

      {/* Settings section */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Extension Settings</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          VS Code settings (<code>settings.json</code>) mein aap language server ko customize kar sakte hain:
        </p>

        <CodeBlock
          code={`{\n  "hinglish.lsp.enabled": true,\n  "hinglish.lsp.path": "hinglish-lsp",\n  "hinglish.lsp.pythonPath": "python3",\n  "hinglish.lsp.trace.server": "off"\n}`}
          language="json"
          filename="settings.json"
        />
      </section>

      {/* Manual Testing File */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Demo File Kholkar Check Karein</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Real testing ke liye <code>examples/editor_demo.hin</code> file ko VS Code mein open karein:
        </p>

        <CodeBlock
          code={`# VS Code mein demo open karein\ncode examples/editor_demo.hin`}
          language="bash"
          filename="terminal"
        />
      </section>
    </div>
  );
};
