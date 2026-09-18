import React from 'react';

export const ArchitecturePage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Technical Deep Dive</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>System Sanrachna (Architecture)</h1>
        <p className="hero-subtitle">
          Hinglish v1.0.0 ke internal modules, pipeline layers, aur execution mechanics.
        </p>
      </div>

      {/* Module Overview */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Architectural Layers</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Hinglish codebase ek modular, decoupled design follow karta hai jismein har module ki apni ek spasht zimmedari hai:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">1. hinglish.keywords</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Vocabulary Single Source of Truth</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Centralized registry jo Hinglish tokens aur Python keywords ke beech mapping maintain karti hai. 
              Isse dialect variations ya naye aliases add karne ke liye lexer ya parser core code ko chhedne ki zaroorat nahi padti.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">2. hinglish.lexer</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Deterministic Tokenizer & Indentation Tracker</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              UTF-8 encoded text ko tokenize karta hai. Yeh indentation stack manage karta hai aur Python-style 
              <code>INDENT</code>, <code>DEDENT</code>, aur <code>NEWLINE</code> tokens emit karta hai. 
              Har token par line number aur column coordinate store hota hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">3. hinglish.parser & ast</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Recursive Descent Parser & Typed AST</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Tokens stream ko consume karke strongly typed, immutable Hinglish AST banata hai. 
              Statements aur expressions ke grammar rules yahan enforce hote hain.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">4. hinglish.compiler</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>AST Lowering & Python Source Generator</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Hinglish AST nodes ko traverse karke canonical Python 3 source code generate karta hai. 
              Ismein source mapping metadata attach hota hai taaki exceptions wapas original <code>.hin</code> line par point kar sakein.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">5. hinglish.runtime</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Native Execution Engine & Importer Hook</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              CPython <code>compile()</code> aur <code>exec()</code> machinery ka upyog karta hai. 
              Ismein <code>HinglishFinder</code> aur <code>HinglishLoader</code> meta-path hooks hain jo Python ke standard <code>import</code> mechanism ko <code>.hin</code> files dhundhne aur load karne ki kshamta dete hain.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">6. hinglish.cli</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Command-Line Interface & REPL</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Standard entrypoint jo arguments parse karta hai, subcommands dispatch karta hai, 
              stdin streams ko buffer karta hai, aur safe exit codes return karta hai.
            </p>
          </div>
        </div>
      </section>

      {/* Import Mechanics */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Native .hin Module Import Kriya (Mechanics)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.6 }}>
          Python ke <code>sys.meta_path</code> par Hinglish custom finder hook install karta hai. 
          Jab code mein <code>laao my_module</code> likha jata hai:
        </p>

        <div className="apple-card" style={{ background: 'var(--bg-secondary)' }}>
          <ol style={{ paddingLeft: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.8 }}>
            <li>Python meta-path par <code>HinglishFinder</code> check karta hai ki kya <code>my_module.hin</code> file exist karti hai.</li>
            <li>Agar file milti hai, toh <code>HinglishLoader</code> us file ko Hinglish pipeline se transpile karke bytecode compile karta hai.</li>
            <li>Bytecode ko standard Python module object mein execute kiya jata hai aur <code>sys.modules</code> mein cache kar liya jata hai.</li>
            <li>Agli baar import hone par seedha memory cache se fetch hota hai — zero extra overhead!</li>
          </ol>
        </div>
      </section>
    </div>
  );
};
