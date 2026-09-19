import React from 'react';
import { CodeBlock } from '../components/CodeBlock';
import { Bug, Play, StepForward, CornerDownRight, CornerUpLeft, ShieldAlert, CheckCircle2 } from 'lucide-react';

export const DebuggerPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Developer Tools</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Hinglish Debugger (DAP)</h1>
        <p className="hero-subtitle">
          VS Code ke andar Hinglish <code>.hin</code> files mein breakpoints set karein, variables inspect karein, aur step-by-step code execution trace karein.
        </p>
      </div>

      {/* Overview Cards */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Debugging Ka Mazedar Experience</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.7 }}>
          Hinglish v1.0 standard <strong>Debug Adapter Protocol (DAP)</strong> provide karta hai. Aapko generated Python code dekhne ki zarurat nahi padegi — saari line numbers, variables aur call stack directly Hinglish source code par map hoti hain.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#ef4444', marginBottom: '0.75rem', fontWeight: 600 }}>
              <Bug size={20} />
              <span>Source-Level Breakpoints</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Kisi bhi line ke left margin par click karke red breakpoint dot lagayein. Code wahi pause ho jayega.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', marginBottom: '0.75rem', fontWeight: 600 }}>
              <Play size={20} />
              <span>F5 Zero-Config Launch</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Bina kisi manual setup ke bas <code>F5</code> dabate hi active <code>.hin</code> file debug mode mein chal padti hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#3b82f6', marginBottom: '0.75rem', fontWeight: 600 }}>
              <StepForward size={20} />
              <span>Intuitive Stepping</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Step Over (<code>F10</code>), Step Into (<code>F11</code>), aur Step Out (<code>Shift+F11</code>) se functions aur loops mein ghoomein.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f59e0b', marginBottom: '0.75rem', fontWeight: 600 }}>
              <ShieldAlert size={20} />
              <span>Runtime Exception Catch</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
              Jab koi runtime error (e.g. division by zero) aati hai, toh debugger seedha error wali Hinglish line par pause ho jata hai.
            </p>
          </div>
        </div>
      </section>

      {/* Debug Controls Table */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">VS Code Debugging Controls</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
          Breakpoint par pause hone ke baad aap yeh standard keyboard shortcuts use kar sakte hain:
        </p>

        <div className="apple-card" style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-color)', textAlign: 'left' }}>
                <th style={{ padding: '0.75rem 1rem' }}>Action</th>
                <th style={{ padding: '0.75rem 1rem' }}>Shortcut</th>
                <th style={{ padding: '0.75rem 1rem' }}>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 600 }}>Continue</td>
                <td style={{ padding: '0.75rem 1rem' }}><code>F5</code></td>
                <td style={{ padding: '0.75rem 1rem', color: 'var(--text-secondary)' }}>Agle breakpoint ya program end tak execution chalayein</td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 600 }}>Step Over</td>
                <td style={{ padding: '0.75rem 1rem' }}><code>F10</code></td>
                <td style={{ padding: '0.75rem 1rem', color: 'var(--text-secondary)' }}>Agli statement execute karein bina functions ke andar ghuse</td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 600 }}>Step Into</td>
                <td style={{ padding: '0.75rem 1rem' }}><code>F11</code></td>
                <td style={{ padding: '0.75rem 1rem', color: 'var(--text-secondary)' }}>Function call ke andar jaakar step-by-step debug karein</td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 600 }}>Step Out</td>
                <td style={{ padding: '0.75rem 1rem' }}><code>Shift + F11</code></td>
                <td style={{ padding: '0.75rem 1rem', color: 'var(--text-secondary)' }}>Current function se bahar nikal kar caller frame mein aayein</td>
              </tr>
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 600 }}>Pause</td>
                <td style={{ padding: '0.75rem 1rem' }}><code>F6</code></td>
                <td style={{ padding: '0.75rem 1rem', color: 'var(--text-secondary)' }}>Chal rahe program ko turant kisi bhi line par rokein</td>
              </tr>
              <tr>
                <td style={{ padding: '0.75rem 1rem', fontWeight: 600 }}>Stop</td>
                <td style={{ padding: '0.75rem 1rem' }}><code>Shift + F5</code></td>
                <td style={{ padding: '0.75rem 1rem', color: 'var(--text-secondary)' }}>Debugging session ko safely band karein</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* launch.json configuration */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Custom Launch Configuration (launch.json)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.7 }}>
          Agar aap specific arguments pass karna chahte hain ya program entry point fix karna chahte hain, toh project ke <code>.vscode/launch.json</code> mein yeh configuration add karein:
        </p>

        <CodeBlock
          code={`{\n  "version": "0.2.0",\n  "configurations": [\n    {\n      "type": "hinglish",\n      "request": "launch",\n      "name": "Debug Hinglish File",\n      "program": "\${file}",\n      "stopOnEntry": false,\n      "args": []\n    }\n  ]\n}`}
          language="json"
          filename=".vscode/launch.json"
        />
      </section>

      {/* Multi-file Debugging */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Multi-File Debugging (Cross-File Breakpoints)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.7 }}>
          Jab aapka program doosri <code>.hin</code> files ko import karta hai (e.g. <code>se utils laao add</code>), toh aap <code>utils.hin</code> ke andar bhi breakpoint laga sakte hain. Jab <code>main.hin</code> us function ko call karega, debugger automatically <code>utils.hin</code> ke andar jump karke ruk jayega!
        </p>

        <div className="apple-card" style={{ background: 'var(--bg-secondary)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', fontWeight: 600, marginBottom: '0.5rem' }}>
            <CheckCircle2 size={18} />
            <span>Multi-File Import Support Verified</span>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', lineHeight: 1.7 }}>
            Call Stack panel mein sabhi active frames cleanly dikhte hain, jaise <code>add() in utils.hin:2</code> aur <code>(module) in main.hin:5</code>.
          </p>
        </div>
      </section>
    </div>
  );
};
