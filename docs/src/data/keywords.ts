import { KeywordInfo } from '../types';

export const KEYWORDS_DATA: KeywordInfo[] = [
  // Statements & Control Flow
  {
    token: 'agar',
    python: 'if',
    category: 'Statements',
    meaning: 'Shart janchne ke liye (Conditional branch)',
    description: 'Agar di gayi shart sahi (True) hoti hai toh yeh block execute hota hai.',
    example: 'agar umar >= 18:\n    dikhao("Aap vote de sakte hain")'
  },
  {
    token: 'warna',
    python: 'else',
    category: 'Statements',
    meaning: 'Vikalp shart (Alternative branch)',
    description: 'Agar koi bhi shart sahi na ho, toh warna block execute hota hai.',
    example: 'agar sankhya > 0:\n    dikhao("Dhanatmak")\nwarna:\n    dikhao("Rinatmak ya zero")'
  },
  {
    token: 'warna_agar',
    python: 'elif',
    category: 'Statements',
    meaning: 'Doosri shart (Secondary condition)',
    description: 'Pichhli shart galat hone par doosri shart check karne ke liye.',
    example: 'agar ank >= 90:\n    dikhao("A Grade")\nwarna_agar ank >= 75:\n    dikhao("B Grade")\nwarna:\n    dikhao("Pass")'
  },
  {
    token: 'jabtak',
    python: 'while',
    category: 'Statements',
    meaning: 'Shart aadharit loop (While loop)',
    description: 'Jab tak di gayi shart sahi rahegi, tab tak block baar-baar chalega.',
    example: 'ginti = 1\njabtak ginti <= 3:\n    dikhao(f"Ginti: {ginti}")\n    ginti = ginti + 1'
  },
  {
    token: 'har',
    python: 'for',
    category: 'Statements',
    meaning: 'Iteration loop (For loop)',
    description: 'Kisi list, string ya range ke har element par traverse karne ke liye.',
    example: 'har i mein kram(1, 4):\n    dikhao(f"Iteration: {i}")'
  },
  {
    token: 'mein',
    python: 'in',
    category: 'Statements',
    meaning: 'Sadasyata ya iteration target (Membership / In)',
    description: 'Iteration mein collection specify karne ya membership janchne ke liye.',
    aliases: ['andar'],
    example: 'har naam mein ["Aarav", "Priya"]:\n    dikhao("Namaste", naam)'
  },
  {
    token: 'ruko',
    python: 'break',
    category: 'Statements',
    meaning: 'Loop se turant bahar nikalna (Break)',
    description: 'Chalu loop ko turant terminate kar deta hai.',
    example: 'har n mein kram(1, 10):\n    agar n == 5:\n        ruko\n    dikhao(n)'
  },
  {
    token: 'aage_bado',
    python: 'continue',
    category: 'Statements',
    meaning: 'Agli iteration par jana (Continue)',
    description: 'Bache huye code ko skip karke loop ki agli cycle shuru karta hai.',
    example: 'har n mein kram(1, 6):\n    agar n % 2 == 0:\n        aage_bado\n    dikhao(f"Visham sankhya: {n}")'
  },
  {
    token: 'chhod_do',
    python: 'pass',
    category: 'Statements',
    meaning: 'Kuch na karein (No-operation placeholder)',
    description: 'Khali block ya placeholder ki tarah istemal hota hai.',
    example: 'kaam abhi_baki_hai():\n    chhod_do'
  },
  {
    token: 'kaam',
    python: 'def',
    category: 'Statements',
    meaning: 'Function paribhashit karna (Function definition)',
    description: 'Reusable block of code banata hai jo arguments le sakta hai.',
    example: 'kaam jod(a, b):\n    wapas a + b\n\nnatija = jod(10, 20)'
  },
  {
    token: 'varg',
    python: 'class',
    category: 'Statements',
    meaning: 'Class paribhashit karna (Class definition)',
    description: 'Object-oriented programming ke liye custom blueprint ya class banata hai.',
    aliases: ['shreni'],
    example: 'varg User:\n    kaam __init__(khood, naam):\n        khood.naam = naam\n\nu = User("Neeraj")'
  },
  {
    token: 'wapas',
    python: 'return',
    category: 'Statements',
    meaning: 'Value wapas bhejna (Return statement)',
    description: 'Function se result caller ko wapas bhejta hai.',
    example: 'kaam varg(x):\n    wapas x * x'
  },
  {
    token: 'upaj',
    python: 'yield',
    category: 'Statements',
    meaning: 'Generator value produce karna (Yield)',
    description: 'Generator function mein ek ek karke value yield karta hai.',
    example: 'kaam ginti_dhara():\n    upaj 1\n    upaj 2\n    upaj 3'
  },
  {
    token: 'sookshm',
    python: 'lambda',
    category: 'Statements',
    meaning: 'Anonymous function (Inline Lambda)',
    description: 'Ek line ka concise bina-naam wala function banata hai.',
    example: 'varg_fn = sookshm x: x ** 2\ndikhao(varg_fn(5))'
  },
  {
    token: 'koshish',
    python: 'try',
    category: 'Statements',
    meaning: 'Error sambhavit block (Try block)',
    description: 'Aise code ko wrap karta hai jismein runtime exception aa sakti hai.',
    example: 'koshish:\n    natija = 10 / 0\npakdo ZeroDivisionError jaise e:\n    dikhao("Division error pakda gaya!")'
  },
  {
    token: 'pakdo',
    python: 'except',
    category: 'Statements',
    meaning: 'Exception capture karna (Catch / Except)',
    description: 'Koshish block mein aayi hui exception ko handle karta hai.',
    aliases: ['sambhalo'],
    example: 'koshish:\n    x = int("abc")\npakdo ValueError:\n    dikhao("Invalid number format")'
  },
  {
    token: 'antatah',
    python: 'finally',
    category: 'Statements',
    meaning: 'Aakhir mein chalne wala block (Finally)',
    description: 'Yeh block hamesha chalta hai chahe error aaye ya na aaye.',
    aliases: ['aakhir_mein'],
    example: 'koshish:\n    dikhao("Kaam chalu")\nantatah:\n    dikhao("Resource clean-up sampann")'
  },
  {
    token: 'uthav',
    python: 'raise',
    category: 'Statements',
    meaning: 'Exception trigger karna (Raise error)',
    description: 'Custom ya standard runtime exception explicitly trigger karta hai.',
    aliases: ['fenko'],
    example: 'agar umar < 0:\n    uthav ValueError("Umar negative nahi ho sakti!")'
  },
  {
    token: 'daawa',
    python: 'assert',
    category: 'Statements',
    meaning: 'Shart ka dawa karna (Assertion check)',
    description: 'Shart galat hone par AssertionError uthata hai.',
    aliases: ['dawa'],
    example: 'daawa 10 > 0, "Dus positive hona chahiye"'
  },
  {
    token: 'saath',
    python: 'with',
    category: 'Statements',
    meaning: 'Context manager ke sath block (With block)',
    description: 'Resource management (jaise file open/close) ko automatically handle karta hai.',
    aliases: ['lekar'],
    example: 'saath khol("data.txt", "w") jaise f:\n    f.write("Namaste")'
  },
  {
    token: 'jaise',
    python: 'as',
    category: 'Statements',
    meaning: 'Alias ya variable binding (As binding)',
    description: 'Import, with, ya except mein variable bind karne ke liye upyog hota hai.',
    aliases: ['roop_mein'],
    example: 'se math laao sqrt jaise varg_mool\ndikhao(varg_mool(16))'
  },
  {
    token: 'sarvavyapi',
    python: 'global',
    category: 'Statements',
    meaning: 'Global variable scope declare karna (Global variable)',
    description: 'Function ke andar module-level global variable ko modify karne ke liye.',
    example: 'ginti = 0\nkaam badhao():\n    sarvavyapi ginti\n    ginti = ginti + 1'
  },
  {
    token: 'asthanik',
    python: 'nonlocal',
    category: 'Statements',
    meaning: 'Enclosing scope variable declare karna (Nonlocal variable)',
    description: 'Nested functions mein outer variable ko bind karne ke liye.',
    aliases: ['asthaniya'],
    example: 'kaam bahar():\n    x = 10\n    kaam andar():\n        asthanik x\n        x = 20\n    andar()'
  },
  {
    token: 'hatao',
    python: 'del',
    category: 'Statements',
    meaning: 'Variable ya item delete karna (Delete statement)',
    description: 'Memory se variable ya collection item ko remove karta hai.',
    aliases: ['mitao'],
    example: 'data = {"a": 1, "b": 2}\nhatao data["b"]'
  },
  {
    token: 'laao',
    python: 'import',
    category: 'Statements',
    meaning: 'Module ya library import karna (Import)',
    description: 'Hinglish ya Python modules ko program mein include karta hai.',
    example: 'laao math\ndikhao(math.pi)'
  },
  {
    token: 'se',
    python: 'from',
    category: 'Statements',
    meaning: 'Module se specific members lana (From import)',
    description: 'Kisi module se vishesh function, class ya variable import karne ke liye.',
    example: 'se datetime laao datetime\ndikhao(datetime.now())'
  },
  {
    token: 'asamanantar',
    python: 'async',
    category: 'Statements',
    meaning: 'Asynchronous function ya construct (Async definition)',
    description: 'Coroutine function, async for, ya async with define karne ke liye.',
    example: 'asamanantar kaam fetch_data():\n    intezaar asyncio.sleep(1)\n    wapas "Data prapt hua"'
  },
  {
    token: 'intezaar',
    python: 'await',
    category: 'Statements',
    meaning: 'Async execution ka intezaar (Await expression)',
    description: 'Coroutine ke complete hone tak pause karke result yield karta hai.',
    example: 'natija = intezaar fetch_data()'
  },

  // Soft Keywords (Pattern Matching)
  {
    token: 'milao',
    python: 'match',
    category: 'Soft Keywords',
    meaning: 'Pattern matching shuru karna (Structural Match)',
    description: 'Python 3.10+ match statement ki tarah value ki structure match karta hai.',
    aliases: ['milaao'],
    example: 'milao status_code:\n    sthiti 200:\n        dikhao("OK")\n    sthiti 404:\n        dikhao("Not Found")'
  },
  {
    token: 'sthiti',
    python: 'case',
    category: 'Soft Keywords',
    meaning: 'Pattern match branch (Case branch)',
    description: 'Match statement ke andar individual case pattern define karta hai.',
    aliases: ['vichaar'],
    example: 'milao command:\n    sthiti ["quit", reason]:\n        dikhao(f"Quitting: {reason}")\n    sthiti _:\n        dikhao("Anya command")'
  },

  // Operators
  {
    token: 'aur',
    python: 'and',
    category: 'Operators',
    meaning: 'Tarkik AND operator (Logical AND)',
    description: 'Dono shartein sahi hone par hi True return karta hai.',
    example: 'agar umar >= 18 aur nagrik == sahi:\n    dikhao("Vote dene yogya")'
  },
  {
    token: 'ya',
    python: 'or',
    category: 'Operators',
    meaning: 'Tarkik OR operator (Logical OR)',
    description: 'Dono mein se koi ek shart sahi hone par True return karta hai.',
    example: 'agar sunday == sahi ya chhutti == sahi:\n    dikhao("Aaram karein")'
  },
  {
    token: 'nahi',
    python: 'not',
    category: 'Operators',
    meaning: 'Tarkik NOT operator (Logical Negation)',
    description: 'Boolean condition ko ulta (invert) karta hai.',
    example: 'agar nahi logged_in:\n    dikhao("Kripya login karein")'
  },
  {
    token: 'hai',
    python: 'is',
    category: 'Operators',
    meaning: 'Identity comparison operator (Identity check)',
    description: 'Object identity check karta hai (kya dono same memory instance hain).',
    example: 'agar natija hai kuch_nahi:\n    dikhao("Koi result nahi mila")'
  },

  // Literals
  {
    token: 'sahi',
    python: 'True',
    category: 'Literals',
    meaning: 'Satya / True boolean value',
    description: 'Boolean true value ko represent karta hai.',
    example: 'sakriya = sahi\nagar sakriya:\n    dikhao("Khata sakriya hai")'
  },
  {
    token: 'galat',
    python: 'False',
    category: 'Literals',
    meaning: 'Asatya / False boolean value',
    description: 'Boolean false value ko represent karta hai.',
    example: 'safal = galat\nagar nahi safal:\n    dikhao("Dobara koshish karein")'
  },
  {
    token: 'kuch_nahi',
    python: 'None',
    category: 'Literals',
    meaning: 'Null / Shunya object (None singleton)',
    description: 'Python ke None singleton object ko represent karta hai.',
    aliases: ['shunya'],
    example: 'data = kuch_nahi\nagar data hai kuch_nahi:\n    dikhao("Data abhi khali hai")'
  },

  // Built-in Core Functions
  {
    token: 'dikhao',
    python: 'print',
    category: 'Builtins',
    meaning: 'Output display karna (Standard output)',
    description: 'Terminal par text ya expressions ko print karta hai.',
    aliases: ['chapo', 'batao'],
    example: 'dikhao("Namaste Bharat!")\ndikhao(10 + 25)'
  },
  {
    token: 'pucho',
    python: 'input',
    category: 'Builtins',
    meaning: 'User se input lena (Standard input)',
    description: 'User se interactive keyboard input string format mein leta hai.',
    example: 'naam = pucho("Aapka naam kya hai? ")'
  },
  {
    token: 'lambai',
    python: 'len',
    category: 'Builtins',
    meaning: 'Sequence ki length nikalna (Length)',
    description: 'List, string, tuple ya dictionary ke items ki sankhya batata hai.',
    example: 'mitra = ["Amit", "Rohit", "Sneha"]\ndikhao(lambai(mitra)) # Output: 3'
  },
  {
    token: 'prakar',
    python: 'type',
    category: 'Builtins',
    meaning: 'Object ka data type jan-na (Type inspection)',
    description: 'Kisi bhi variable ya value ka Python type class return karta hai.',
    example: 'dikhao(prakar(100)) # Output: <class "int">'
  },
  {
    token: 'kram',
    python: 'range',
    category: 'Builtins',
    meaning: 'Sankhya sequence banana (Range generator)',
    description: 'Loops ke liye numbers ka sequence generate karta hai.',
    example: 'har i mein kram(0, 5):\n    dikhao(i)'
  },
  {
    token: 'purnank',
    python: 'int',
    category: 'Builtins',
    meaning: 'Integer mein badalna (Convert to int)',
    description: 'Value ya string ko integer number mein cast karta hai.',
    example: 'num = purnank("42")'
  },
  {
    token: 'dashamlav',
    python: 'float',
    category: 'Builtins',
    meaning: 'Float mein badalna (Convert to float)',
    description: 'Value ya string ko decimal / floating point number mein cast karta hai.',
    example: 'pi_val = dashamlav("3.14159")'
  },
  {
    token: 'akshar',
    python: 'str',
    category: 'Builtins',
    meaning: 'String mein badalna (Convert to str)',
    description: 'Kisi bhi value ko readable string representation mein badalta hai.',
    example: 's = akshar(12345)'
  },
  {
    token: 'kul_jod',
    python: 'sum',
    category: 'Builtins',
    meaning: 'Numbers ka kul jod (Sum of iterable)',
    description: 'Sequence ke sabhi numbers ka total calculation karta hai.',
    example: 'sankhyayein = [10, 20, 30]\ndikhao(kul_jod(sankhyayein)) # Output: 60'
  },
  {
    token: 'adhiktam',
    python: 'max',
    category: 'Builtins',
    meaning: 'Sabse badi sankhya (Maximum value)',
    description: 'Sequence mein sabse badi value return karta hai.',
    example: 'dikhao(adhiktam([15, 82, 44])) # Output: 82'
  },
  {
    token: 'nyuntam',
    python: 'min',
    category: 'Builtins',
    meaning: 'Sabse chhoti sankhya (Minimum value)',
    description: 'Sequence mein sabse chhoti value return karta hai.',
    example: 'dikhao(nyuntam([15, 82, 44])) # Output: 15'
  },
  {
    token: 'khol',
    python: 'open',
    category: 'Builtins',
    meaning: 'File open karna (File descriptor)',
    description: 'File reading ya writing ke liye file stream open karta hai.',
    example: 'saath khol("log.txt", "r") jaise f:\n    dikhao(f.read())'
  },

  // Aliases (Representing alternative natural words)
  {
    token: 'andar',
    python: 'in',
    category: 'Aliases',
    meaning: '"mein" ka aam bolchal ka alias',
    description: 'har item andar collection (Same as mein).',
    example: 'har x andar [1, 2, 3]:\n    dikhao(x)'
  },
  {
    token: 'shunya',
    python: 'None',
    category: 'Aliases',
    meaning: '"kuch_nahi" ka aam bolchal ka alias',
    description: 'None singleton ko shunya se bhi likha ja sakta hai.',
    example: 'res = shunya\nagar res hai shunya:\n    dikhao("Khali")'
  },
  {
    token: 'chapo',
    python: 'print',
    category: 'Aliases',
    meaning: '"dikhao" ka print alias',
    description: 'Screen par print karne ka lokpriya desi alias.',
    example: 'chapo("Desi print command!")'
  },
  {
    token: 'batao',
    python: 'print',
    category: 'Aliases',
    meaning: '"dikhao" ka informative alias',
    description: 'Screen par display karne ka ek aur bolchal roop.',
    example: 'batao("Yeh ek jankari hai")'
  },
  {
    token: 'shreni',
    python: 'class',
    category: 'Aliases',
    meaning: '"varg" ka class alias',
    description: 'Class banate waqt shreni ka prayog bhi kiya ja sakta hai.',
    example: 'shreni Gadi:\n    chhod_do'
  },
  {
    token: 'sambhalo',
    python: 'except',
    category: 'Aliases',
    meaning: '"pakdo" ka exception handling alias',
    description: 'Exception pakadne aur sambhalne ke liye.',
    example: 'koshish:\n    x = 1/0\nsambhalo Exception:\n    dikhao("Sambhal liya!")'
  },
  {
    token: 'aakhir_mein',
    python: 'finally',
    category: 'Aliases',
    meaning: '"antatah" ka finally alias',
    description: 'Koshish/pakdo ke aakhir mein clean-up block.',
    example: 'koshish:\n    chhod_do\naakhir_mein:\n    dikhao("Done")'
  },
  {
    token: 'fenko',
    python: 'raise',
    category: 'Aliases',
    meaning: '"uthav" ka raise exception alias',
    description: 'Explicitly exception throw karne ke liye.',
    example: 'fenko RuntimeError("Critical rukawat")'
  },
  {
    token: 'lekar',
    python: 'with',
    category: 'Aliases',
    meaning: '"saath" ka context manager alias',
    description: 'Resource context hold karne ke liye.',
    example: 'lekar khol("sample.txt") jaise f:\n    chhod_do'
  },
  {
    token: 'roop_mein',
    python: 'as',
    category: 'Aliases',
    meaning: '"jaise" ka formal binding alias',
    description: 'Variables ko as binding dene ke liye.',
    example: 'laao math roop_mein ganit\ndikhao(ganit.pi)'
  },
  {
    token: 'mitao',
    python: 'del',
    category: 'Aliases',
    meaning: '"hatao" ka deletion alias',
    description: 'Collection item ya variable hatane/mitane ke liye.',
    example: 'd = {"a": 1}\nmitao d["a"]'
  },
  {
    token: 'dawa',
    python: 'assert',
    category: 'Aliases',
    meaning: '"daawa" ka assertion spelling alias',
    description: 'Assertion condition verify karne ke liye.',
    example: 'dawa 5 > 2'
  },
  {
    token: 'asthaniya',
    python: 'nonlocal',
    category: 'Aliases',
    meaning: '"asthanik" ka nonlocal scope alias',
    description: 'Enclosing function scope variable ko bind karne ke liye.',
    example: 'kaam outer():\n    x = 1\n    kaam inner():\n        asthaniya x\n        x = 5\n    inner()'
  },
  {
    token: 'milaao',
    python: 'match',
    category: 'Aliases',
    meaning: '"milao" ka pattern match phonetic alias',
    description: 'Phonetic variation for match keyword.',
    example: 'milaao val:\n    sthiti 10:\n        dikhao("Dus")'
  },
  {
    token: 'vichaar',
    python: 'case',
    category: 'Aliases',
    meaning: '"sthiti" ka case pattern alias',
    description: 'Match statement branch ke liye synonym.',
    example: 'milao val:\n    vichaar "admin":\n        dikhao("Admin panel")'
  }
];
