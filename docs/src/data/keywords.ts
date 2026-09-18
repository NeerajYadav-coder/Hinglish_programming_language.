import { KeywordInfo } from '../types';

export const KEYWORDS_DATA: KeywordInfo[] = [
  // Statements & Control Flow
  {
    token: 'agar',
    python: 'if',
    category: 'Statements',
    meaning: 'Condition check karne ke liye (if)',
    description: 'Agar di gayi condition sahi (True) hoti hai toh yeh block chalega.',
    example: 'agar umar >= 18:\n    dikhao("Aap vote de sakte hain")'
  },
  {
    token: 'warna',
    python: 'else',
    category: 'Statements',
    meaning: 'Agar pehli condition galat ho (else)',
    description: 'Jab koi bhi condition match na kare, tab warna block chalta hai.',
    example: 'agar sankhya > 0:\n    dikhao("Positive number")\nwarna:\n    dikhao("Zero ya negative number")'
  },
  {
    token: 'warna_agar',
    python: 'elif',
    category: 'Statements',
    meaning: 'Ek aur nayi condition check karne ke liye (elif)',
    description: 'Agar pehla agar galat nikle, toh doosri condition test karne ke liye.',
    example: 'agar ank >= 90:\n    dikhao("A Grade")\nwarna_agar ank >= 75:\n    dikhao("B Grade")\nwarna:\n    dikhao("Pass")'
  },
  {
    token: 'jabtak',
    python: 'while',
    category: 'Statements',
    meaning: 'Jab tak condition sach ho tab tak chalao (while loop)',
    description: 'Yeh loop tab tak chalta rahega jab tak condition False na ho jaye.',
    example: 'ginti = 1\njabtak ginti <= 3:\n    dikhao(f"Ginti number: {ginti}")\n    ginti = ginti + 1'
  },
  {
    token: 'har',
    python: 'for',
    category: 'Statements',
    meaning: 'Ek-ek karke sabhi items par loop chalana (for loop)',
    description: 'Kisi list, range ya text ke har element par traverse karne ke liye.',
    example: 'har i mein kram(1, 4):\n    dikhao(f"Number: {i}")'
  },
  {
    token: 'mein',
    python: 'in',
    category: 'Statements',
    meaning: 'Collection ke andar check ya loop karna (in)',
    description: 'Loop mein collection batane ya item present hai ya nahi check karne ke liye.',
    aliases: ['andar'],
    example: 'har naam mein ["Aarav", "Priya"]:\n    dikhao("Hello", naam)'
  },
  {
    token: 'ruko',
    python: 'break',
    category: 'Statements',
    meaning: 'Loop ko turant beech mein rok dena (break)',
    description: 'Condition match hone par chalu loop se turant bahar aa jata hai.',
    example: 'har n mein kram(1, 10):\n    agar n == 5:\n        ruko\n    dikhao(n)'
  },
  {
    token: 'aage_bado',
    python: 'continue',
    category: 'Statements',
    meaning: 'Agli baari par jump karna (continue)',
    description: 'Bache huye code ko chhodkar loop ki agli round shuru karta hai.',
    example: 'har n mein kram(1, 6):\n    agar n % 2 == 0:\n        aage_bado\n    dikhao(f"Odd number: {n}")'
  },
  {
    token: 'chhod_do',
    python: 'pass',
    category: 'Statements',
    meaning: 'Khali placeholder chhodne ke liye (pass)',
    description: 'Agar abhi function ya block mein kuch nahi likhna toh ise use karein.',
    example: 'kaam abhi_baki_hai():\n    chhod_do'
  },
  {
    token: 'kaam',
    python: 'def',
    category: 'Statements',
    meaning: 'Naya function banane ke liye (def)',
    description: 'Apna reusable function banayein jise code mein baar-baar call kar sakein.',
    example: 'kaam jod(a, b):\n    wapas a + b\n\nnatija = jod(10, 20)'
  },
  {
    token: 'varg',
    python: 'class',
    category: 'Statements',
    meaning: 'Nayi class banane ke liye (class)',
    description: 'Object-oriented programming ke liye custom blueprint ya class banana.',
    aliases: ['shreni'],
    example: 'varg User:\n    kaam __init__(khood, naam):\n        khood.naam = naam\n\nu = User("Neeraj")'
  },
  {
    token: 'wapas',
    python: 'return',
    category: 'Statements',
    meaning: 'Function se value lautana (return)',
    description: 'Calculation ya result ko function call karne wale ko wapas bhejta hai.',
    example: 'kaam square(x):\n    wapas x * x'
  },
  {
    token: 'upaj',
    python: 'yield',
    category: 'Statements',
    meaning: 'Generator se ek-ek karke value bhejna (yield)',
    description: 'Puri list memory mein store kiye bina stream ke roop mein values bhejna.',
    example: 'kaam ginti_stream():\n    upaj 1\n    upaj 2\n    upaj 3'
  },
  {
    token: 'sookshm',
    python: 'lambda',
    category: 'Statements',
    meaning: 'Ek line ka chhota function (lambda)',
    description: 'Inline lightweight bina naam ka function banane ke liye.',
    example: 'square_fn = sookshm x: x ** 2\ndikhao(square_fn(5))'
  },
  {
    token: 'koshish',
    python: 'try',
    category: 'Statements',
    meaning: 'Error check karne ke liye (try)',
    description: 'Aise code ko wrap karta hai jahan error aane ka chance ho.',
    example: 'koshish:\n    natija = 10 / 0\npakdo ZeroDivisionError jaise e:\n    dikhao("Zero division error pakda gaya!")'
  },
  {
    token: 'pakdo',
    python: 'except',
    category: 'Statements',
    meaning: 'Error ko sambhalna (except / catch)',
    description: 'Program crash hone se bacha kar error ko catch karta hai.',
    aliases: ['sambhalo'],
    example: 'koshish:\n    x = int("abc")\npakdo ValueError:\n    dikhao("Galat number format")'
  },
  {
    token: 'antatah',
    python: 'finally',
    category: 'Statements',
    meaning: 'Aakhir mein pakka chalne wala block (finally)',
    description: 'Chahe error aaye ya na aaye, yeh block hamesha chalta hai.',
    aliases: ['aakhir_mein'],
    example: 'koshish:\n    dikhao("Kaam chalu")\nantatah:\n    dikhao("Clean-up complete ho gaya")'
  },
  {
    token: 'uthav',
    python: 'raise',
    category: 'Statements',
    meaning: 'Custom error trigger karna (raise error)',
    description: 'Apni marzi se koi bhi error explicitly trigger karne ke liye.',
    aliases: ['fenko'],
    example: 'agar umar < 0:\n    uthav ValueError("Umar negative nahi ho sakti!")'
  },
  {
    token: 'daawa',
    python: 'assert',
    category: 'Statements',
    meaning: 'Condition verify karna (assert)',
    description: 'Agar condition galat ho toh program turant AssertionError deta hai.',
    aliases: ['dawa'],
    example: 'daawa 10 > 0, "Number positive hona chahiye"'
  },
  {
    token: 'saath',
    python: 'with',
    category: 'Statements',
    meaning: 'Resource / File ko safely handle karna (with block)',
    description: 'Kaam hone par file ya resource ko apne aap band kar deta hai.',
    aliases: ['lekar'],
    example: 'saath khol("data.txt", "w") jaise f:\n    f.write("Namaste")'
  },
  {
    token: 'jaise',
    python: 'as',
    category: 'Statements',
    meaning: 'Naya naam ya alias dena (as)',
    description: 'Import, file open ya except error ko variable naam dene ke liye.',
    aliases: ['roop_mein'],
    example: 'se math laao sqrt jaise square_root\ndikhao(square_root(16))'
  },
  {
    token: 'sarvavyapi',
    python: 'global',
    category: 'Statements',
    meaning: 'Global variable modify karna (global)',
    description: 'Function ke andar se bahar wale global variable ko update karne ke liye.',
    example: 'ginti = 0\nkaam badhao():\n    sarvavyapi ginti\n    ginti = ginti + 1'
  },
  {
    token: 'asthanik',
    python: 'nonlocal',
    category: 'Statements',
    meaning: 'Outer function ka variable modify karna (nonlocal)',
    description: 'Nested function ke andar outer variable ko bind karne ke liye.',
    aliases: ['asthaniya'],
    example: 'kaam bahar():\n    x = 10\n    kaam andar():\n        asthanik x\n        x = 20\n    andar()'
  },
  {
    token: 'hatao',
    python: 'del',
    category: 'Statements',
    meaning: 'Variable ya item delete karna (del)',
    description: 'List item, dictionary key ya variable ko delete karta hai.',
    aliases: ['mitao'],
    example: 'data = {"a": 1, "b": 2}\nhatao data["b"]'
  },
  {
    token: 'laao',
    python: 'import',
    category: 'Statements',
    meaning: 'Module ya library import karna (import)',
    description: 'Python ki library ya apni .hin files ko program mein load karta hai.',
    example: 'laao math\ndikhao(math.pi)'
  },
  {
    token: 'se',
    python: 'from',
    category: 'Statements',
    meaning: 'Module ke andar se kuch lana (from import)',
    description: 'Module se specific function ya class direct import karne ke liye.',
    example: 'se datetime laao datetime\ndikhao(datetime.now())'
  },
  {
    token: 'asamanantar',
    python: 'async',
    category: 'Statements',
    meaning: 'Async function banana (async)',
    description: 'Fast background task ya coroutine define karne ke liye.',
    example: 'asamanantar kaam fetch_data():\n    intezaar asyncio.sleep(1)\n    wapas "Data mil gaya"'
  },
  {
    token: 'intezaar',
    python: 'await',
    category: 'Statements',
    meaning: 'Async task ka wait karna (await)',
    description: 'Jab tak background task poora na ho jaye, wait karke result leta hai.',
    example: 'natija = intezaar fetch_data()'
  },

  // Soft Keywords (Pattern Matching)
  {
    token: 'milao',
    python: 'match',
    category: 'Soft Keywords',
    meaning: 'Pattern match karna (match)',
    description: 'Value ka structure check karke sahi case par redirect karta hai.',
    aliases: ['milaao'],
    example: 'milao status_code:\n    sthiti 200:\n        dikhao("OK")\n    sthiti 404:\n        dikhao("Not Found")'
  },
  {
    token: 'sthiti',
    python: 'case',
    category: 'Soft Keywords',
    meaning: 'Match ka ek case branch (case)',
    description: 'Milao statement ke andar har condition branch ko define karta hai.',
    aliases: ['vichaar'],
    example: 'milao command:\n    sthiti ["quit", reason]:\n        dikhao(f"Quitting: {reason}")\n    sthiti _:\n        dikhao("Koi aur command")'
  },

  // Operators
  {
    token: 'aur',
    python: 'and',
    category: 'Operators',
    meaning: 'Dono shartein sahi honi chahiye (and)',
    description: 'Jab pehli aur doosri dono conditions True hon tabhi result True hoga.',
    example: 'agar umar >= 18 aur nagrik == sahi:\n    dikhao("Vote de sakte hain")'
  },
  {
    token: 'ya',
    python: 'or',
    category: 'Operators',
    meaning: 'Dono mein se koi ek shart sahi ho (or)',
    description: 'Dono mein se koi bhi ek condition True ho toh result True milta hai.',
    example: 'agar sunday == sahi ya chhutti == sahi:\n    dikhao("Aaram karein")'
  },
  {
    token: 'nahi',
    python: 'not',
    category: 'Operators',
    meaning: 'Ulta karna (not)',
    description: 'Condition ko invert karta hai (True ko False aur False ko True).',
    example: 'agar nahi logged_in:\n    dikhao("Pehle login karein")'
  },
  {
    token: 'hai',
    python: 'is',
    category: 'Operators',
    meaning: 'Same object identity check karna (is)',
    description: 'Check karta hai ki kya do variables memory mein bilkul same object hain.',
    example: 'agar natija hai kuch_nahi:\n    dikhao("Result khali hai")'
  },

  // Literals
  {
    token: 'sahi',
    python: 'True',
    category: 'Literals',
    meaning: 'True (Sach)',
    description: 'Boolean true value ko represent karta hai.',
    example: 'active = sahi\nagar active:\n    dikhao("Account active hai")'
  },
  {
    token: 'galat',
    python: 'False',
    category: 'Literals',
    meaning: 'False (Jhooth / Galat)',
    description: 'Boolean false value ko represent karta hai.',
    example: 'failed = galat\nagar nahi failed:\n    dikhao("Sab badhiya chal raha hai")'
  },
  {
    token: 'kuch_nahi',
    python: 'None',
    category: 'Literals',
    meaning: 'None (Khali object)',
    description: 'Python ke None singleton object ko darshata hai.',
    aliases: ['shunya'],
    example: 'data = kuch_nahi\nagar data hai kuch_nahi:\n    dikhao("Abhi koi data nahi hai")'
  },

  // Built-in Core Functions
  {
    token: 'dikhao',
    python: 'print',
    category: 'Builtins',
    meaning: 'Screen par print karna (print)',
    description: 'Terminal screen par message ya value print karne ke liye.',
    aliases: ['chapo', 'batao'],
    example: 'dikhao("Namaste Bharat!")\ndikhao(10 + 25)'
  },
  {
    token: 'pucho',
    python: 'input',
    category: 'Builtins',
    meaning: 'User se keyboard input lena (input)',
    description: 'Terminal par user se text input lene ke liye.',
    example: 'naam = pucho("Aapka naam kya hai? ")'
  },
  {
    token: 'lambai',
    python: 'len',
    category: 'Builtins',
    meaning: 'Items ki sankhya / length nikalna (len)',
    description: 'List, string ya dictionary mein kitne items hain yeh batata hai.',
    example: 'mitra = ["Amit", "Rohit", "Sneha"]\ndikhao(lambai(mitra)) # Output: 3'
  },
  {
    token: 'prakar',
    python: 'type',
    category: 'Builtins',
    meaning: 'Data type jan-na (type)',
    description: 'Variable ka type (int, str, list wagairah) check karta hai.',
    example: 'dikhao(prakar(100)) # Output: <class "int">'
  },
  {
    token: 'kram',
    python: 'range',
    category: 'Builtins',
    meaning: 'Numbers ki series banana (range)',
    description: 'Loop chalane ke liye sequence of numbers generate karta hai.',
    example: 'har i mein kram(0, 5):\n    dikhao(i)'
  },
  {
    token: 'purnank',
    python: 'int',
    category: 'Builtins',
    meaning: 'Integer number mein badalna (int)',
    description: 'Text ya decimal value ko seedhe pure number mein convert karta hai.',
    example: 'num = purnank("42")'
  },
  {
    token: 'dashamlav',
    python: 'float',
    category: 'Builtins',
    meaning: 'Point wale number mein badalna (float)',
    description: 'Value ko decimal point number mein badalta hai.',
    example: 'pi_val = dashamlav("3.14159")'
  },
  {
    token: 'akshar',
    python: 'str',
    category: 'Builtins',
    meaning: 'Text / String mein badalna (str)',
    description: 'Kisi bhi value ko readable text mein convert karta hai.',
    example: 's = akshar(12345)'
  },
  {
    token: 'kul_jod',
    python: 'sum',
    category: 'Builtins',
    meaning: 'Sabhi numbers ka total jod (sum)',
    description: 'List ke sabhi numbers ko aapas mein add karta hai.',
    example: 'numbers = [10, 20, 30]\ndikhao(kul_jod(numbers)) # Output: 60'
  },
  {
    token: 'adhiktam',
    python: 'max',
    category: 'Builtins',
    meaning: 'Sabse bada number (max)',
    description: 'List ya sequence mein se sabse badi value nikalta hai.',
    example: 'dikhao(adhiktam([15, 82, 44])) # Output: 82'
  },
  {
    token: 'nyuntam',
    python: 'min',
    category: 'Builtins',
    meaning: 'Sabse chhota number (min)',
    description: 'List ya sequence mein se sabse chhoti value nikalta hai.',
    example: 'dikhao(nyuntam([15, 82, 44])) # Output: 15'
  },
  {
    token: 'khol',
    python: 'open',
    category: 'Builtins',
    meaning: 'File open karna (open)',
    description: 'File ko padhne ya likhne ke liye open karta hai.',
    example: 'saath khol("log.txt", "r") jaise f:\n    dikhao(f.read())'
  },

  // Aliases (Bolchal ke aasan shabda)
  {
    token: 'andar',
    python: 'in',
    category: 'Aliases',
    meaning: '"mein" ka aasan bolchal ka alias (in)',
    description: 'har item andar collection (mein ki tarah bilkul same).',
    example: 'har x andar [1, 2, 3]:\n    dikhao(x)'
  },
  {
    token: 'shunya',
    python: 'None',
    category: 'Aliases',
    meaning: '"kuch_nahi" ka aasan alias (None)',
    description: 'Python ke None ko aap shunya bhi likh sakte hain.',
    example: 'res = shunya\nagar res hai shunya:\n    dikhao("Khali hai")'
  },
  {
    token: 'chapo',
    python: 'print',
    category: 'Aliases',
    meaning: '"dikhao" ka desi print alias (print)',
    description: 'Screen par print karne ka lokpriya desi alias.',
    example: 'chapo("Desi print command!")'
  },
  {
    token: 'batao',
    python: 'print',
    category: 'Aliases',
    meaning: '"dikhao" ka ek aur aasan print alias (print)',
    description: 'Screen par output dikhane ke liye.',
    example: 'batao("Yeh ek jankari hai")'
  },
  {
    token: 'shreni',
    python: 'class',
    category: 'Aliases',
    meaning: '"varg" ka class alias (class)',
    description: 'Class banate waqt shreni bhi likh sakte hain.',
    example: 'shreni Gadi:\n    chhod_do'
  },
  {
    token: 'sambhalo',
    python: 'except',
    category: 'Aliases',
    meaning: '"pakdo" ka exception handling alias (except)',
    description: 'Error sambhalne ke liye.',
    example: 'koshish:\n    x = 1/0\nsambhalo Exception:\n    dikhao("Error sambhal liya!")'
  },
  {
    token: 'aakhir_mein',
    python: 'finally',
    category: 'Aliases',
    meaning: '"antatah" ka aasan alias (finally)',
    description: 'Aakhir mein chalne wala clean-up block.',
    example: 'koshish:\n    chhod_do\naakhir_mein:\n    dikhao("Kaam done")'
  },
  {
    token: 'fenko',
    python: 'raise',
    category: 'Aliases',
    meaning: '"uthav" ka error phenkne wala alias (raise)',
    description: 'Apni taraf se error throw karne ke liye.',
    example: 'fenko RuntimeError("Critical error aayi")'
  },
  {
    token: 'lekar',
    python: 'with',
    category: 'Aliases',
    meaning: '"saath" ka context manager alias (with)',
    description: 'File ya resource ko open rakhne ke liye.',
    example: 'lekar khol("sample.txt") jaise f:\n    chhod_do'
  },
  {
    token: 'roop_mein',
    python: 'as',
    category: 'Aliases',
    meaning: '"jaise" ka alias (as)',
    description: 'Variables ko alias naam dene ke liye.',
    example: 'laao math roop_mein ganit\ndikhao(ganit.pi)'
  },
  {
    token: 'mitao',
    python: 'del',
    category: 'Aliases',
    meaning: '"hatao" ka aasan delete alias (del)',
    description: 'Item ya variable ko mitane ke liye.',
    example: 'd = {"a": 1}\nmitao d["a"]'
  },
  {
    token: 'dawa',
    python: 'assert',
    category: 'Aliases',
    meaning: '"daawa" ka short spelling alias (assert)',
    description: 'Condition check karne ke liye.',
    example: 'dawa 5 > 2'
  },
  {
    token: 'asthaniya',
    python: 'nonlocal',
    category: 'Aliases',
    meaning: '"asthanik" ka nonlocal scope alias',
    description: 'Outer function variable ko bind karne ke liye.',
    example: 'kaam outer():\n    x = 1\n    kaam inner():\n        asthaniya x\n        x = 5\n    inner()'
  },
  {
    token: 'milaao',
    python: 'match',
    category: 'Aliases',
    meaning: '"milao" ka phonetic alias (match)',
    description: 'Pattern matching keyword ka alternate roop.',
    example: 'milaao val:\n    sthiti 10:\n        dikhao("Dus mila")'
  },
  {
    token: 'vichaar',
    python: 'case',
    category: 'Aliases',
    meaning: '"sthiti" ka case pattern alias (case)',
    description: 'Match statement branch ke liye synonym.',
    example: 'milao val:\n    vichaar "admin":\n        dikhao("Admin login")'
  }
];
