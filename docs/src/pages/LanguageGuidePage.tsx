import React, { useState } from 'react';
import { CodeBlock } from '../components/CodeBlock';


export const LanguageGuidePage: React.FC = () => {
  const [activeSection, setActiveSection] = useState('basics');

  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Bhasha Nirdeshika</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Hinglish Language Guide</h1>
        <p className="hero-subtitle">
          Hinglish v1.0.0 ke sabhi bhasha niyam, syntax, keywords, aur constructs ka poora vivran.
        </p>
      </div>

      {/* Apple-style Segmented Sub-navigation pills */}
      <div
        style={{
          display: 'flex',
          gap: '0.5rem',
          overflowX: 'auto',
          paddingBottom: '0.75rem',
          marginBottom: '2.5rem',
          borderBottom: '1px solid var(--border-color)'
        }}
      >
        {[
          { id: 'basics', label: 'Buniyadi (Basics)' },
          { id: 'control-flow', label: 'Control Flow' },
          { id: 'functions', label: 'Functions (Kaam)' },
          { id: 'collections', label: 'Collections' },
          { id: 'oop', label: 'OOP (Varg)' },
          { id: 'exceptions', label: 'Exceptions' },
          { id: 'context', label: 'Context (Saath)' },
          { id: 'generators', label: 'Generators (Upaj)' },
          { id: 'async', label: 'Async (Asamanantar)' },
          { id: 'pattern', label: 'Pattern (Milao)' },
          { id: 'scope', label: 'Scope & Imports' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveSection(tab.id)}
            style={{
              padding: '0.45rem 1rem',
              borderRadius: '9999px',
              border: 'none',
              background: activeSection === tab.id ? 'var(--accent-color)' : 'var(--bg-tertiary)',
              color: activeSection === tab.id ? '#ffffff' : 'var(--text-secondary)',
              fontWeight: 500,
              fontSize: '0.85rem',
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              transition: 'all 0.15s ease'
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* 1. Basics */}
      {activeSection === 'basics' && (
        <div>
          <h2 className="section-title">1. Buniyadi Niyam (Basics)</h2>
          <p className="section-subtitle">
            Variables, literals, comments, indentation aur basic data types.
          </p>

          <h3 className="subsection-title">Variables aur Assignment</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Variables ko declare karne ke liye seedha standard assignment operator <code>=</code> ka upyog hota hai:
          </p>
          <CodeBlock
            code={`naam = "Neeraj"
umar = 25
unchai = 5.9
sakriya = sahi       # Boolean True
chhutti = galat      # Boolean False
khali_jagah = shunya # Python None (alias: kuch_nahi)`}
            language="hin"
          />

          <h3 className="subsection-title">Indentation aur Block Sanrachna</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Hinglish mein blocks ko delimit karne ke liye curly braces <code>{}</code> ke bajay 
            Python ki tarah <strong>colon (:) aur 4 spaces indentation</strong> ka prayog hota hai:
          </p>
          <CodeBlock
            code={`agar umar >= 18:
    # 4 spaces indentation block shuru
    dikhao("Aap adult hain")
    dikhao("Namaste")`}
            language="hin"
          />

          <h3 className="subsection-title">Comments</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Single line comments <code>#</code> se shuru hote hain:
          </p>
          <CodeBlock
            code={`# Yeh ek poori line ka comment hai
x = 100 # Yeh ek inline comment hai`}
            language="hin"
          />
        </div>
      )}

      {/* 2. Control Flow */}
      {activeSection === 'control-flow' && (
        <div>
          <h2 className="section-title">2. Control Flow (Shartein aur Loops)</h2>
          <p className="section-subtitle">
            agar, warna_agar, warna, jabtak, har ... mein, ruko, aur aage_bado.
          </p>

          <h3 className="subsection-title">Shart Nirnay (agar / warna_agar / warna)</h3>
          <CodeBlock
            code={`ank = 85

agar ank >= 90:
    dikhao("Grade: A+")
warna_agar ank >= 75:
    dikhao("Grade: A")
warna_agar ank >= 60:
    dikhao("Grade: B")
warna:
    dikhao("Grade: C / Pass")`}
            language="hin"
          />

          <h3 className="subsection-title">While Loop (jabtak)</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Jab tak shart sahi rahegi tab tak loop chalta rahega:
          </p>
          <CodeBlock
            code={`sankhya = 1
jabtak sankhya <= 5:
    dikhao(f"Current sankhya: {sankhya}")
    sankhya = sankhya + 1`}
            language="hin"
          />

          <h3 className="subsection-title">For Loop (har ... mein / andar)</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Sequence iteration ke liye <code>mein</code> ya bolchal alias <code>andar</code> ka upyog karein:
          </p>
          <CodeBlock
            code={`# List iteration
shehar = ["Delhi", "Mumbai", "Bengaluru"]
har sh mein shehar:
    dikhao("Bhaarat ka shehar:", sh)

# Range loop
har i mein kram(1, 4):
    dikhao(f"Step {i}")`}
            language="hin"
          />

          <h3 className="subsection-title">Loop Control: ruko (break) aur aage_bado (continue)</h3>
          <CodeBlock
            code={`har n mein kram(1, 10):
    agar n == 3:
        aage_bado # 3 ko chhodkar agle par jao
    agar n == 8:
        ruko      # Loop se bahar nikal jao
    dikhao(n)`}
            language="hin"
          />
        </div>
      )}

      {/* 3. Functions */}
      {activeSection === 'functions' && (
        <div>
          <h2 className="section-title">3. Functions (kaam) aur Decorators</h2>
          <p className="section-subtitle">
            kaam, wapas, parameters, lambda (sookshm), aur decorators.
          </p>

          <h3 className="subsection-title">Function Paribhasha (kaam / wapas)</h3>
          <CodeBlock
            code={`kaam jodo(a, b, bonus = 5):
    kul = a + b + bonus
    wapas kul

dikhao(jodo(10, 20))        # 35
dikhao(jodo(10, 20, bonus=0)) # 30`}
            language="hin"
          />

          <h3 className="subsection-title">Vistrit Parameters (*args, **kwargs, /, *)</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Python 3 ki tarah positional-only (<code>/</code>), keyword-only (<code>*</code>), variable arguments shamil hain:
          </p>
          <CodeBlock
            code={`kaam configure(pos_val, /, normal_val, *args, kw_only = "def", **extra):
    dikhao("Positional only:", pos_val)
    dikhao("Args:", args)
    dikhao("Extra:", extra)`}
            language="hin"
          />

          <h3 className="subsection-title">Inline Anonymous Functions (sookshm / lambda)</h3>
          <CodeBlock
            code={`varg_fn = sookshm x: x * x
jod_fn = sookshm a, b: a + b

dikhao(varg_fn(7))      # 49
dikhao(jod_fn(12, 18))  # 30`}
            language="hin"
          />

          <h3 className="subsection-title">Decorators (@)</h3>
          <CodeBlock
            code={`kaam mera_decorator(fn):
    kaam wrapper(*args, **kwargs):
        dikhao("Function shuru hone se pehle")
        res = fn(*args, **kwargs)
        dikhao("Function khatam hone ke baad")
        wapas res
    wapas wrapper

@mera_decorator
kaam abhinandan(naam):
    dikhao(f"Namaste {naam}!")`}
            language="hin"
          />
        </div>
      )}

      {/* 4. Collections */}
      {activeSection === 'collections' && (
        <div>
          <h2 className="section-title">4. Collections aur Comprehensions</h2>
          <p className="section-subtitle">
            Lists, Dictionaries, Sets, Tuples aur shaktishali comprehensions.
          </p>

          <h3 className="subsection-title">List, Dict, Set, Tuple Syntax</h3>
          <CodeBlock
            code={`# List
mitra = ["Amit", "Sneha", "Rahul"]
mitra.append("Priya")

# Dictionary
upayogakarta = {
    "naam": "Aarav",
    "umar": 28,
    "shehar": "Pune"
}

# Set
anokhe_ank = {1, 2, 3, 2, 1} # {1, 2, 3}

# Tuple
sthir_bindu = (10, 20)`}
            language="hin"
          />

          <h3 className="subsection-title">List aur Dict Comprehensions</h3>
          <CodeBlock
            code={`# List comprehension
sam_varg = [x * x har x mein kram(1, 10) agar x % 2 == 0]
dikhao("Sam varg:", sam_varg)

# Dict comprehension
varg_kosh = {x: x * x har x mein kram(1, 5)}
dikhao("Dictionary:", varg_kosh)`}
            language="hin"
          />
        </div>
      )}

      {/* 5. OOP */}
      {activeSection === 'oop' && (
        <div>
          <h2 className="section-title">5. Object-Oriented Programming (varg / shreni)</h2>
          <p className="section-subtitle">
            varg, khood (self), inheritance, methods, aur properties.
          </p>

          <CodeBlock
            code={`# Class declaration
varg Gadi:
    kaam __init__(khood, model, gati = 0):
        khood.model = model
        khood.gati = gati

    kaam accelerate(khood, kitna):
        khood.gati = khood.gati + kitna
        dikhao(f"{khood.model} ki gati: {khood.gati} km/h")

# Inheritance
varg ElectricGadi(Gadi):
    kaam __init__(khood, model, battery_pct):
        Gadi.__init__(khood, model, 0)
        khood.battery = battery_pct

ev = ElectricGadi("Tata Nexon EV", 95)
ev.accelerate(40)`}
            language="hin"
          />
        </div>
      )}

      {/* 6. Exceptions */}
      {activeSection === 'exceptions' && (
        <div>
          <h2 className="section-title">6. Exception Handling (koshish, pakdo, antatah)</h2>
          <p className="section-subtitle">
            koshish (try), pakdo (except), antatah (finally), uthav (raise), aur daawa (assert).
          </p>

          <CodeBlock
            code={`kaam anupaat(a, b):
    # Assertion check
    daawa b != 0, "Bhaajak (b) shunya nahi ho sakta"
    
    koshish:
        natija = a / b
        wapas natija
    pakdo ZeroDivisionError jaise e:
        dikhao("Truti pakdi gayi:", e)
        uthav ValueError("Anya exception uthayi gayi")
    antatah:
        dikhao("Clean-up execution har baar chalega")`}
            language="hin"
          />
        </div>
      )}

      {/* 7. Context Managers */}
      {activeSection === 'context' && (
        <div>
          <h2 className="section-title">7. Context Managers (saath / lekar)</h2>
          <p className="section-subtitle">
            Resource management aur safe file operations.
          </p>

          <CodeBlock
            code={`# File reading
saath khol("sandesh.txt", "w") jaise file:
    file.write("Namaste Hinglish!")

saath khol("sandesh.txt", "r") jaise file:
    data = file.read()
    dikhao("File data:", data)`}
            language="hin"
          />
        </div>
      )}

      {/* 8. Generators */}
      {activeSection === 'generators' && (
        <div>
          <h2 className="section-title">8. Generators aur Yield (upaj)</h2>
          <p className="section-subtitle">
            Memory-efficient sequence generation with upaj.
          </p>

          <CodeBlock
            code={`kaam sankhya_dhara(antim):
    n = 1
    jabtak n <= antim:
        upaj n
        n = n + 1

har x mein sankhya_dhara(4):
    dikhao(f"Dhara se mila: {x}")`}
            language="hin"
          />
        </div>
      )}

      {/* 9. Async */}
      {activeSection === 'async' && (
        <div>
          <h2 className="section-title">9. Asynchronous Programming (asamanantar)</h2>
          <p className="section-subtitle">
            asamanantar (async), intezaar (await), aur asyncio co-operative multitasking.
          </p>

          <CodeBlock
            code={`laao asyncio

asamanantar kaam network_call(url):
    dikhao(f"Connecting: {url}")
    intezaar asyncio.sleep(0.05)
    wapas {"url": url, "status": 200}

asamanantar kaam main():
    res = intezaar network_call("https://api.example.com/data")
    dikhao("Prapt hua:", res)

asyncio.run(main())`}
            language="hin"
          />
        </div>
      )}

      {/* 10. Pattern Matching */}
      {activeSection === 'pattern' && (
        <div>
          <h2 className="section-title">10. Structural Pattern Matching (milao / sthiti)</h2>
          <p className="section-subtitle">
            Python 3.10+ match and case semantics with clean Hinglish keywords.
          </p>

          <CodeBlock
            code={`kaam handle_event(event):
    milao event:
        sthiti {"type": "click", "x": x, "y": y}:
            dikhao(f"Click at ({x}, {y})")
        sthiti {"type": "keypress", "key": k}:
            dikhao(f"Key dabayi gayi: {k}")
        sthiti [first, *rest]:
            dikhao(f"Sequence with first element: {first}")
        sthiti _:
            dikhao("Anya event fallback")`}
            language="hin"
          />
        </div>
      )}

      {/* 11. Scope & Imports */}
      {activeSection === 'scope' && (
        <div>
          <h2 className="section-title">11. Scope aur Module Imports</h2>
          <p className="section-subtitle">
            sarvavyapi (global), asthanik (nonlocal), hatao (del), laao (import), se (from).
          </p>

          <CodeBlock
            code={`# Module imports
laao math
se os laao path jaise rasta

# Variable scope
kul_ginti = 0

kaam counter_badhao():
    sarvavyapi kul_ginti
    kul_ginti = kul_ginti + 1

# Item deletion
kosh = {"a": 1, "b": 2}
hatao kosh["b"] # mitao kosh["b"]`}
            language="hin"
          />
        </div>
      )}
    </div>
  );
};
