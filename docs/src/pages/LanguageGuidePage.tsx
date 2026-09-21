import React, { useState } from 'react';
import { CodeBlock } from '../components/CodeBlock';

export const LanguageGuidePage: React.FC = () => {
  const [activeSection, setActiveSection] = useState('basics');

  return (
    <div>
      <div style={{ marginBottom: '2.5rem' }}>
        <span className="apple-pill" style={{ marginBottom: '0.75rem' }}>Full Guide</span>
        <h1 className="hero-title" style={{ fontSize: '2.6rem' }}>Hinglish Language Guide</h1>
        <p className="hero-subtitle">
          Hinglish v1.1.0 ke sabhi basic aur advanced features ko aasan shabdon mein samjhein.
        </p>
      </div>

      {/* Segmented Sub-navigation pills */}
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
          { id: 'basics', label: '1. Basics' },
          { id: 'control-flow', label: '2. Conditions & Loops' },
          { id: 'functions', label: '3. Functions (Kaam)' },
          { id: 'collections', label: '4. Lists & Dicts' },
          { id: 'oop', label: '5. Classes & OOP' },
          { id: 'exceptions', label: '6. Error Handling' },
          { id: 'context', label: '7. File Open (Saath)' },
          { id: 'generators', label: '8. Generators (Upaj)' },
          { id: 'async', label: '9. Async (Asamanantar)' },
          { id: 'pattern', label: '10. Pattern Match' },
          { id: 'scope', label: '11. Imports & Scope' }
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
          <h2 className="section-title">1. Basics (Variables, Data Types, Comments)</h2>
          <p className="section-subtitle">
            Hinglish mein variables kaise banate hain aur code kaise likhte hain.
          </p>

          <h3 className="subsection-title">Variables aur Values</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Variable banane ke liye seedha naam likhkar <code>=</code> lagayein:
          </p>
          <CodeBlock
            code={`naam = "Neeraj"
umar = 25
unchai = 5.9
active = sahi       # Python True
chhutti = galat     # Python False
khali = shunya      # Python None (kuch_nahi bhi chalega)`}
            language="hin"
          />

          <h3 className="subsection-title">Indentation (4 Spaces)</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Python ki tarah yahan bhi curly brackets <code>{}</code> nahi lagte. 
            Code block ko colon <code>:</code> ke baad 4 spaces aage badha kar (indent karke) likhte hain:
          </p>
          <CodeBlock
            code={`agar umar >= 18:
    # 4 spaces indentation
    dikhao("Aap adult hain")
    dikhao("Namaste")`}
            language="hin"
          />

          <h3 className="subsection-title">Bilingual Built-in Aliases (v1.1)</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Hinglish v1.1 mein natural Hindi aur English dono built-in functions seamlessly chalte hain:
          </p>
          <CodeBlock
            code={`ank = [10, 20, 30, 40]

# lambai ya len
dikhao(lambai(ank))         # Output: 4
dikhao(len(ank))            # Output: 4

# ginti ya range / kram
har i mein ginti(1, 4):     # 1, 2, 3
    dikhao("Ginti step:", i)

# jod ya sum / kul_jod
dikhao("Total sum:", jod(ank)) # Output: 100

# sab (all) aur koi (any)
dikhao(sab([sahi, sahi]))   # True
dikhao(koi([galat, sahi]))  # True`}
            language="hin"
          />

          <h3 className="subsection-title">Comments</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Comments likhne ke liye <code>#</code> ka use karein:
          </p>
          <CodeBlock
            code={`# Yeh ek comment line hai
x = 100 # Yeh aage ka comment hai`}
            language="hin"
          />
        </div>
      )}

      {/* 2. Control Flow */}
      {activeSection === 'control-flow' && (
        <div>
          <h2 className="section-title">2. Conditions aur Loops</h2>
          <p className="section-subtitle">
            agar, warna_agar, warna, inline ternary, jabtak, har ... mein, ruko, aur aage_bado.
          </p>

          <h3 className="subsection-title">If-Else (agar / warna_agar / warna)</h3>
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

          <h3 className="subsection-title">Inline Conditional Expression (v1.1 Ternary Operator)</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Python ke ternary operator (<code>x if cond else y</code>) ka natural Hinglish roop: <code>&lt;expr&gt; agar &lt;shart&gt; warna &lt;fallback&gt;</code>. Concise assignment aur function returns ke liye best hai:
          </p>
          <CodeBlock
            code={`# 1. Single-line variable assignment
umar = 19
status = "Adult" agar umar >= 18 warna "Minor"
dikhao("User status:", status)

# 2. Function returns
kaam get_access(role):
    wapas "Full Access" agar role == "admin" warna "Guest Access"

# 3. Short-circuit / Lazy evaluation:
# Agar shart sahi hai toh 'warna' wala expression execute hi nahi hoga
safe = 100 agar sahi warna (1 / 0)  # Safe! ZeroDivisionError nahi aayega`}
            language="hin"
          />

          <h3 className="subsection-title">While Loop (jabtak)</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            Jab tak shart sach rahegi, loop chalta rahega:
          </p>
          <CodeBlock
            code={`sankhya = 1
jabtak sankhya <= 5:
    dikhao(f"Number hai: {sankhya}")
    sankhya = sankhya + 1`}
            language="hin"
          />

          <h3 className="subsection-title">For Loop (har ... mein / andar)</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
            List ya range par loop chalane ke liye <code>mein</code> ya <code>andar</code> use karein:
          </p>
          <CodeBlock
            code={`# List par loop
shehar = ["Delhi", "Mumbai", "Bengaluru"]
har sh mein shehar:
    dikhao("Shehar ka naam:", sh)

# Range par loop (ginti ya kram)
har i mein ginti(1, 4):
    dikhao(f"Step {i}")`}
            language="hin"
          />

          <h3 className="subsection-title">Loop Control (ruko aur aage_bado)</h3>
          <CodeBlock
            code={`har n mein ginti(1, 10):
    agar n == 3:
        aage_bado # 3 ko skip karke agle par jao (continue)
    agar n == 8:
        ruko      # Loop se bahar nikal jao (break)
    dikhao(n)`}
            language="hin"
          />
        </div>
      )}

      {/* 3. Functions */}
      {activeSection === 'functions' && (
        <div>
          <h2 className="section-title">3. Functions (kaam) aur Short Functions (sookshm)</h2>
          <p className="section-subtitle">
            kaam, wapas, parameters, default values, aur decorators.
          </p>

          <h3 className="subsection-title">Function Banana (kaam / wapas)</h3>
          <CodeBlock
            code={`kaam jodo(a, b, bonus = 5):
    kul = a + b + bonus
    wapas kul

dikhao(jodo(10, 20))        # Output: 35
dikhao(jodo(10, 20, bonus=0)) # Output: 30`}
            language="hin"
          />

          <h3 className="subsection-title">Short Lambda Functions (sookshm)</h3>
          <CodeBlock
            code={`square = sookshm x: x * x
jod_do = sookshm a, b: a + b

dikhao(square(7))     # 49
dikhao(jod_do(12, 18)) # 30`}
            language="hin"
          />

          <h3 className="subsection-title">Decorators (@)</h3>
          <CodeBlock
            code={`kaam mera_decorator(fn):
    kaam wrapper(*args, **kwargs):
        dikhao("Function shuru ho raha hai")
        res = fn(*args, **kwargs)
        dikhao("Function poora ho gaya")
        wapas res
    wapas wrapper

@mera_decorator
kaam greet(naam):
    dikhao(f"Namaste {naam}!")`}
            language="hin"
          />
        </div>
      )}

      {/* 4. Collections */}
      {activeSection === 'collections' && (
        <div>
          <h2 className="section-title">4. Lists, Dictionaries aur Comprehensions</h2>
          <p className="section-subtitle">
            Data store karne aur single line mein filter karne ke aasan tareeqe.
          </p>

          <h3 className="subsection-title">List, Dictionary, Set aur Tuple</h3>
          <CodeBlock
            code={`# List
mitra = ["Amit", "Sneha", "Rahul"]
mitra.append("Priya")

# Dictionary
user = {
    "naam": "Aarav",
    "umar": 28,
    "shehar": "Pune"
}

# Set (Unique values)
anokhe_ank = {1, 2, 3, 2, 1} # {1, 2, 3}

# Tuple (Fixed values)
point = (10, 20)`}
            language="hin"
          />

          <h3 className="subsection-title">List & Dict Comprehensions</h3>
          <CodeBlock
            code={`# Ek line mein list filter aur square karna
sam_varg = [x * x har x mein ginti(1, 10) agar x % 2 == 0]
dikhao("Even squares:", sam_varg)

# Dictionary comprehension
squares_map = {x: x * x har x mein ginti(1, 5)}
dikhao("Map:", squares_map)`}
            language="hin"
          />

          <div className="apple-callout" style={{ marginTop: '1.25rem' }}>
            <div>
              <strong>Pro-Tip (Comprehension Syntax in Hinglish):</strong> Hinglish comprehensions mein Python ke <code>for ... in</code> ki jagah <strong><code>har ... mein</code></strong> use hota hai:
              <br />
              <code>[x * 2 har x mein ginti(5)]</code>
              <br />
              <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
                Agar aap aadat ke chalte Python-style <code>for ... in</code> likh dete hain, toh Hinglish v1.1 ka parser aur linter turant helpful diagnostic hint deta hai: <em>"Hinglish mein 'har &lt;var&gt; mein &lt;iter&gt;' likhein"</em>.
              </span>
            </div>
          </div>
        </div>
      )}

      {/* 5. OOP */}
      {activeSection === 'oop' && (
        <div>
          <h2 className="section-title">5. Classes aur Objects (varg)</h2>
          <p className="section-subtitle">
            varg, khood (self), constructor (__init__), aur methods.
          </p>

          <CodeBlock
            code={`# Class banayein
varg Gadi:
    kaam __init__(khood, model, speed = 0):
        khood.model = model
        khood.speed = speed

    kaam accelerate(khood, kitna):
        khood.speed = khood.speed + kitna
        dikhao(f"{khood.model} ki speed: {khood.speed} km/h")

# Inheritance (Subclass)
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
          <h2 className="section-title">6. Error Handling (koshish aur pakdo)</h2>
          <p className="section-subtitle">
            koshish (try), pakdo (except), antatah (finally), uthav (raise), aur daawa (assert).
          </p>

          <CodeBlock
            code={`kaam divide(a, b):
    # Assertion check
    daawa b != 0, "Divider shunya (zero) nahi hona chahiye"
    
    koshish:
        natija = a / b
        wapas natija
    pakdo ZeroDivisionError jaise e:
        dikhao("Error aayi:", e)
        uthav ValueError("Invalid division operation")
    antatah:
        dikhao("Yeh clean-up block har baar chalega")`}
            language="hin"
          />
        </div>
      )}

      {/* 7. Context Managers */}
      {activeSection === 'context' && (
        <div>
          <h2 className="section-title">7. Files Safely Open Karna (saath / khol)</h2>
          <p className="section-subtitle">
            File reading aur writing bina memory leak ke.
          </p>

          <CodeBlock
            code={`# File mein likhein
saath khol("sandesh.txt", "w") jaise file:
    file.write("Namaste Hinglish!")

# File padhein
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
            Values ko stream ke roop mein ek-ek karke generate karna.
          </p>

          <CodeBlock
            code={`kaam ginti_stream(antim):
    n = 1
    jabtak n <= antim:
        upaj n
        n = n + 1

har x mein ginti_stream(4):
    dikhao(f"Stream se mila: {x}")`}
            language="hin"
          />
        </div>
      )}

      {/* 9. Async */}
      {activeSection === 'async' && (
        <div>
          <h2 className="section-title">9. Async Programming (asamanantar aur intezaar)</h2>
          <p className="section-subtitle">
            Fast background network calls aur coroutines.
          </p>

          <CodeBlock
            code={`laao asyncio

asamanantar kaam fetch_api(url):
    dikhao(f"Calling: {url}")
    intezaar asyncio.sleep(0.05)
    wapas {"url": url, "status": 200}

asamanantar kaam main():
    res = intezaar fetch_api("https://api.example.com/data")
    dikhao("Mil gaya:", res)

asyncio.run(main())`}
            language="hin"
          />
        </div>
      )}

      {/* 10. Pattern Matching */}
      {activeSection === 'pattern' && (
        <div>
          <h2 className="section-title">10. Pattern Matching (milao aur sthiti)</h2>
          <p className="section-subtitle">
            Python 3.10+ match-case semantics with milao aur sthiti.
          </p>

          <CodeBlock
            code={`kaam handle_event(event):
    milao event:
        sthiti {"type": "click", "x": x, "y": y}:
            dikhao(f"Click hua ({x}, {y}) par")
        sthiti {"type": "keypress", "key": k}:
            dikhao(f"Key press hui: {k}")
        sthiti [first, *rest]:
            dikhao(f"First element: {first}")
        sthiti _:
            dikhao("Koi aur event mila")`}
            language="hin"
          />
        </div>
      )}

      {/* 11. Scope & Imports */}
      {activeSection === 'scope' && (
        <div>
          <h2 className="section-title">11. Scope aur Module Imports (laao / se)</h2>
          <p className="section-subtitle">
            sarvavyapi (global), asthanik (nonlocal), hatao (del), laao (import).
          </p>

          <CodeBlock
            code={`# Imports
laao math
se os laao path jaise rasta

# Global variable
total = 0

kaam badhao():
    sarvavyapi total
    total = total + 1

# Delete item
user_data = {"a": 1, "b": 2}
hatao user_data["b"] # mitao bhi likh sakte hain`}
            language="hin"
          />
        </div>
      )}
    </div>
  );
};
