import React from 'react';
import { ShieldCheck } from 'lucide-react';

export const PhilosophyPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Design Principles</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Design Vichardhara (Philosophy)</h1>
        <p className="hero-subtitle">
          Hinglish language ka takneeki lakshya, aadharbhut vichar, aur design seemayein.
        </p>
      </div>

      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Hinglish Kyun Banayi Gayi? (Core Purpose)</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.96rem', lineHeight: 1.8, marginBottom: '1.25rem' }}>
          Computer programming mein computational logic aur algorithms bhasha-nirpeksh (language-agnostic) hote hain. 
          Lekin aamtaur par programming languages ke keywords keval Angrezi (English) shabdon tak seemit rahe hain.
        </p>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.96rem', lineHeight: 1.8, marginBottom: '1.25rem' }}>
          Hinglish ka core technical uddeshya yeh parakhna hai ki kya familiar Hindi/Hinglish vocabulary 
          (jaise <code>agar</code>, <code>warna</code>, <code>kaam</code>, <code>jabtak</code>, <code>har</code>) 
          ke madhyam se programming syntax ko adhik swabhavik aur approachable banaya ja sakta hai — 
          <strong>bina Python ke shaktishali execution ecosystem ko badle</strong>.
        </p>
      </section>

      {/* 3 Core Pillars */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Teen Mukhya Siddhant (Three Core Pillars)</h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.5rem', marginTop: '1.25rem' }}>
          <div className="apple-card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              1. Syntax aur Semantics Ka Alagav
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Hinglish keval syntax representation layer pradan karta hai. 
              Computational semantics, object model, aur memory model poori tarah se Python 3 par aadharit rehte hain.
            </p>
          </div>

          <div className="apple-card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              2. Bridge, Not an Island
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Ek alag aur alag-thalag language banana jiska koi ecosystem na ho, developers ke liye simit upyogi hota hai. 
              Hinglish ek seamless bridge ka kaam karta hai jismein standard Python libraries direct import ki ja sakti hain.
            </p>
          </div>

          <div className="apple-card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              3. Deterministic Compiler Engineering
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Koi regex replace ya heuristics nahi. Ek formal lexer, predictive recursive descent parser, 
              aur structured AST generator code ko transparent aur reproducible banate hain.
            </p>
          </div>
        </div>
      </section>

      {/* Realistic Scope */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Takneeki Seema (Technical Bounds)</h2>
        <div className="apple-callout">
          <ShieldCheck size={20} style={{ color: 'var(--accent-color)', flexShrink: 0, marginTop: '2px' }} />
          <div style={{ fontSize: '0.92rem', color: 'var(--text-secondary)', lineHeight: 1.7 }}>
            Ham koi atishayokti ya kranti ka dawa nahi karte. Hinglish ka prayas programming education 
            aur linguistic interface accessibility ko badhana hai, jabki standard Python runtime engineering ke 
            karyashaili ko preserve rakha gaya hai.
          </div>
        </div>
      </section>
    </div>
  );
};
