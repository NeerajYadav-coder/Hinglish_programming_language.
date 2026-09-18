import { ExampleItem } from '../types';

export const EXAMPLES_DATA: ExampleItem[] = [
  {
    id: 'hello-world',
    title: '1. Namaste Duniya (Hello World)',
    category: 'Buniyadi',
    description: 'Hinglish ka sabse pehla basic program jo variables, conditional shart, aur dikhao (print) function ka pryog dikhata hai.',
    hinglishCode: `# Hinglish Mein Namaste Duniya
naam = "Neeraj"

agar naam == "Neeraj":
    dikhao("Namaste duniya!")
warna:
    dikhao("Hello!")
`,
    pythonCode: `# Python Samtulya Code
naam = "Neeraj"

if naam == "Neeraj":
    print("Namaste duniya!")
else:
    print("Hello!")
`,
    output: `Namaste duniya!`,
    keyConcepts: ['Variables', 'agar (if)', 'warna (else)', 'dikhao (print)']
  },
  {
    id: 'conditionals',
    title: '2. Shartein aur Conditionals',
    category: 'Control Flow',
    description: 'agar, warna_agar, aur warna ka upyog karke complex sharton ka nirnay lena.',
    hinglishCode: `# Conditionals ka pryog
umar = 17

agar umar >= 18:
    dikhao("Aap voting ke liye yogya hain!")
warna_agar umar >= 16:
    dikhao("Aap learner driving license le sakte hain!")
warna:
    dikhao("Abhi aap chhote hain, thoda intezaar karein!")
`,
    pythonCode: `umar = 17

if umar >= 18:
    print("Aap voting ke liye yogya hain!")
elif umar >= 16:
    print("Aap learner driving license le sakte hain!")
else:
    print("Abhi aap chhote hain, thoda intezaar karein!")
`,
    output: `Aap learner driving license le sakte hain!`,
    keyConcepts: ['agar', 'warna_agar', 'warna', 'comparison operators']
  },
  {
    id: 'loops',
    title: '3. Loops (jabtak aur har)',
    category: 'Control Flow',
    description: 'Indefinite while loop (jabtak) aur sequence iterative for loop (har ... mein) ka saaf udaharan.',
    hinglishCode: `# While Loop (jabtak)
ginti = 1
jabtak ginti <= 3:
    dikhao(f"Ginti number: {ginti}")
    ginti = ginti + 1

# For Loop (har ... mein)
phal = ["Aam", "Seb", "Kela"]
har p mein phal:
    dikhao("Mera pasandida phal:", p)
`,
    pythonCode: `ginti = 1
while ginti <= 3:
    print(f"Ginti number: {ginti}")
    ginti = ginti + 1

phal = ["Aam", "Seb", "Kela"]
for p in phal:
    print("Mera pasandida phal:", p)
`,
    output: `Ginti number: 1
Ginti number: 2
Ginti number: 3
Mera pasandida phal: Aam
Mera pasandida phal: Seb
Mera pasandida phal: Kela`,
    keyConcepts: ['jabtak (while)', 'har (for)', 'mein (in)', 'f-strings']
  },
  {
    id: 'functions',
    title: '4. Functions (kaam) aur Lambda (sookshm)',
    category: 'Functions',
    description: 'Named functions (kaam), return (wapas), aur inline lightweight lambda expressions (sookshm).',
    hinglishCode: `# Function definition
kaam jod(pehla, doosra = 10):
    wapas pehla + doosra

kul = jod(25)
dikhao(f"Kul jod: {kul}")

# Sookshm (Lambda) Expression
guna_do = sookshm x: x * 2
dikhao(f"Double: {guna_do(15)}")
`,
    pythonCode: `def jod(pehla, doosra=10):
    return pehla + doosra

kul = jod(25)
print(f"Kul jod: {kul}")

guna_do = lambda x: x * 2
print(f"Double: {guna_do(15)}")
`,
    output: `Kul jod: 35
Double: 30`,
    keyConcepts: ['kaam (def)', 'wapas (return)', 'default args', 'sookshm (lambda)']
  },
  {
    id: 'oop-classes',
    title: '5. Classes aur Objects (varg)',
    category: 'OOP',
    description: 'Object-oriented programming using varg, khood (self), constructor initialization, and methods.',
    hinglishCode: `# Class definition
varg Khata:
    kaam __init__(khood, dharak, rashi):
        khood.dharak = dharak
        khood.rashi = rashi

    kaam jama(khood, dhan):
        khood.rashi = khood.rashi + dhan
        dikhao(f"{khood.dharak} ke khate mein {dhan} jama huye. Kul: {khood.rashi}")

k = Khata("Aarav", 500)
k.jama(250)
`,
    pythonCode: `class Khata:
    def __init__(self, dharak, rashi):
        self.dharak = dharak
        self.rashi = rashi

    def jama(self, dhan):
        self.rashi = self.rashi + dhan
        print(f"{self.dharak} ke khate mein {dhan} jama huye. Kul: {self.rashi}")

k = Khata("Aarav", 500)
k.jama(250)
`,
    output: `Aarav ke khate mein 250 jama huye. Kul: 750`,
    keyConcepts: ['varg (class)', 'khood (self)', '__init__', 'methods']
  },
  {
    id: 'exceptions',
    title: '6. Exception Handling (koshish aur pakdo)',
    category: 'Exceptions',
    description: 'Robust error handling with koshish (try), pakdo (except), antatah (finally), and uthav (raise).',
    hinglishCode: `# Exception Handling
koshish:
    sankhya = 10 / 0
pakdo ZeroDivisionError jaise truti:
    dikhao(f"Galti pakdi gayi: {truti}")
antatah:
    dikhao("Yeh block har sthiti mein chalega (Clean-up sampann).")
`,
    pythonCode: `try:
    sankhya = 10 / 0
except ZeroDivisionError as truti:
    print(f"Galti pakdi gayi: {truti}")
finally:
    print("Yeh block har sthiti mein chalega (Clean-up sampann).")
`,
    output: `Galti pakdi gayi: division by zero
Yeh block har sthiti mein chalega (Clean-up sampann).`,
    keyConcepts: ['koshish (try)', 'pakdo (except)', 'jaise (as)', 'antatah (finally)']
  },
  {
    id: 'comprehensions',
    title: '7. Comprehensions aur Generators',
    category: 'Collections',
    description: 'List, Dict comprehensions aur generator stream yield karne ke liye upaj keyword ka istemal.',
    hinglishCode: `# List Comprehension
sam_varg = [x ** 2 har x mein kram(1, 7) agar x % 2 == 0]
dikhao("Sam sankhya ke varg:", sam_varg)

# Generator Function
kaam gin():
    upaj 10
    upaj 20
    upaj 30

har g mein gin():
    dikhao(f"Generator value: {g}")
`,
    pythonCode: `sam_varg = [x ** 2 for x in range(1, 7) if x % 2 == 0]
print("Sam sankhya ke varg:", sam_varg)

def gin():
    yield 10
    yield 20
    yield 30

for g in gin():
    print(f"Generator value: {g}")
`,
    output: `Sam sankhya ke varg: [4, 16, 36]
Generator value: 10
Generator value: 20
Generator value: 30`,
    keyConcepts: ['List comprehension', 'har ... mein ... agar', 'upaj (yield)']
  },
  {
    id: 'async-await',
    title: '8. Asynchronous Programming (asamanantar)',
    category: 'Async',
    description: 'Modern asynchronous workflows using asamanantar (async), intezaar (await), and asyncio integration.',
    hinglishCode: `laao asyncio

asamanantar kaam fetch_message(id):
    intezaar asyncio.sleep(0.01)
    wapas f"Payload #{id} prapt hua"

asamanantar kaam mukhya():
    dikhao("Data mangwa rahe hain...")
    res = intezaar fetch_message(42)
    dikhao("Async Natija:", res)

asyncio.run(mukhya())
`,
    pythonCode: `import asyncio

async def fetch_message(id):
    await asyncio.sleep(0.01)
    return f"Payload #{id} prapt hua"

async def mukhya():
    print("Data mangwa rahe hain...")
    res = await fetch_message(42)
    print("Async Natija:", res)

asyncio.run(mukhya())
`,
    output: `Data mangwa rahe hain...
Async Natija: Payload #42 prapt hua`,
    keyConcepts: ['asamanantar (async)', 'intezaar (await)', 'asyncio']
  },
  {
    id: 'pattern-matching',
    title: '9. Structural Pattern Matching (milao aur sthiti)',
    category: 'Pattern Matching',
    description: 'Python 3.10+ style structural pattern matching using milao (match), sthiti (case), wildcard _, and captures.',
    hinglishCode: `# Pattern Matching Example
kaam process_status(code):
    milao code:
        sthiti 200:
            dikhao("Status: Success (200 OK)")
        sthiti 404:
            dikhao("Status: Not Found (404)")
        sthiti [code, sandesh]:
            dikhao(f"Complex Status [{code}]: {sandesh}")
        sthiti _:
            dikhao("Agyaat status code")

process_status(200)
process_status([500, "Server Error"])
`,
    pythonCode: `def process_status(code):
    match code:
        case 200:
            print("Status: Success (200 OK)")
        case 404:
            print("Status: Not Found (404)")
        case [code, sandesh]:
            print(f"Complex Status [{code}]: {sandesh}")
        case _:
            print("Agyaat status code")

process_status(200)
process_status([500, "Server Error"])
`,
    output: `Status: Success (200 OK)
Complex Status [500]: Server Error`,
    keyConcepts: ['milao (match)', 'sthiti (case)', 'wildcard _', 'sequence pattern']
  },
  {
    id: 'multi-file',
    title: '10. Bahu-File (Multi-File) Project Architecture',
    category: 'Projects',
    description: 'Real-world multi-file layout with native .hin inter-module imports and working-directory independence.',
    hinglishCode: `# File: utils.hin
kaam jod(a, b):
    wapas a + b

# File: main.hin
laao utils

kul = utils.jod(15, 25)
dikhao(f"Multi-file Jod Natija: {kul}")
`,
    pythonCode: `# File: utils.py
def jod(a, b):
    return a + b

# File: main.py
import utils

kul = utils.jod(15, 25)
print(f"Multi-file Jod Natija: {kul}")
`,
    output: `Multi-file Jod Natija: 40`,
    keyConcepts: ['laao (import)', 'multi-file .hin resolution', 'sys.path independence']
  },
  {
    id: 'editor-demo',
    title: '11. Hinglish Full Showcase (v1.0.0)',
    category: 'Showcase',
    description: 'Comprehensive test program covering OOP, decorators, exception handling, dictionary operations, and deletion.',
    hinglishCode: `# Hinglish v1.0.0 Showcase
varg Calculator:
    kaam __init__(khood, offset = 0):
        khood.offset = offset

    kaam ganana(khood, a, b):
        koshish:
            natija = (a * b) + khood.offset
            wapas natija
        pakdo Exception jaise err:
            dikhao("Error aayi:", err)
            wapas shunya

calc = Calculator(10)
dikhao("Natija:", calc.ganana(5, 4))
`,
    pythonCode: `class Calculator:
    def __init__(self, offset=0):
        self.offset = offset

    def ganana(self, a, b):
        try:
            natija = (a * b) + self.offset
            return natija
        except Exception as err:
            print("Error aayi:", err)
            return None

calc = Calculator(10)
print("Natija:", calc.ganana(5, 4))
`,
    output: `Natija: 30`,
    keyConcepts: ['varg', 'koshish', 'pakdo', 'wapas', 'shunya']
  }
];
