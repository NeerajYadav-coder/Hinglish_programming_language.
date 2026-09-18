import React, { useState } from 'react';
import { Check, Copy } from 'lucide-react';

interface CodeBlockProps {
  code: string;
  language?: string;
  filename?: string;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({
  code,
  language = 'hin',
  filename
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="code-window">
      <div className="code-header">
        <div className="window-dots">
          <span className="window-dot dot-red" />
          <span className="window-dot dot-yellow" />
          <span className="window-dot dot-green" />
          {filename && (
            <span style={{ marginLeft: '8px', fontSize: '0.8rem', color: '#a0a0b0', fontFamily: 'JetBrains Mono, monospace' }}>
              {filename}
            </span>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <span className="code-lang-label">{language}</span>
          <button
            onClick={handleCopy}
            className={`code-copy-btn ${copied ? 'copied' : ''}`}
            title="Code copy karein"
          >
            {copied ? (
              <>
                <Check size={13} />
                <span>Copy ho gaya!</span>
              </>
            ) : (
              <>
                <Copy size={13} />
                <span>Copy Karein</span>
              </>
            )}
          </button>
        </div>
      </div>

      <div className="code-body">
        <pre><code>{code.trim()}</code></pre>
      </div>
    </div>
  );
};
