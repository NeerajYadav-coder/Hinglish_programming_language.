import React from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { AlertTriangle } from 'lucide-react';

export const CliPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Terminal Guide</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Terminal Commands (CLI Reference)</h1>
        <p className="hero-subtitle">
          Hinglish command-line tool ke sabhi commands, flags, pipes aur exit codes ki aasan guide.
        </p>
      </div>

      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Commands Reference</h2>
        <p className="section-subtitle">
          Aap subcommands bhi use kar sakte hain aur direct shorthand bhi — dono 100% chalte hain.
        </p>

        <div className="apple-table-container">
          <table className="apple-table">
            <thead>
              <tr>
                <th>Subcommand</th>
                <th>Short Syntax</th>
                <th>Kisko Kya Kaam Aata Hai?</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>hinglish run file.hin</code></td>
                <td><code>hinglish file.hin</code></td>
                <td>Hinglish script ko seedha compile aur execute (run) karta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish transpile file.hin</code></td>
                <td><code>hinglish --transpile file.hin</code></td>
                <td>Hinglish code ko Python 3 mein convert karke screen par dikhata hai.</td>
              </tr>
              <tr>
                <td><code>hinglish transpile file.hin -o out.py</code></td>
                <td>—</td>
                <td>Generated Python code ko ek nayi <code>.py</code> file mein save kar deta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish tokens file.hin</code></td>
                <td><code>hinglish --tokens file.hin</code></td>
                <td>Lexer dwara banaye gaye tokens ko line aur column ke sath print karta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish ast file.hin</code></td>
                <td><code>hinglish --ast file.hin</code></td>
                <td>Parser dwara banaya gaya Abstract Syntax Tree (AST) dikhata hai.</td>
              </tr>
              <tr>
                <td><code>hinglish repl</code></td>
                <td><code>hinglish</code> (bina file ke)</td>
                <td>Interactive REPL shell shuru karta hai jahan aap live code type kar sakte hain.</td>
              </tr>
              <tr>
                <td><code>hinglish format &lt;path&gt;</code></td>
                <td><code>hinglish --format &lt;path&gt;</code></td>
                <td>Source code ko canonical style mein format karta hai (single file ya recursive directory).</td>
              </tr>
              <tr>
                <td><code>hinglish format &lt;path&gt; --check</code></td>
                <td>—</td>
                <td>Check karta hai ki code formatted hai ya nahi bina modify kiye (exit code 0/1).</td>
              </tr>
              <tr>
                <td><code>hinglish lint &lt;path&gt;</code></td>
                <td><code>hinglish --lint &lt;path&gt;</code></td>
                <td>AST static analysis se unreferenced variables, syntax issues aur bugs detect karta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish lint &lt;path&gt; --check</code></td>
                <td>—</td>
                <td>CI/CD mode: agar koi warning ya error mile toh exit code 1 deta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish lsp</code></td>
                <td>—</td>
                <td>Language Server Protocol daemon start karta hai (VS Code editor integration).</td>
              </tr>
              <tr>
                <td><code>hinglish dap</code></td>
                <td>—</td>
                <td>Debug Adapter Protocol server start karta hai (step-by-step interactive debugging).</td>
              </tr>
              <tr>
                <td><code>hinglish --version</code></td>
                <td><code>hinglish -v</code></td>
                <td>Installed Hinglish package ka version (v1.1.0) check karne ke liye.</td>
              </tr>
              <tr>
                <td><code>hinglish --help</code></td>
                <td><code>hinglish -h</code></td>
                <td>Available commands aur options ki help list dekhne ke liye.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Recursive Directory Support (v1.1) */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Recursive Directory Processing (v1.1)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.7 }}>
          Hinglish v1.1 mein <code>format</code> aur <code>lint</code> commands folders ko recursively scan kar sakti hain. Aapko ek-ek file ka path dene ki zarurat nahi hai:
        </p>

        <CodeBlock
          code={`# Poore source folder ko ek command mein format karein
hinglish format src/ tests/

# Poore project ko recursively lint karein
hinglish lint .

# CI/CD pipeline mein zero findings verify karein
hinglish lint src/ --check`}
          language="bash"
          filename="terminal"
        />
      </section>

      {/* Stdin Pipelines */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Terminal Pipes (Standard Input)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Unix style pipes ke sath aap seedha command line se code pipe karke chala sakte hain:
        </p>

        <CodeBlock
          code={`# Pipe ke through file execute karein\ncat script.hin | hinglish\n\n# Dash (-) laga kar direct stdin se run karein\necho 'dikhao("Namaste Terminal!")' | hinglish -\n\n# Python code dekhne ke liye transpile pipe\necho 'x = 10; agar x > 5: dikhao(x)' | hinglish transpile -`}
          language="bash"
          filename="terminal"
        />
      </section>

      {/* Safety Mechanisms */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Safety Check (File Overwrite Protection)</h2>
        <div className="apple-callout warning">
          <AlertTriangle size={20} style={{ color: '#f59e0b', flexShrink: 0, marginTop: '2px' }} />
          <div>
            <strong>Original File Hamesha Safe Hai:</strong> Hinglish aapki original <code>.hin</code> source file ko kisi bhi haal mein overwrite nahi hone deta! 
            Agar aap galti se <code>hinglish transpile test.hin -o test.hin</code> likh bhi dein, toh compiler turant safe guard trigger karke error de deta hai taaki aapka code delete na ho.
          </div>
        </div>
      </section>

      {/* Exit Codes */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Exit Codes (Shell Scripts ke liye)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Bash scripts aur CI/CD pipelines ke liye standard exit codes:
        </p>

        <div className="apple-table-container">
          <table className="apple-table">
            <thead>
              <tr>
                <th>Code</th>
                <th>Status</th>
                <th>Matlab</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>0</code></td>
                <td><span className="apple-pill" style={{ background: 'rgba(16, 185, 129, 0.1)', color: '#10b981' }}>SUCCESS</span></td>
                <td>Program successfully chal gaya, ya version/help display hua, ya REPL se clean exit.</td>
              </tr>
              <tr>
                <td><code>1</code></td>
                <td><span className="apple-pill" style={{ background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444' }}>RUNTIME ERROR</span></td>
                <td>Syntax error, compiler error, runtime exception, file missing, ya overwrite protection alert.</td>
              </tr>
              <tr>
                <td><code>2</code></td>
                <td><span className="apple-pill" style={{ background: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' }}>USAGE ERROR</span></td>
                <td>Galat command flag ya argument ki kami.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
};
