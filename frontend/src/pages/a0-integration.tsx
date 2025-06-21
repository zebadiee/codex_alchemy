import React, { useState, useEffect } from 'react';
import Link from 'next/link';

interface A0Status {
  available: boolean;
  agents: string[];
  spells_count: number;
  has_lineage: boolean;
}

interface A0Spell {
  source: string;
  file: string;
  [key: string]: any;
}

interface A0SpellsResponse {
  spells: A0Spell[];
  total: number;
}

interface MergedVaults {
  codex_alchemy: any;
  a0: {
    spells: A0Spell[];
    lineage: any;
  };
  merged: {
    total_spells: number;
    total_glyphs: number;
    systems: string[];
  };
}

export default function A0Integration() {
  const [a0Status, setA0Status] = useState<A0Status | null>(null);
  const [a0Spells, setA0Spells] = useState<A0Spell[]>([]);
  const [mergedVaults, setMergedVaults] = useState<MergedVaults | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

  useEffect(() => {
    fetchA0Data();
  }, []);

  const fetchA0Data = async () => {
    try {
      setLoading(true);
      
      // Fetch A0 status
      const statusResponse = await fetch(`${API_BASE}/api/a0/status`);
      if (statusResponse.ok) {
        const status = await statusResponse.json();
        setA0Status(status);
      }

      // Fetch A0 spells
      const spellsResponse = await fetch(`${API_BASE}/api/a0/spells`);
      if (spellsResponse.ok) {
        const spellsData: A0SpellsResponse = await spellsResponse.json();
        setA0Spells(spellsData.spells);
      }

      // Fetch merged vaults
      const mergedResponse = await fetch(`${API_BASE}/api/a0/vault/merged`);
      if (mergedResponse.ok) {
        const merged = await mergedResponse.json();
        setMergedVaults(merged);
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch A0 data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white p-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold mb-8">A0 Integration</h1>
          <div className="animate-pulse">
            <div className="h-4 bg-gray-700 rounded w-1/4 mb-4"></div>
            <div className="h-4 bg-gray-700 rounded w-1/2 mb-4"></div>
            <div className="h-4 bg-gray-700 rounded w-3/4"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 text-white p-8">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl font-bold mb-8">A0 Integration</h1>
          <div className="bg-red-900 border border-red-700 rounded-lg p-4 mb-6">
            <h2 className="text-xl font-semibold mb-2">Error</h2>
            <p>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">A0 Integration</h1>
          <Link href="/" className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg">
            Back to Home
          </Link>
        </div>

        {/* A0 Status */}
        {a0Status && (
          <div className="bg-gray-800 rounded-lg p-6 mb-8">
            <h2 className="text-2xl font-semibold mb-4">A0 System Status</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-sm text-gray-400">Available</div>
                <div className={`text-lg font-semibold ${a0Status.available ? 'text-green-400' : 'text-red-400'}`}>
                  {a0Status.available ? 'Yes' : 'No'}
                </div>
              </div>
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-sm text-gray-400">Agents</div>
                <div className="text-lg font-semibold">{a0Status.agents.length}</div>
              </div>
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-sm text-gray-400">Spells</div>
                <div className="text-lg font-semibold">{a0Status.spells_count}</div>
              </div>
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-sm text-gray-400">Lineage</div>
                <div className={`text-lg font-semibold ${a0Status.has_lineage ? 'text-green-400' : 'text-red-400'}`}>
                  {a0Status.has_lineage ? 'Yes' : 'No'}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Available Agents */}
        {a0Status && a0Status.agents.length > 0 && (
          <div className="bg-gray-800 rounded-lg p-6 mb-8">
            <h2 className="text-2xl font-semibold mb-4">Available A0 Agents</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {a0Status.agents.map((agent, index) => (
                <div key={index} className="bg-gray-700 rounded-lg p-4">
                  <div className="text-lg font-semibold">{agent}</div>
                  <div className="text-sm text-gray-400 mt-2">Ready to invoke</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* A0 Spells */}
        {a0Spells.length > 0 && (
          <div className="bg-gray-800 rounded-lg p-6 mb-8">
            <h2 className="text-2xl font-semibold mb-4">A0 Spells ({a0Spells.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {a0Spells.map((spell, index) => (
                <div key={index} className="bg-gray-700 rounded-lg p-4">
                  <div className="text-lg font-semibold">{spell.file}</div>
                  <div className="text-sm text-gray-400 mt-2">Source: {spell.source}</div>
                  {spell.name && (
                    <div className="text-sm text-blue-400 mt-1">{spell.name}</div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Merged Vaults */}
        {mergedVaults && (
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">Unified Vault Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-sm text-gray-400">Total Spells</div>
                <div className="text-2xl font-bold text-blue-400">{mergedVaults.merged.total_spells}</div>
              </div>
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-sm text-gray-400">Total Glyphs</div>
                <div className="text-2xl font-bold text-green-400">{mergedVaults.merged.total_glyphs}</div>
              </div>
              <div className="bg-gray-700 rounded-lg p-4">
                <div className="text-sm text-gray-400">Systems</div>
                <div className="text-lg font-semibold">
                  {mergedVaults.merged.systems.join(' + ')}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="mt-8 flex gap-4">
          <Link href="/rituals" className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg">
            View Rituals
          </Link>
          <Link href="/glyphs" className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg">
            View Glyphs
          </Link>
          <Link href="/debug" className="bg-yellow-600 hover:bg-yellow-700 px-4 py-2 rounded-lg">
            Debug
          </Link>
        </div>
      </div>
    </div>
  );
} 