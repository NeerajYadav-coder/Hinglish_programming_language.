import React from 'react';
import { CodeBlock } from '../components/CodeBlock';

export const MultiFilePage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Project Structure</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Multi-File Projects (Badi Apps)</h1>
        <p className="hero-subtitle">
          Ek se zyada .hin files bana kar modular project kaise banayein aur aapas mein import karein.
        </p>
      </div>

      {/* Directory Structure */}
      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Recommended Folder Structure</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Jab aapka project bada ho, toh aap apne code ko alag-alag files mein divide kar sakte hain:
        </p>

        <div className="apple-card" style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '0.9rem', lineHeight: 1.8 }}>
          <div style={{ color: 'var(--accent-color)', fontWeight: 600, marginBottom: '0.5rem' }}>📁 mera_project/</div>
          <div style={{ paddingLeft: '1.25rem', color: 'var(--text-secondary)' }}>
            ├── 📄 main.hin &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: 'var(--text-muted)' }}># Main entrypoint jahan se program start hoga</span><br />
            ├── 📄 utils.hin &nbsp;&nbsp;&nbsp;&nbsp;<span style={{ color: 'var(--text-muted)' }}># Helper functions aur formatting</span><br />
            ├── 📄 models.hin &nbsp;&nbsp;&nbsp;<span style={{ color: 'var(--text-muted)' }}># Data classes (jaise varg User)</span><br />
            └── 📄 services.hin &nbsp;<span style={{ color: 'var(--text-muted)' }}># API aur business logic</span>
          </div>
        </div>
      </section>

      {/* Code Example Walkthrough */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Example: Files Aapas Mein Kaise Connect Karein?</h2>

        <h3 className="subsection-title">1. models.hin (Classes Wali File)</h3>
        <CodeBlock
          code={`# models.hin
varg User:
    kaam __init__(khood, naam, role):
        khood.naam = naam
        khood.role = role

    kaam is_admin(khood):
        wapas khood.role == "admin"`}
          language="hin"
          filename="models.hin"
        />

        <h3 className="subsection-title">2. utils.hin (Helper Functions Wali File)</h3>
        <CodeBlock
          code={`# utils.hin
kaam jod(a, b):
    wapas a + b

kaam format_msg(naam, msg):
    wapas f"[{naam}]: {msg}"`}
          language="hin"
          filename="utils.hin"
        />

        <h3 className="subsection-title">3. main.hin (Main Program Jo Sabko Chalaega)</h3>
        <CodeBlock
          code={`# main.hin
# Dusri .hin files ko import karein
laao utils
se models laao User

# Standard Python library bhi direct import kar sakte hain
se datetime laao datetime

u = User("Aarav", "admin")
dikhao("Admin check:", u.is_admin())

total = utils.jod(100, 250)
dikhao(utils.format_msg(u.naam, f"Total prapt hua: {total}"))`}
          language="hin"
          filename="main.hin"
        />
      </section>

      {/* Working Directory Independence */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Kahin Se Bhi Run Karo (No Path Issues)</h2>
        <div className="apple-card" style={{ background: 'var(--bg-secondary)' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '0.5rem' }}>
            Automatic Path Resolution
          </h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', lineHeight: 1.6, marginBottom: '1rem' }}>
            Aap terminal mein chahe kisi bhi folder mein baithe hon, jab aap <code>main.hin</code> run karte hain, 
            toh Hinglish automatically uske aas-paas ki sibling <code>.hin</code> files ko dhoondh leta hai:
          </p>
          <CodeBlock
            code={`# Project folder ke bahar se bhi chala sakte hain
cd ~
hinglish /path/to/mera_project/main.hin
# utils.hin aur models.hin apne aap load ho jayengi!`}
            language="bash"
            filename="terminal"
          />
        </div>
      </section>

      {/* Multi-file Tracebacks */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Clear Multi-File Error Messages</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
          Agar kisi imported file ke andar koi error aati hai, toh Hinglish accurate file name 
          aur original line number ke sath saaf error dikhata hai:
        </p>

        <CodeBlock
          code={`Hinglish Traceback (sabse aakhiri call pehle):
  File "main.hin", line 8, in <module>
    res = utils.divide(10, 0)
  File "utils.hin", line 3, in divide
    wapas a / b
ZeroDivisionError: division by zero`}
          language="text"
          filename="error-traceback"
        />
      </section>
    </div>
  );
};
