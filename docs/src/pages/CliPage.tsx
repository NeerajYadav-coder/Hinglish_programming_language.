import React from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { AlertTriangle } from 'lucide-react';

export const CliPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Command-Line Tool</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>CLI Nirdeshika (CLI Reference)</h1>
        <p className="hero-subtitle">
          Hinglish CLI ke sabhi subcommands, flags, shorthands, stdin pipelines, aur exit codes ka poora vivran.
        </p>
      </div>

      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Subcommands Reference</h2>
        <p className="section-subtitle">
          Hinglish CLI explicit subcommands aur shorthand syntax dono ko 100% support karta hai.
        </p>

        <div className="apple-table-container">
          <table className="apple-table">
            <thead>
              <tr>
                <th>Subcommand</th>
                <th>Shorthand Syntax</th>
                <th>Vivran (Description)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>hinglish run file.hin</code></td>
                <td><code>hinglish file.hin</code></td>
                <td>Hinglish script ko seedha compile aur execute karta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish transpile file.hin</code></td>
                <td><code>hinglish --transpile file.hin</code></td>
                <td>Program ko compile karke Python 3 source code stdout par print karta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish transpile file.hin -o out.py</code></td>
                <td>—</td>
                <td>Generated Python code ko specify ki gayi output file mein surakshit save karta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish tokens file.hin</code></td>
                <td><code>hinglish --tokens file.hin</code></td>
                <td>Source code ke tokens ka sequential stream line/column ke sath display karta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish ast file.hin</code></td>
                <td><code>hinglish --ast file.hin</code></td>
                <td>Parser dwara construct kiya gaya Abstract Syntax Tree (AST) tree view mein dikhata hai.</td>
              </tr>
              <tr>
                <td><code>hinglish repl</code></td>
                <td><code>hinglish</code> (bina arguments)</td>
                <td>Interactive REPL session shuru karta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish --version</code></td>
                <td><code>hinglish -v</code></td>
                <td>Installed Hinglish package version (v1.0.0) display karta hai.</td>
              </tr>
              <tr>
                <td><code>hinglish --help</code></td>
                <td><code>hinglish -h</code></td>
                <td>CLI usage manual aur available options display karta hai.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Stdin Pipelines */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Standard Input (Stdin Pipelines)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Hinglish Unix philosophy ko follow karta hai aur seedha pipe ya redirection se code execute kar sakta hai:
        </p>

        <CodeBlock
          code={`# Pipe ke madhyam se script execute karein\ncat script.hin | hinglish\n\n# Dash (-) argument se explicit stdin reading\necho 'dikhao("Namaste Terminal!")' | hinglish -\n\n# Python source dekhne ke liye pipe\necho 'x = 10; agar x > 5: dikhao(x)' | hinglish transpile -`}
          language="bash"
          filename="terminal"
        />
      </section>

      {/* Safety Mechanisms */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Suraksha Niyam (Safety Controls)</h2>
        <div className="apple-callout warning">
          <AlertTriangle size={20} style={{ color: '#f59e0b', flexShrink: 0, marginTop: '2px' }} />
          <div>
            <strong>Source Overwrite Suraksha:</strong> Hinglish aapke original <code>.hin</code> source file ko kisi bhi haal mein overwrite nahi hone deta! 
            Agar aap galti se <code>hinglish transpile test.hin -o test.hin</code> likhenge, toh compiler turant safe guard trigger karke error de dega aur file corrupt nahi hogi.
          </div>
        </div>
      </section>

      {/* Exit Codes */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Exit Codes Reference</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          CI/CD pipelines aur shell scripts ke liye standardized exit codes:
        </p>

        <div className="apple-table-container">
          <table className="apple-table">
            <thead>
              <tr>
                <th>Code</th>
                <th>Status</th>
                <th>Arth (Meaning)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><code>0</code></td>
                <td><span className="apple-pill" style={{ background: 'rgba(16, 185, 129, 0.1)', color: '#10b981' }}>SUCCESS</span></td>
                <td>Karyakram safaltapoorvak execute hua, version/help display hua, ya REPL se clean exit.</td>
              </tr>
              <tr>
                <td><code>1</code></td>
                <td><span className="apple-pill" style={{ background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444' }}>RUNTIME ERROR</span></td>
                <td>Syntax error, compiler error, runtime exception, file not found, ya overwrite safety violation.</td>
              </tr>
              <tr>
                <td><code>2</code></td>
                <td><span className="apple-pill" style={{ background: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' }}>CLI USAGE ERROR</span></td>
                <td>Galat flags, command arguments ki kami, ya anjaan subcommand.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
};
