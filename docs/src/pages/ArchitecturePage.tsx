import React from 'react';

export const ArchitecturePage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Under The Hood</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Kaise Kaam Karta Hai? (Architecture)</h1>
        <p className="hero-subtitle">
          Hinglish compiler ke internal parts, modules aur execution process ko aasan bhasha mein samjhein.
        </p>
      </div>

      {/* Module Overview */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Hinglish Ke 6 Main Modules</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Hinglish codebase bohot clean aur modular tarike se likha gaya hai:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">1. hinglish.keywords</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Keywords Ki List</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Ek central dictionary jahan sabhi Hinglish shabdon ka Python equivalent mapped rehta hai. 
              Isse naye bolchal ke aliases add karna bohot aasan ho jata hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">2. hinglish.lexer</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Lexer (Words Pehchanna)</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Aapke text code ko padh kar tokens banata hai aur 4-spaces indentation (INDENT / DEDENT) track karta hai. 
              Har token par line number aur column offset store rehta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">3. hinglish.parser & ast</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Parser & AST Tree</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Tokens ko check karke syntax grammar verify karta hai aur code ka ek structured typed tree (AST) banata hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">4. hinglish.compiler</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Compiler</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Hinglish AST tree ko clean, standard Python 3 source code mein convert karta hai. 
              Ismein source mapping bhi hoti hai taaki error aane par original .hin file ki line dikhe.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">5. hinglish.runtime</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Runtime & Import Hooks</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Standard Python ke <code>compile()</code> aur <code>exec()</code> se code execute karta hai. 
              Ismein custom import hook bhi hai jo .hin files ko direct import hone deta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">6. hinglish.cli</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Terminal CLI Engine</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Terminal commands (run, transpile, tokens, ast, repl) ko manage karta hai aur safe exit codes return karta hai.
            </p>
          </div>
        </div>
      </section>

      {/* Import Mechanics */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">.hin File Import Kaise Hoti Hai?</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.6 }}>
          Jab aap code mein likhte hain <code>laao my_utils</code>:
        </p>

        <div className="apple-card" style={{ background: 'var(--bg-secondary)' }}>
          <ol style={{ paddingLeft: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.8 }}>
            <li>Hinglish ka custom import hook check karta hai ki kya <code>my_utils.hin</code> file exist karti hai.</li>
            <li>File milne par use turant compile karke Python bytecode bana deta hai.</li>
            <li>Bytecode ko standard Python module ki tarah memory mein load karke cache kar leta hai.</li>
            <li>Agli baar import karne par seedha memory cache se mil jata hai — bilkul zero extra delay ke!</li>
          </ol>
        </div>
      </section>
    </div>
  );
};
