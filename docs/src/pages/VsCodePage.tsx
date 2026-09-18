import React from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { CheckCircle2, XCircle } from 'lucide-react';

export const VsCodePage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Code Editor Tooling</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>VS Code Extension Setup</h1>
        <p className="hero-subtitle">
          Visual Studio Code mein Hinglish <code>.hin</code> files ke liye syntax colors aur automatic brackets setup.
        </p>
      </div>

      {/* Extension Overview */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Extension Kaise Install Karein?</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.7 }}>
          Hinglish repository ke <code>vscode-hinglish/</code> folder mein ek ready-to-use extension maujood hai. 
          Ise terminal se ek single command chala kar install kar sakte hain:
        </p>

        <div className="apple-card" style={{ background: 'var(--bg-secondary)', marginBottom: '2rem' }}>
          <CodeBlock
            code={`# Terminal mein yeh command run karein\ncode --install-extension vscode-hinglish/hinglish-1.0.0.vsix`}
            language="bash"
            filename="terminal"
          />
        </div>
      </section>

      {/* What it provides vs does NOT provide */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Extension Mein Kya-Kya Features Hain?</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          Hum bilkul clearly bata rahe hain ki abhi kya supported hai aur aage kya aayega:
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', marginBottom: '1rem', fontWeight: 600 }}>
              <CheckCircle2 size={20} />
              <span>Abhi Available Hai (Supported)</span>
            </div>
            <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.8 }}>
              <li><strong>.hin File Recognition:</strong> <code>.hin</code> file kholte hi VS Code automatically Hinglish mode on kar deta hai.</li>
              <li><strong>Colorful Syntax Highlighting:</strong> Keywords, numbers, strings, function names aur classes ke sundar colors.</li>
              <li><strong>Auto-Closing Brackets:</strong> <code>()</code>, <code>[]</code>, <code>{}</code> type karte hi automatically band ho jate hain.</li>
              <li><strong>Comment Shortcut:</strong> <code>Ctrl+/</code> (ya <code>Cmd+/</code>) dabakar comment lagana aur hatana.</li>
            </ul>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', marginBottom: '1rem', fontWeight: 600 }}>
              <XCircle size={20} />
              <span>Future Updates Mein Aayega</span>
            </div>
            <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-muted)', fontSize: '0.88rem', lineHeight: 1.8 }}>
              <li>Autocomplete / IntelliSense (suggestion list)</li>
              <li>Language Server (LSP)</li>
              <li>Go to definition (F12)</li>
              <li>Rename Symbol (F2)</li>
              <li>Interactive Debugger (Breakpoints)</li>
              <li>Auto Formatter (Prettier style)</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Manual Testing File */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Demo File Kholkar Check Karein</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Syntax colors dekhne ke liye <code>examples/editor_demo.hin</code> file ko VS Code mein open karein:
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
