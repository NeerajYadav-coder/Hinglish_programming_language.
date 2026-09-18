import React from 'react';
import { CodeBlock } from '../components/CodeBlock';


export const MultiFilePage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Modular Architecture</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Bahu-File (Multi-File) Projects</h1>
        <p className="hero-subtitle">
          Hinglish v1.0.0 mein real-world modular codebases, sibling imports, aur source-mapped multi-file tracebacks.
        </p>
      </div>

      {/* Directory Structure */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Anukoolit Project Structure (Recommended Layout)</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Hinglish mein aap apne program ko alag-alag logical modules mein baant sakte hain:
        </p>

        <div className="apple-card" style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.9rem', lineHeight: 1.8 }}>
          <div style={{ color: 'var(--accent-color)', fontWeight: 600, marginBottom: '0.5rem' }}>📁 mera_project/</div>
          <div style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)' }}>
            ├── 📄 main.hin &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: 'var(--text-muted)' }}># Entrypoint (Mukhya file jahan se shuru hoga)</span><br />
            ├── 📄 utils.hin &nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: 'var(--text-muted)' }}># Utility helpers, ganit aur formatters</span><br />
            ├── 📄 models.hin &nbsp;&nbsp;&nbsp;<span style={{ color: 'var(--text-muted)' }}># Data classes (varg Khata, varg User)</span><br />
            └── 📄 services.hin &nbsp;<span style={{ color: 'var(--text-muted)' }}># Business logic aur API / DB service layer</span>
          </div>
        </div>
      </section>

      {/* Code Example Walkthrough */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Step-by-Step Code Walkthrough</h2>

        <h3 className="subsection-title">1. models.hin</h3>
        <CodeBlock
          code={`# models.hin
varg Upayogakarta:
    kaam __init__(khood, naam, bhumika):
        khood.naam = naam
        khood.bhumika = bhumika

    kaam is_admin(khood):
        wapas khood.bhumika == "admin"`}
          language="hin"
          filename="models.hin"
        />

        <h3 className="subsection-title">2. utils.hin</h3>
        <CodeBlock
          code={`# utils.hin
kaam jod(a, b):
    wapas a + b

kaam sandesh_sajao(naam, sandesh):
    wapas f"[{naam}]: {sandesh}"`}
          language="hin"
          filename="utils.hin"
        />

        <h3 className="subsection-title">3. main.hin (Entrypoint)</h3>
        <CodeBlock
          code={`# main.hin
# Sibling .hin modules import karein
laao utils
se models laao Upayogakarta

# Python standard library modules bhi transparently import ho sakte hain
se datetime laao datetime

u = Upayogakarta("Aarav", "admin")
dikhao("Admin check:", u.is_admin())

natija = utils.jod(100, 250)
dikhao(utils.sandesh_sajao(u.naam, f"Kul jod prapt hua: {natija}"))`}
          language="hin"
          filename="main.hin"
        />
      </section>

      {/* Working Directory Independence */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Working Directory Independence</h2>
        <div className="apple-card" style={{ background: 'var(--bg-secondary)' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.5rem' }}>
            Kahin se bhi execute karein
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', lineHeight: 1.6, marginBottom: '1rem' }}>
            Hinglish runtime entrypoint script ke folder ko automatically <code>sys.path[0]</code> par anchor karta hai. 
            Iska arth yeh hai ki chahe aap terminal mein kisi bhi directory mein baithe hon, relative .hin imports bina kisi issue ke resolve hote hain:
          </p>
          <CodeBlock
            code={`# Project directory ke bahar se chalayein
cd /home/user
hinglish /path/to/mera_project/main.hin
# Sibling files (utils.hin, models.hin) turant load hongi!`}
            language="bash"
            filename="terminal"
          />
        </div>
      </section>

      {/* Multi-file Tracebacks */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Source-Mapped Multi-File Tracebacks</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Jab kisi imported <code>.hin</code> module ke andar runtime exception aati hai, 
          toh Hinglish Python traceback ko translate karke accurate <code>.hin</code> file name, 
          exact line number aur original Hinglish code snippet screen par render karta hai:
        </p>

        <CodeBlock
          code={`Hinglish Traceback (sabse aakhiri call pehle):
  File "main.hin", line 8, in <module>
    res = utils.bhaag_karo(10, 0)
  File "utils.hin", line 3, in bhaag_karo
    wapas a / b
ZeroDivisionError: division by zero`}
          language="text"
          filename="error-traceback"
        />
      </section>
    </div>
  );
};
