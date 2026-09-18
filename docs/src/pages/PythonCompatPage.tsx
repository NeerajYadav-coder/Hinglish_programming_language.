import React from 'react';
import { CheckCircle2, AlertTriangle } from 'lucide-react';

export const PythonCompatPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Execution Model</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Python Sangatata (Python Semantics)</h1>
        <p className="hero-subtitle">
          Hinglish ka execution pipeline, Python ke sath relation, aur transparent semantics.
        </p>
      </div>

      {/* Core Architectural Pipeline */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Hinglish Compilation Pipeline</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          Hinglish ek compiler-based language interface hai jo deterministic pipeline par aadharit hai:
        </p>

        <div className="apple-card" style={{ textAlign: 'center', padding: '2rem 1.5rem', background: 'var(--bg-secondary)' }}>
          <div style={{ display: 'inline-flex', flexDirection: 'column', gap: '0.75rem', alignItems: 'center', width: '100%', maxWidth: '480px' }}>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center' }}>
              📄 Hinglish Source (.hin)
            </div>
            <div style={{ color: 'var(--text-muted)' }}>↓</div>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center' }}>
              🔍 Lexer / Tokenizer (Indentation Tracker)
            </div>
            <div style={{ color: 'var(--text-muted)' }}>↓</div>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center' }}>
              🌳 Hinglish Abstract Syntax Tree (AST)
            </div>
            <div style={{ color: 'var(--text-muted)' }}>↓</div>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center' }}>
              ⚙️ Compiler / Code Generator
            </div>
            <div style={{ color: 'var(--text-muted)' }}>↓</div>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center' }}>
              🐍 Python 3 Source / Bytecode
            </div>
            <div style={{ color: 'var(--text-muted)' }}>↓</div>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center', background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', borderColor: 'rgba(16, 185, 129, 0.3)' }}>
              ⚡ CPython compile() & exec() Runtime
            </div>
          </div>
        </div>
      </section>

      {/* No Custom VM Explanation */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Hinglish Koi Naya VM (Virtual Machine) Nahi Hai</h2>
        <div className="apple-card">
          <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, fontSize: '0.95rem', marginBottom: '1rem' }}>
            Hinglish alag bytecode interpreter ya custom virtual machine nahi banata. 
            Iske bajaay, Hinglish ka formal parser aur AST compiler Hinglish syntax ko sidhe valid 
            standard <strong>Python 3 semantics</strong> mein compile karta hai.
          </p>
          <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, fontSize: '0.95rem' }}>
            Iska sabse bada laabh yeh hai ki Python standard library ke sabhi powerful modules 
            (jaise <code>math</code>, <code>json</code>, <code>asyncio</code>, <code>datetime</code>, <code>pathlib</code>) 
            bina kisi artificial wrapper ya speed penalty ke seedhe upyog kiye ja sakte hain.
          </p>
        </div>
      </section>

      {/* Implementation Scope & Known Limitations */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Laagu Visheshtayein aur Limitations</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Hinglish v1.0.0 ke vastavik status aur limitations ka satya vivran:
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', marginBottom: '0.75rem', fontWeight: 600 }}>
              <CheckCircle2 size={18} />
              <span>Purnatah Uplabdh (Fully Supported)</span>
            </div>
            <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.8 }}>
              <li>Variables, Types, Expressions, Operators</li>
              <li>Conditionals (agar, warna_agar, warna)</li>
              <li>Loops (jabtak, har ... mein, ruko, aage_bado)</li>
              <li>Functions (kaam, default args, *args, **kwargs, /, *)</li>
              <li>Inline Lambdas (sookshm) aur Decorators (@)</li>
              <li>OOP (varg, khood, inheritance, methods)</li>
              <li>Exceptions (koshish, pakdo, antatah, uthav, daawa)</li>
              <li>Context Managers (saath, jaise)</li>
              <li>Generators aur yield (upaj, se_upaj)</li>
              <li>Async/await (asamanantar, intezaar)</li>
              <li>Structural Pattern Matching (milao, sthiti)</li>
              <li>Standard type annotations aur Walrus operator (:=)</li>
            </ul>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b', marginBottom: '0.75rem', fontWeight: 600 }}>
              <AlertTriangle size={18} />
              <span>Gyaat Seemayein (Known Limitations)</span>
            </div>
            <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.8 }}>
              <li>
                <strong>PEP 695 Type Parameters:</strong> Python 3.12+ ka <code>type List[T] = list[T]</code> ya <code>def f[T](x: T)</code> syntax Hinglish grammar mein abhi shamil nahi hai. Standard variable annotations (<code>x: int = 10</code>) purnatah chalte hain.
              </li>
              <li>
                <strong>Target Python:</strong> Python 3.10+ aavashyak hai kyunki structural pattern matching (<code>milao / sthiti</code>) Python 3.10 engine par aadharit hai.
              </li>
              <li>
                <strong>Language Scope:</strong> Hinglish ek syntax and language layer hai, independent operating system ya C runtime nahi.
              </li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  );
};
