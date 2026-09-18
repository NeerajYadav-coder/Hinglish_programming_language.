export interface KeywordInfo {
  token: string;
  python: string;
  category: 'Statements' | 'Operators' | 'Literals' | 'Builtins' | 'Soft Keywords' | 'Aliases';
  meaning: string;
  description: string;
  aliases?: string[];
  example: string;
}

export interface ExampleItem {
  id: string;
  title: string;
  category: string;
  description: string;
  hinglishCode: string;
  pythonCode: string;
  output: string;
  keyConcepts: string[];
}

export interface NavItem {
  id: string;
  title: string;
  titleHi: string;
  iconName: string;
  badge?: string;
}

export interface NavSection {
  title: string;
  items: NavItem[];
}
