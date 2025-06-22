import React, { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useFloating, offset, flip, shift, autoUpdate } from '@floating-ui/react';

interface GeneContext {
  page: string;
  recentRitual?: string;
  vault?: string;
  glyphs?: number;
  lastSync?: string;
}

interface GeneResponse {
  response: string;
  suggestions?: string[];
  ritual_hint?: string;
  offline?: boolean;
}

export const GeneAssistant: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [response, setResponse] = useState<GeneResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isOffline, setIsOffline] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  const { refs, floatingStyles } = useFloating({
    placement: 'top',
    middleware: [offset(10), flip(), shift()],
    whileElementsMounted: autoUpdate,
  });

  // Hotkey handler
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'G') {
        e.preventDefault();
        setIsOpen(true);
        setTimeout(() => inputRef.current?.focus(), 100);
      }
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  // Get current context
  const getContext = (): GeneContext => {
    return {
      page: router.pathname,
      recentRitual: localStorage.getItem('lastRitualRun') || undefined,
      vault: localStorage.getItem('activeVault') || 'default',
      glyphs: parseInt(localStorage.getItem('glyphCount') || '0'),
      lastSync: localStorage.getItem('lastSyncTime') || undefined,
    };
  };

  // Send request to Gene
  const sendToGene = async (prompt: string): Promise<GeneResponse> => {
    const context = getContext();
    
    try {
      const response = await fetch('/api/assistant/respond', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, context }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setIsOffline(false);
      return data;
    } catch (error) {
      console.log('Gene offline, using local oracle...');
      setIsOffline(true);
      return await useLocalOracle(prompt, context);
    }
  };

  // Local oracle for offline mode
  const useLocalOracle = async (prompt: string, context: GeneContext): Promise<GeneResponse> => {
    // Simple local responses based on context
    const responses = {
      ritual: {
        response: "I sense you're working with rituals. Try `python unified_cli.py dream-loop` to evolve your glyphs, or `codex-alchemy vault diff default evolved` to see the changes.",
        suggestions: ['dream-loop', 'vault diff', 'sync-status'],
        ritual_hint: 'The dream loop ritual evolves glyphs with 🧬 mutations.'
      },
      vault: {
        response: "Your vault contains symbolic entities. Use `codex-alchemy vault list` to see all sigils, or `codex-alchemy vault reflect new_sigil` to create a reflection.",
        suggestions: ['vault list', 'vault reflect', 'vault restore'],
        ritual_hint: 'Vaults preserve glyphs under unique sigils for ritual work.'
      },
      default: {
        response: "I am Gene, your symbolic assistant. I can help with rituals, vaults, glyphs, and the dream loop evolution. What would you like to explore?",
        suggestions: ['rituals', 'vaults', 'glyphs', 'dream-loop'],
        ritual_hint: 'Press Ctrl+Shift+G anytime to summon me.'
      }
    };

    // Determine context and return appropriate response
    if (prompt.toLowerCase().includes('ritual') || context.recentRitual) {
      return responses.ritual;
    } else if (prompt.toLowerCase().includes('vault') || context.vault) {
      return responses.vault;
    } else {
      return responses.default;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setIsLoading(true);
    setResponse(null);

    try {
      const geneResponse = await sendToGene(input);
      setResponse(geneResponse);
      setInput('');
    } catch (error) {
      setResponse({
        response: "I'm having trouble connecting right now. Try again in a moment.",
        offline: true
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestion = (suggestion: string) => {
    setInput(suggestion);
    inputRef.current?.focus();
  };

  if (!isOpen) {
    return (
      <button
        ref={refs.setReference}
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 bg-purple-600 hover:bg-purple-700 text-white rounded-full p-3 shadow-lg transition-all duration-200 z-50"
        title="Summon Gene (Ctrl+Shift+G)"
      >
        <GeneIcon className="w-6 h-6" />
      </button>
    );
  }

  return (
    <>
      <div
        ref={refs.setFloating}
        style={floatingStyles}
        className="bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 w-96 max-h-96 overflow-hidden z-50"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <GeneIcon className="w-5 h-5" />
              <span className="font-semibold">Gene Assistant</span>
              {isOffline && (
                <span className="text-xs bg-yellow-500 text-yellow-900 px-2 py-1 rounded">
                  OFFLINE
                </span>
              )}
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <XIcon className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-4 space-y-4 max-h-80 overflow-y-auto">
          {/* Response */}
          {response && (
            <div className="space-y-3">
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                <p className="text-sm text-gray-800 dark:text-gray-200">
                  {response.response}
                </p>
                {response.ritual_hint && (
                  <div className="mt-2 p-2 bg-purple-50 dark:bg-purple-900/20 rounded border-l-4 border-purple-400">
                    <p className="text-xs text-purple-700 dark:text-purple-300">
                      💡 {response.ritual_hint}
                    </p>
                  </div>
                )}
              </div>
              
              {/* Suggestions */}
              {response.suggestions && (
                <div className="flex flex-wrap gap-2">
                  {response.suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestion(suggestion)}
                      className="text-xs bg-purple-100 dark:bg-purple-800 text-purple-700 dark:text-purple-300 px-2 py-1 rounded hover:bg-purple-200 dark:hover:bg-purple-700 transition-colors"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Loading */}
          {isLoading && (
            <div className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-purple-600"></div>
              <span className="text-sm">Gene is thinking...</span>
            </div>
          )}

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="space-y-2">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask Gene about rituals, vaults, or glyphs..."
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm"
              disabled={isLoading}
            />
            <div className="flex justify-between items-center text-xs text-gray-500 dark:text-gray-400">
              <span>Press Enter to send</span>
              <span>Esc to close</span>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

// Icon Components
const GeneIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg className={className} fill="currentColor" viewBox="0 0 20 20">
    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const XIcon: React.FC<{ className?: string }> = ({ className }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
  </svg>
);

export default GeneAssistant; 