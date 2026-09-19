import React from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { AlignLeft, CheckCircle2, RefreshCw, Terminal, FileCode2, ShieldCheck, Sparkles } from 'lucide-react';

export const FormatterPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Developer Tools</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Hinglish Code Formatter</h1>
        <p className="hero-subtitle">
          Ek real, deterministic AST-based source formatter jo aapke Hinglish (<code>.hin</code>) code ko clean, readable aur consistent banata hai bina logic change kiye.
        </p>
      </div>

      {/* Highlights Grid */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Formatter Ki Khasiyat</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Hinglish formatter koi regex ya LLM text replacer nahi hai — yeh language ke actual <strong>Lexer, Parser aur AST</strong> ke through code ko inspect karke canonical style mein transform karta hai.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#3b82f6', marginBottom: '0.75rem', fontWeight: 600 }}>
              <AlignLeft size={20} />
              <span>Canonical 4-Space Indents</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Python aur Hinglish ke block semantics ko strictly preserve karte hue inconsistent spaces aur tabs ko clean 4 spaces mein standardize karta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', marginBottom: '0.75rem', fontWeight: 600 }}>
              <RefreshCw size={20} />
              <span>100% Idempotent</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              <code>format(format(code)) == format(code)</code>. Chahe aap 1 baar format karein ya 100 baar, second pass byte-for-byte identical output deta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#8b5cf6', marginBottom: '0.75rem', fontWeight: 600 }}>
              <Sparkles size={20} />
              <span>Preserves Comments & Strings</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Standalone aur inline comments (<code># ...</code>), escape sequences, quotes, aur f-strings ko bina kisi disturbance ke preserve rakhta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b', marginBottom: '0.75rem', fontWeight: 600 }}>
              <ShieldCheck size={20} />
              <span>Semantic Preservation</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Operator precedence aur mathematical order ko preserve karta hai. Formatter kabhi bhi program ka meaning ya AST execution change nahi karta.
            </p>
          </div>
        </div>
      </section>

      {/* Code Comparison Example */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Before vs After Comparison</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Dekhein kaise messy code clean aur readable ban jata hai:
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
          <div>
            <div style={{ fontWeight: 600, color: '#ef4444', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span>Unformatted (Messy) Code</span>
            </div>
            <CodeBlock language="hinglish" code={`# Header comment
x=10+20*30 # Inline comment
agar x>50:
  dikhao("High")
warna:
    dikhao("Low")

kaam greet(naam,umar=21):
  wapas f"Hello {naam}, age {umar}!"`} />
          </div>

          <div>
            <div style={{ fontWeight: 600, color: '#10b981', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <CheckCircle2 size={18} />
              <span>Canonical Formatted Code</span>
            </div>
            <CodeBlock language="hinglish" code={`# Header comment
x = 10 + 20 * 30  # Inline comment

agar x > 50:
    dikhao("High")
warna:
    dikhao("Low")


kaam greet(naam, umar=21):
    wapas f"Hello {naam}, age {umar}!"`} />
          </div>
        </div>
      </section>

      {/* CLI Usage */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Terminal / CLI Usage</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Hinglish CLI ke sath format command use karna super aasan hai:
        </p>

        <div className="apple-card" style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)', fontWeight: 600, marginBottom: '0.75rem' }}>
            <Terminal size={18} />
            <span>1. In-Place Formatting (File ko seedha update karein)</span>
          </div>
          <CodeBlock language="bash" code="hinglish format program.hin" />
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', marginTop: '0.5rem' }}>
            Yeh file ko read karke usi file ko canonical format mein safely overwrite kar deta hai.
          </p>
        </div>

        <div className="apple-card" style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)', fontWeight: 600, marginBottom: '0.75rem' }}>
            <Terminal size={18} />
            <span>2. CI/CD & Pre-commit Check Mode (--check)</span>
          </div>
          <CodeBlock language="bash" code="hinglish format program.hin --check" />
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', marginTop: '0.5rem' }}>
            Files ko modify nahi karta. Agar file perfectly formatted hai toh exit code <code>0</code> return karega, aur agar changes needed hain toh exit code <code>1</code> return karega.
          </p>
        </div>

        <div className="apple-card" style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)', fontWeight: 600, marginBottom: '0.75rem' }}>
            <Terminal size={18} />
            <span>3. Output to Another File (-o)</span>
          </div>
          <CodeBlock language="bash" code="hinglish format source.hin -o formatted.hin" />
        </div>

        <div className="apple-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-primary)', fontWeight: 600, marginBottom: '0.75rem' }}>
            <Terminal size={18} />
            <span>4. Stdin / Pipe Support (-)</span>
          </div>
          <CodeBlock language="bash" code='cat program.hin | hinglish format -' />
        </div>
      </section>

      {/* VS Code Integration */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">VS Code Integration</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Hinglish VS Code extension aur Language Server (LSP) mein document formatting built-in hai:
        </p>

        <div className="apple-card" style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#3b82f6', fontWeight: 600, marginBottom: '0.75rem' }}>
            <FileCode2 size={18} />
            <span>Format Document Command</span>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7, marginBottom: '0.75rem' }}>
            Editor mein kisi bhi <code>.hin</code> file par right click karke <strong>Format Document</strong> select karein ya shortcut use karein:
          </p>
          <ul style={{ listStyle: 'disc', paddingLeft: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.8 }}>
            <li><strong>Windows / Linux:</strong> <code>Shift + Alt + F</code></li>
            <li><strong>macOS:</strong> <code>Shift + Option + F</code></li>
          </ul>
        </div>

        <div className="apple-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', fontWeight: 600, marginBottom: '0.75rem' }}>
            <CheckCircle2 size={18} />
            <span>Auto Format on Save (Optional)</span>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7, marginBottom: '0.75rem' }}>
            Agar aap file save karte hi automatically format karwana chahte hain, toh VS Code <code>settings.json</code> mein yeh configure karein:
          </p>
          <CodeBlock language="json" code={`{
  "[hinglish]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "neerajyadav.hinglish"
  }
}`} />
        </div>
      </section>
    </div>
  );
};
