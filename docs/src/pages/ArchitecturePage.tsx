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
        <h2 className="section-title">Hinglish Ke 10 Core Modules (v1.1.0 Architecture)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Hinglish codebase zero external runtime dependencies ke saath 10 clean, modular components mein structured hai:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">1. hinglish.keywords</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Keywords & Built-in Registry</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Ek central dictionary jahan sabhi Hinglish shabdon ka Python equivalent mapped rehta hai, including v1.1 bilingual aliases (<code>lambai</code>, <code>ginti</code>, <code>jod</code>, <code>sab</code>, <code>koi</code>).
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">2. hinglish.lexer</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Lexer (Words & Indentation)</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Aapke text code ko padh kar tokens banata hai aur 4-spaces indentation (<code>INDENT</code> / <code>DEDENT</code>) track karta hai. Har token par line number aur column offset store rehta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">3. hinglish.parser & ast</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Parser & Typed AST Tree</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Tokens ko check karke syntax grammar verify karta hai aur code ka ek structured typed tree (AST) banata hai. Ismein inline ternary expressions aur comprehension error recovery bhi shamil hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">4. hinglish.compiler</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Compiler & Transpiler</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Hinglish AST tree ko clean, standard Python 3 source code mein convert karta hai. Source mapping ke zariye runtime errors seedha original <code>.hin</code> source line par point karte hain.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">5. hinglish.runtime</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Runtime & Import Hook</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Standard Python ke <code>compile()</code> aur <code>exec()</code> se code execute karta hai. Ismein custom import hook hai jo <code>.hin</code> files ko seamlessly import karne deta hai bina path issues ke.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">6. hinglish.formatter</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>AST-Aware Source Formatter</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Code formatting tool jo comments aur strings ko safely preserve karte hue idempotent 4-space formatting aur recursive directory formatting provide karta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">7. hinglish.linter</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Static Analysis & Diagnostics</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              AST aur scope inspection se unreferenced variables, unreachable code, aur syntax mistakes ko bina code execute kiye turant catch karta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">8. hinglish.lsp</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Language Server Protocol (LSP)</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Modern IDEs (VS Code) ke liye background JSON-RPC daemon jo live auto-complete, hover documentation, syntax squiggles aur document symbols serve karta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">9. hinglish.dap</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Debug Adapter Protocol (DAP)</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Interactive debugger engine jo source breakpoints, variable inspection, step-over/step-into aur call stack mapping provide karta hai seedha <code>.hin</code> files ke liye.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '0.5rem' }}>
              <span className="apple-pill">10. hinglish.cli</span>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Terminal CLI Driver</h3>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Command line interface jo run, transpile, tokens, ast, repl, format, lint, lsp, aur dap subcommands ko handle karta hai, safe exit codes aur recursive directory support ke sath.
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
