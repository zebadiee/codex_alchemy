import React, { useState, useEffect } from 'react';
import Link from 'next/link';

interface RefinedPaper {
  title: string;
  refined_summary: string;
  refined_at: string;
  sigil: string;
}

interface VaultEntry {
  refined_papers: RefinedPaper[];
}

export default function Glyphcyclopedia() {
  const [vaultData, setVaultData] = useState<VaultEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSigil, setSelectedSigil] = useState<string | null>(null);

  useEffect(() => {
    fetchVaultData();
  }, []);

  const fetchVaultData = async () => {
    try {
      // In a real implementation, this would be an API endpoint
      // For now, we'll simulate the data structure
      const mockData: VaultEntry[] = [
        {
          refined_papers: [
            {
              title: "Advanced AI Hallucination Detection Methods",
              refined_summary: "🔮 [Codex-20250622-002145]\nThis paper presents novel approaches to detect AI hallucination in large language models. The methods achieve 95% accuracy on benchmark datasets from 2023. Performance analysis shows significant improvements over existing techniques.\n\n# 🔍 Codex Note: Validate against benchmark X / real dataset Y\n# 📅 Codex Note: Check for more recent developments\n# ⚡ Codex Note: Consider computational efficiency trade-offs",
              refined_at: "2025-06-22T00:21:45.290090",
              sigil: "🔮 [Codex-20250622-002145]"
            },
            {
              title: "Neural Network Optimization Techniques",
              refined_summary: "🔮 [Codex-20250622-002145]\nWe explore various optimization strategies for deep neural networks, focusing on computational efficiency and accuracy trade-offs. The research builds upon 2024 developments in transformer architectures.\n# 📅 Codex Note: Check for more recent developments\n# ⚡ Codex Note: Consider computational efficiency trade-offs",
              refined_at: "2025-06-22T00:21:45.290098",
              sigil: "🔮 [Codex-20250622-002145]"
            }
          ]
        }
      ];
      
      setVaultData(mockData);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching vault data:', error);
      setLoading(false);
    }
  };

  const allPapers = vaultData.flatMap(entry => entry.refined_papers);
  
  const filteredPapers = allPapers.filter(paper =>
    paper.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    paper.refined_summary.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const uniqueSigils = [...new Set(allPapers.map(paper => paper.sigil))];

  const papersToShow = selectedSigil 
    ? filteredPapers.filter(paper => paper.sigil === selectedSigil)
    : filteredPapers;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading Glyphcyclopedia...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">🔮 Glyphcyclopedia</h1>
              <p className="text-gray-600">Symbolic Research Vault & Refined Knowledge</p>
            </div>
            <Link href="/" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              ← Back to Dashboard
            </Link>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-2xl font-bold text-blue-600">{allPapers.length}</div>
            <div className="text-gray-600">Total Papers</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-2xl font-bold text-green-600">{uniqueSigils.length}</div>
            <div className="text-gray-600">Unique Sigils</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-2xl font-bold text-purple-600">
              {new Set(allPapers.map(p => p.refined_at.split('T')[0])).size}
            </div>
            <div className="text-gray-600">Refinement Days</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <div className="text-2xl font-bold text-orange-600">
              {allPapers.filter(p => p.refined_summary.includes('🔍')).length}
            </div>
            <div className="text-gray-600">Validation Notes</div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white p-6 rounded-lg shadow mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search Papers
              </label>
              <input
                type="text"
                placeholder="Search by title or content..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Filter by Sigil
              </label>
              <select
                value={selectedSigil || ''}
                onChange={(e) => setSelectedSigil(e.target.value || null)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Sigils</option>
                {uniqueSigils.map(sigil => (
                  <option key={sigil} value={sigil}>{sigil}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Papers Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {papersToShow.map((paper, index) => (
            <div key={index} className="bg-white rounded-lg shadow-lg overflow-hidden">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-xl font-semibold text-gray-900 flex-1">
                    {paper.title}
                  </h3>
                  <span className="text-sm text-gray-500 ml-2">
                    {new Date(paper.refined_at).toLocaleDateString()}
                  </span>
                </div>
                
                <div className="mb-4">
                  <span className="inline-block bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">
                    {paper.sigil}
                  </span>
                </div>

                <div className="prose prose-sm max-w-none">
                  <div className="whitespace-pre-wrap text-gray-700">
                    {paper.refined_summary}
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="flex items-center text-sm text-gray-500">
                    <span>Refined: {new Date(paper.refined_at).toLocaleString()}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {papersToShow.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">🔮</div>
            <h3 className="text-xl font-medium text-gray-900 mb-2">No papers found</h3>
            <p className="text-gray-600">Try adjusting your search or sigil filter.</p>
          </div>
        )}
      </div>
    </div>
  );
} 