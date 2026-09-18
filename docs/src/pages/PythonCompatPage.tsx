import React from 'react';
import { CheckCircle2, AlertTriangle } from 'lucide-react';

export const PythonCompatPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Python Integration</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Python ke Sath Compatibility</h1>
        <p className="hero-subtitle">
          Hinglish background mein Python ke sath kaise connect hoti hai aur kaise chalti hai.
        </p>
      </div>

      {/* Core Architectural Pipeline */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Hinglish Execution Pipeline</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          Jab aap code run karte hain, toh step-by-step yeh process hota hai:
        </p>

        <div className="apple-card" style={{ textAlign: 'center', padding: '2rem 1.5rem', background: 'var(--bg-secondary)' }}>
          <div style={{ display: 'inline-flex', flexDirection: 'column', gap: '0.75rem', alignItems: 'center', width: '100%', maxWidth: '480px' }}>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center' }}>
              📄 Hinglish Code (.hin)
            </div>
            <div style={{ color: 'var(--text-muted)' }}>↓</div>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center' }}>
              🔍 Lexer / Tokens (Words pehchanna)
            </div>
            <div style={{ color: 'var(--text-muted)' }}>↓</div>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center' }}>
              🌳 Parser & AST (Grammar structure)
            </div>
            <div style={{ color: 'var(--text-muted)' }}>↓</div>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center' }}>
              ⚙️ Compiler (Python 3 code generation)
            </div>
            <div style={{ color: 'var(--text-muted)' }}>↓</div>
            <div className="apple-pill" style={{ fontSize: '0.9rem', padding: '0.45rem 1.2rem', width: '100%', justifyContent: 'center', background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', borderColor: 'rgba(16, 185, 129, 0.3)' }}>
              ⚡ CPython Engine (Direct Fast Execution)
            </div>
          </div>
        </div>
      </section>

      {/* No Custom VM Explanation */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Hinglish Koi Alag VM Nahi Hai</h2>
        <div className="apple-card">
          <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, fontSize: '0.95rem', marginBottom: '1rem' }}>
            Hinglish koi alag custom virtual machine ya slow interpreter nahi banata. 
            Aapka Hinglish code ek clean, typed compiler ke zariye standard <strong>Python 3</strong> mein convert hota hai 
            aur seedhe Python runtime par fast execute hota hai.
          </p>
          <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, fontSize: '0.95rem' }}>
            Iska sabse bada faayda yeh hai ki Python ki koi bhi library (jaise <code>math</code>, <code>json</code>, 
            <code>asyncio</code>, <code>datetime</code>) aap bina kisi delay ya extra setup ke seedha use kar sakte hain.
          </p>
        </div>
      </section>

      {/* Supported Features & Limitations */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Supported Features aur Limitations</h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', marginBottom: '0.75rem', fontWeight: 600 }}>
              <CheckCircle2 size={18} />
              <span>Kya-Kya Supported Hai?</span>
            </div>
            <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.8 }}>
              <li>Variables, Data Types, Math Operators</li>
              <li>If-Else (agar, warna_agar, warna)</li>
              <li>Loops (jabtak, har ... mein, ruko, aage_bado)</li>
              <li>Functions (kaam, *args, **kwargs, default values)</li>
              <li>Lambdas (sookshm) aur Decorators (@)</li>
              <li>Classes & OOP (varg, khood, methods)</li>
              <li>Error Handling (koshish, pakdo, antatah, uthav)</li>
              <li>Files & Context Managers (saath, khol)</li>
              <li>Generators aur yield (upaj)</li>
              <li>Async/await (asamanantar, intezaar)</li>
              <li>Pattern Matching (milao, sthiti)</li>
              <li>Type annotations aur Walrus operator (:=)</li>
            </ul>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b', marginBottom: '0.75rem', fontWeight: 600 }}>
              <AlertTriangle size={18} />
              <span>Dhyan Rakhne Wali Baatein</span>
            </div>
            <ul style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.8 }}>
              <li>
                <strong>Python Version:</strong> Python 3.10 ya usse upar ka version zaroori hai kyunki pattern matching (<code>milao/sthiti</code>) Python 3.10 engine par chalta hai.
              </li>
              <li>
                <strong>PEP 695 Generics:</strong> Python 3.12 ka <code>type Alias[T] = ...</code> syntax abhi Hinglish grammar mein nahi hai, par standard annotations (<code>x: int = 10</code>) poori tarah chalte hain.
              </li>
              <li>
                <strong>Execution Engine:</strong> Code CPython par hi run hota hai, isliye performance Python ke barabar hi fast rehti hai.
              </li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  );
};
