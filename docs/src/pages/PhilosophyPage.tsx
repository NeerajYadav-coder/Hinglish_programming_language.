import React from 'react';
import { ShieldCheck } from 'lucide-react';

export const PhilosophyPage: React.FC = () => {
  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Design Philosophy</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Hinglish Kyun Banayi Gayi?</h1>
        <p className="hero-subtitle">
          Hinglish language ko banane ke piche kya soch hai aur iska kya goal hai.
        </p>
      </div>

      <section style={{ margin: '2rem 0' }}>
        <h2 className="section-title">Hinglish Ka Main Goal</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.96rem', lineHeight: 1.8, marginBottom: '1.25rem' }}>
          Coding seekhte waqt logic aur problem solving sabse zaroori cheez hoti hai. 
          Lekin shuruat mein English syntax aur keywords ki wajah se bohot se logon ko coding thodi mushkil lagne lagti hai.
        </p>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.96rem', lineHeight: 1.8, marginBottom: '1.25rem' }}>
          Hinglish ka simple goal yeh hai ki kya hum aam bolchal ke Hinglish shabdon 
          (jaise <code>agar</code>, <code>warna</code>, <code>kaam</code>, <code>jabtak</code>, <code>har</code>) 
          se code likh sakte hain — <strong>bina Python ke powerful ecosystem aur speed ko kho-e</strong>.
        </p>
      </section>

      {/* 3 Core Pillars */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">3 Simple Principles</h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.5rem', marginTop: '1.25rem' }}>
          <div className="apple-card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              1. Aasan Syntax, Real Python
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Aap code aasan Hinglish mein likhein, lekin background mein poori computational semantics aur memory standard Python 3 ki hi rehti hai.
            </p>
          </div>

          <div className="apple-card">
            <div style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              2. Bridge, Not an Island
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Ek nayi aisi language banana jismein koi library na chale, kisi kaam ka nahi hota. Hinglish ek bridge hai jismein Python ki saari libraries direct import hoti hain.
            </p>
          </div>

          <div className="apple-card">
            <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
              3. Clean Real Compiler
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>
              Koi guessing, AI ya simple string replace nahi hai. Ek real typed compiler aapke code ko deterministically standard Python mein convert karta hai.
            </p>
          </div>
        </div>
      </section>

      {/* Realistic Scope */}
      <section style={{ margin: '3rem 0' }}>
        <h2 className="section-title">Hamari Soch</h2>
        <div className="apple-callout">
          <ShieldCheck size={20} style={{ color: 'var(--accent-color)', flexShrink: 0, marginTop: '2px' }} />
          <div style={{ fontSize: '0.92rem', color: 'var(--text-secondary)', lineHeight: 1.7 }}>
            Hamara lakshya coding education aur syntax accessibility ko simple banana hai, 
            taaki koi bhi insaan bina kisi bhasha ki rukawat ke coding ke logic ko aasani se samajh sake.
          </div>
        </div>
      </section>
    </div>
  );
};
