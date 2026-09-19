import React from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { ShieldCheck, AlertCircle, AlertTriangle, Info, Terminal, FileCode2, Cpu, CheckCircle2 } from 'lucide-react';

export const LinterPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Developer Tools</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Hinglish Linter & Static Analysis</h1>
        <p className="hero-subtitle">
          Code execute hone se pehle hi bugs, unreferenced variables, unreachable statements aur syntax issues ko detect karne wala high-speed AST static analyzer.
        </p>
      </div>

      {/* Feature Pillars */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Static Analysis Kyun Zaroori Hai?</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Hinglish Linter program ko run kiye bina uske <strong>Abstract Syntax Tree (AST) aur Lexical Scopes</strong> ka deep analysis karta hai. Yeh dynamic runtime errors ko development time par hi catch kar leta hai.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#ef4444', marginBottom: '0.75rem', fontWeight: 600 }}>
              <AlertCircle size={20} />
              <span>Zero False Positives</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Python ke dynamic semantics ko dhyan mein rakhte hue sirf high-confidence problems par diagnostics trigger karta hai taaki developer ka focus disturb na ho.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', marginBottom: '0.75rem', fontWeight: 600 }}>
              <ShieldCheck size={20} />
              <span>Deterministic & Pure Python</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Standard library par built, zero external dependencies (<code>dependencies = []</code>). Har run par consistent aur sorted diagnostics generate karta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#3b82f6', marginBottom: '0.75rem', fontWeight: 600 }}>
              <Cpu size={20} />
              <span>Full Scope Awareness</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Modules, functions, classes, closures, comprehensions, lambdas, <code>sarvavyapi</code> (globals), aur <code>asthanik</code> (nonlocals) ko accurately model karta hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b', marginBottom: '0.75rem', fontWeight: 600 }}>
              <FileCode2 size={20} />
              <span>Live LSP & VS Code Support</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              VS Code ke Problems view aur inline squiggles mein live errors aur warnings show karta hai language server protocol ke through.
            </p>
          </div>
        </div>
      </section>

      {/* Rules Catalog */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Static Analysis Rules Catalog</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Hinglish Linter mein implemented standard diagnostic rules:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* H001 */}
          <div className="apple-card" style={{ borderLeft: '4px solid #ef4444' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontFamily: 'monospace', fontWeight: 700, color: '#ef4444' }}>H001</span>
                <span style={{ fontWeight: 600, fontSize: '1.05rem' }}>Undefined Name</span>
              </div>
              <span className="apple-badge" style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', color: '#ef4444' }}>Error</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem', lineHeight: 1.7 }}>
              Aise variable ya function name ka use jo current scope, outer scopes, module, ya builtins mein define nahi hai.
            </p>
            <CodeBlock language="hinglish" code={`# ❌ H001: 'naam' defined nahi hai
dikhao(naam)

# ✅ Correct: pehle define karein
naam = "Aarav"
dikhao(naam)`} />
          </div>

          {/* H002 */}
          <div className="apple-card" style={{ borderLeft: '4px solid #f59e0b' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontFamily: 'monospace', fontWeight: 700, color: '#f59e0b' }}>H002</span>
                <span style={{ fontWeight: 600, fontSize: '1.05rem' }}>Unused Variable</span>
              </div>
              <span className="apple-badge" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' }}>Warning</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem', lineHeight: 1.7 }}>
              Function ke andar assign kiya gaya local variable jo kabhi dubara read nahi hua. Underscore (<code>_</code> ya <code>_var</code>) wale names ko ignore kiya jata hai.
            </p>
            <CodeBlock language="hinglish" code={`kaam hisab():
    # ⚠️ H002: 'vyarth_var' assign hua par use nahi hua
    vyarth_var = 100
    kul = 500
    wapas kul`} />
          </div>

          {/* H003 */}
          <div className="apple-card" style={{ borderLeft: '4px solid #f59e0b' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontFamily: 'monospace', fontWeight: 700, color: '#f59e0b' }}>H003</span>
                <span style={{ fontWeight: 600, fontSize: '1.05rem' }}>Unused Import</span>
              </div>
              <span className="apple-badge" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' }}>Warning</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem', lineHeight: 1.7 }}>
              <code>laao</code> ya <code>se ... laao</code> se import kiya gaya symbol jo pure module mein kahin use nahi ho raha.
            </p>
            <CodeBlock language="hinglish" code={`# ⚠️ H003: 'math' import hua par use nahi hua
laao math

dikhao("Namaste Duniya!")`} />
          </div>

          {/* H004 */}
          <div className="apple-card" style={{ borderLeft: '4px solid #f59e0b' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontFamily: 'monospace', fontWeight: 700, color: '#f59e0b' }}>H004</span>
                <span style={{ fontWeight: 600, fontSize: '1.05rem' }}>Duplicate Definition</span>
              </div>
              <span className="apple-badge" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' }}>Warning</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem', lineHeight: 1.7 }}>
              Same scope ke andar do functions ya classes ka same name se define hona.
            </p>
            <CodeBlock language="hinglish" code={`kaam greet():
    dikhao("Pehla")

# ⚠️ H004: 'greet' dobara define hua
kaam greet():
    dikhao("Dusra")`} />
          </div>

          {/* H005 */}
          <div className="apple-card" style={{ borderLeft: '4px solid #f59e0b' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontFamily: 'monospace', fontWeight: 700, color: '#f59e0b' }}>H005</span>
                <span style={{ fontWeight: 600, fontSize: '1.05rem' }}>Unreachable Code</span>
              </div>
              <span className="apple-badge" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' }}>Warning</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem', lineHeight: 1.7 }}>
              Unconditional terminators jaise <code>wapas</code>, <code>uthav</code>, <code>ruko</code>, ya <code>aage_bado</code> ke baad likhe statements jo kabhi execute nahi honge.
            </p>
            <CodeBlock language="hinglish" code={`kaam process():
    wapas 10
    # ⚠️ H005: 'wapas' ke baad unreachable code
    dikhao("Yeh line kabhi nahi chalegi")`} />
          </div>

          {/* H006 */}
          <div className="apple-card" style={{ borderLeft: '4px solid #f59e0b' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontFamily: 'monospace', fontWeight: 700, color: '#f59e0b' }}>H006</span>
                <span style={{ fontWeight: 600, fontSize: '1.05rem' }}>Constant Condition</span>
              </div>
              <span className="apple-badge" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' }}>Warning</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem', lineHeight: 1.7 }}>
              <code>agar</code>, <code>warna_agar</code> ya <code>jabtak</code> mein trivially constant conditions (jaise <code>sahi</code>, <code>galat</code>, <code>0</code>, <code>kuch_nahi</code>).
            </p>
            <CodeBlock language="hinglish" code={`# ⚠️ H006: Constant condition 'sahi'
agar sahi:
    dikhao("Always true")`} />
          </div>

          {/* H007 */}
          <div className="apple-card" style={{ borderLeft: '4px solid #3b82f6' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontFamily: 'monospace', fontWeight: 700, color: '#3b82f6' }}>H007</span>
                <span style={{ fontWeight: 600, fontSize: '1.05rem' }}>Shadowed Name</span>
              </div>
              <span className="apple-badge" style={{ backgroundColor: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6' }}>Warning</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem', lineHeight: 1.7 }}>
              Function parameter ya local variable ka built-in function (jaise <code>dikhao</code>, <code>lambai</code>, <code>print</code>) ya outer function ko shadow karna.
            </p>
            <CodeBlock language="hinglish" code={`# ⚠️ H007: Parameter 'dikhao' built-in function ko shadow kar raha hai
kaam display_message(dikhao):
    dikhao("Test")`} />
          </div>
        </div>
      </section>

      {/* CLI Usage */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Command Line Usage (CLI)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Terminal mein <code>hinglish lint</code> command se single file, multiple files, ya CI/CD check run karein:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div>
            <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}>1. Single File Linting</div>
            <CodeBlock language="bash" code={`# Script lint karein
hinglish lint script.hin`} />
          </div>

          <div>
            <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}>2. Multiple Files Linting</div>
            <CodeBlock language="bash" code={`# Ek saath multiple files inspect karein
hinglish lint utils.hin models.hin app.hin`} />
          </div>

          <div>
            <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}>3. CI / CD Pipeline Check Mode</div>
            <CodeBlock language="bash" code={`# Agar koi bhi finding (warning ya error) aati hai to exit code 1 return karega
hinglish lint --check app.hin`} />
          </div>

          <div>
            <div style={{ fontWeight: 600, marginBottom: '0.5rem' }}>4. Standard Input (Piping)</div>
            <CodeBlock language="bash" code={`# Stdin se code pipe karein
cat script.hin | hinglish lint -`} />
          </div>
        </div>
      </section>

      {/* Exit Codes */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">CLI Exit Codes</h2>
        <div className="apple-card" style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-primary)' }}>
                <th style={{ padding: '0.75rem 1rem' }}>Exit Code</th>
                <th style={{ padding: '0.75rem 1rem' }}>Meaning</th>
                <th style={{ padding: '0.75rem 1rem' }}>Standard Mode</th>
                <th style={{ padding: '0.75rem 1rem' }}><code>--check</code> Mode</th>
              </tr>
            </thead>
            <tbody style={{ color: 'var(--text-secondary)' }}>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '0.75rem 1rem', fontFamily: 'monospace', fontWeight: 600, color: '#10b981' }}>0</td>
                <td style={{ padding: '0.75rem 1rem' }}>Clean / Successful</td>
                <td style={{ padding: '0.75rem 1rem' }}>No error diagnostics (warnings permitted)</td>
                <td style={{ padding: '0.75rem 1rem' }}>Zero findings (no errors, no warnings)</td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '0.75rem 1rem', fontFamily: 'monospace', fontWeight: 600, color: '#ef4444' }}>1</td>
                <td style={{ padding: '0.75rem 1rem' }}>Lint Check Failure</td>
                <td style={{ padding: '0.75rem 1rem' }}>Any error-level finding or syntax error</td>
                <td style={{ padding: '0.75rem 1rem' }}>Any warning or error finding detected</td>
              </tr>
              <tr>
                <td style={{ padding: '0.75rem 1rem', fontFamily: 'monospace', fontWeight: 600, color: '#f59e0b' }}>2</td>
                <td style={{ padding: '0.75rem 1rem' }}>CLI Usage Error</td>
                <td style={{ padding: '0.75rem 1rem' }}>Missing file argument ya non-existent file</td>
                <td style={{ padding: '0.75rem 1rem' }}>Missing file argument ya non-existent file</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Python Public API */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Python Public API</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Agar aap Hinglish linter ko apne custom tooling, test framework, ya scripts mein integrate karna chahte hain:
        </p>

        <CodeBlock language="python" code={`from hinglish import lint_source

code = """
kaam test():
    age = 21
    dikhao("Namaste")
"""

diagnostics = lint_source(code, filename="test.hin")

for diag in diagnostics:
    print(diag.format_cli())
    # Output: test.hin:3:5: warning H002: variable 'age' is assigned but never used`} />
      </section>
    </div>
  );
};
