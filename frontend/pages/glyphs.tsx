import React, { useEffect, useState } from 'react';
import RitualButtons from '../components/RitualButtons';
import GlyphLineageTree from '../components/GlyphLineageTree';
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import GeneAssistant from '@/components/GeneAssistant';

type LineageEntry = {
  svg: string;
  glyph: any;
  ritual?: string;
  timestamp?: string;
  insight?: string;
};

function downloadGlyph(svg: string, glyph: any, i: number) {
  // Download SVG
  const svgBlob = new Blob([svg], { type: 'image/svg+xml' });
  const svgUrl = URL.createObjectURL(svgBlob);
  const svgLink = document.createElement('a');
  svgLink.href = svgUrl;
  svgLink.download = `glyph_${i + 1}.svg`;
  svgLink.click();
  // Download JSON
  const jsonBlob = new Blob([JSON.stringify(glyph, null, 2)], { type: 'application/json' });
  const jsonUrl = URL.createObjectURL(jsonBlob);
  const jsonLink = document.createElement('a');
  jsonLink.href = jsonUrl;
  jsonLink.download = `glyph_${i + 1}.json`;
  jsonLink.click();
}

function downloadHistory(lineage: LineageEntry[]) {
  const jsonBlob = new Blob([JSON.stringify(lineage, null, 2)], { type: 'application/json' });
  const jsonUrl = URL.createObjectURL(jsonBlob);
  const jsonLink = document.createElement('a');
  jsonLink.href = jsonUrl;
  jsonLink.download = `glyph_lineage_history.json`;
  jsonLink.click();
}
function handleEvolve() {
  fetch('/api/glyph/evolve')
    .then(res => res.json())
    .then(data => {
      setGlyphSvg(data.svg);
      setGlyph(data.glyph);
      setLineage(lin => [...lin, {
        svg: data.svg,
        glyph: data.glyph,
        ritual: 'evolve',
        timestamp: new Date().toISOString()
      }]);
    });
}

function handleMutate() {
  fetch('/api/glyph/mutate')
    .then(res => res.json())
    .then(data => {
      setGlyphSvg(data.svg);
      setGlyph(data.glyph);
      setLineage(lin => [...lin, {
        svg: data.svg,
        glyph: data.glyph,
        ritual: 'mutate',
        timestamp: new Date().toISOString()
      }]);
    });
}

function handleReflect() {
  fetch('/api/oracle/reflect')
    .then(res => res.json())
    .then(data => {
      setOracleInsight(data.insight || '');
      setLineage(lin => [...lin, {
        svg: glyphSvg || '',
        glyph,
        ritual: 'reflect',
        timestamp: new Date().toISOString(),
        insight: data.insight
      }]);
    });
}

export default function GlyphsPage() {
  const [mode, setMode] = useState<'live' | 'test'>('live');
  const [glyphSvg, setGlyphSvg] = useState<string | null>(null);
  const [glyph, setGlyph] = useState<any>(null);
  const [lineage, setLineage] = useState<LineageEntry[]>([]);
  const [ghostGlyph, setGhostGlyph] = useState<{ svg: string; glyph: any; ritual?: string; timestamp?: string } | null>(null);
  const [showCommit, setShowCommit] = useState(false);
  const [dreaming, setDreaming] = useState(false);
  const [dreamPaused, setDreamPaused] = useState(false);
  const [dreamStep, setDreamStep] = useState(0);
  const [oracleInsight, setOracleInsight] = useState<string | null>(null);
  const [dreamLog, setDreamLog] = useState<any[]>([]);
  const dreamLoopRef = React.useRef<NodeJS.Timeout | null>(null);
  const [geneSuggestions, setGeneSuggestions] = useState<any[]>([]);

  useEffect(() => {
    const fetchGlyph = async () => {
      try {
        const res = await fetch(
          'http://localhost:8000/api/glyph/generate?steps=5&grammar=default&format=svg'
        );
        const svg = await res.text();
        const resJson = await fetch(
          'http://localhost:8000/api/glyph/generate?steps=5&grammar=default&format=json'
        );
        const glyphJson = await resJson.json();
        const now = new Date().toISOString();
        setGlyphSvg(svg);
        setGlyph(glyphJson);
        setLineage([{ svg, glyph: glyphJson, ritual: 'init', timestamp: now }]);
      } catch (error) {
        console.error('Error fetching glyph:', error);
      }
    };
    fetchGlyph();
  }, []);

  function setGlyphSvgAndUpdate(svg: string, glyph: any, ritual: string) {
    setGlyphSvg(svg);
    setGlyph(glyph);
    setLineage(prev => [...prev, { svg, glyph, ritual, timestamp: new Date().toISOString() }]);
  }

  function handleLineageClick(entry: any) {
    setGlyphSvgAndUpdate(entry.svg, entry.glyph, entry.ritual || 'manual');
  }
  const handleRestore = handleLineageClick;

  const handleCommit = () => {
    if (ghostGlyph) {
      setGlyphSvg(ghostGlyph.svg);
      setGlyph(ghostGlyph.glyph);
      setLineage((prev) => [...prev, ghostGlyph]);
      setGhostGlyph(null);
      setShowCommit(false);
    }
  };

  const handleCancel = () => {
    setGhostGlyph(null);
    setShowCommit(false);
  };

  async function dreamLoopStep() {
    if (dreamPaused) return;
    setDreamStep(s => s + 1);
    try {
      // Evolve
      const evolveRes = await fetch('/api/glyph/evolve?loop=true');
      const evolveData = await evolveRes.json();
      setLineage(lin => [...lin, { svg: evolveData.svg, glyph: evolveData.glyph, ritual: 'evolve', timestamp: new Date().toISOString() }]);
      setDreamLog(log => [...log, { type: 'evolve', ...evolveData, timestamp: new Date().toISOString() }]);
      // Mutate
      const mutateRes = await fetch('/api/glyph/mutate?loop=true');
      const mutateData = await mutateRes.json();
      setLineage(lin => [...lin, { svg: mutateData.svg, glyph: mutateData.glyph, ritual: 'mutate', timestamp: new Date().toISOString() }]);
      setDreamLog(log => [...log, { type: 'mutate', ...mutateData, timestamp: new Date().toISOString() }]);
      // Reflect
      const reflectRes = await fetch('/api/oracle/reflect?loop=true');
      const reflectData = await reflectRes.json();
      setOracleInsight(reflectData.insight || '');
      setDreamLog(log => [...log, { type: 'reflect', ...reflectData, timestamp: new Date().toISOString() }]);
      setTimeout(() => setOracleInsight(null), 3500);
    } catch (err) {
      setDreaming(false);
      if (dreamLoopRef.current) clearInterval(dreamLoopRef.current);
    }
  }

  function startDreamLoop() {
    setDreaming(true);
    setDreamPaused(false);
    setDreamStep(0);
    dreamLoopStep();
    dreamLoopRef.current = setInterval(dreamLoopStep, 5000);
  }
  function stopDreamLoop() {
    setDreaming(false);
    setDreamPaused(false);
    setDreamStep(0);
    if (dreamLoopRef.current) clearInterval(dreamLoopRef.current);
  }
  function pauseDreamLoop() {
    setDreamPaused(true);
  }
  function resumeDreamLoop() {
    setDreamPaused(false);
  }
  useEffect(() => {
    if (!dreaming && dreamLoopRef.current) {
      clearInterval(dreamLoopRef.current);
    }
    return () => {
      if (dreamLoopRef.current) clearInterval(dreamLoopRef.current);
    };
  }, [dreaming]);

  function downloadDreamLog() {
    const jsonBlob = new Blob([JSON.stringify(dreamLog, null, 2)], { type: 'application/json' });
    const jsonUrl = URL.createObjectURL(jsonBlob);
    const jsonLink = document.createElement('a');
    jsonLink.href = jsonUrl;
    jsonLink.download = `dream_log.json`;
    jsonLink.click();
  }

  function handleGeneSuggestion(ritualType: string) {
    if (ritualType === 'evolve') handleEvolve();
    else if (ritualType === 'mutate') handleMutate();
    else if (ritualType === 'reflect') handleReflect();
  }

  useEffect(() => {
    if (lineage.length >= 2) {
      const last = lineage[lineage.length - 1];
      const prev = lineage[lineage.length - 2];
      if (last.ritual === 'evolve' && prev.ritual === 'mutate') {
        setGeneSuggestions([
          {
            ritual: 'reflect',
            title: 'Consider Reflecting',
            message: 'You've evolved and mutated—reflect to extract meaning.',
          }
        ]);
      } else {
        setGeneSuggestions([]);
      }
    } else {
      setGeneSuggestions([]);
    }
  }, [lineage]);

  return (
    <div style={{ padding: '2rem', position: 'relative' }}>
      <h1>🧬 Codex Glyph Viewer</h1>
      <div style={{ marginBottom: 12 }}>
        <label style={{ fontWeight: 600, marginRight: 12 }}>Mode:</label>
        <button
          onClick={() => setMode(mode === 'live' ? 'test' : 'live')}
          style={{
            background: mode === 'live' ? '#0070f3' : '#f59e42',
            color: '#fff',
            border: 'none',
            borderRadius: 8,
            padding: '6px 18px',
            fontWeight: 600,
            fontSize: 15,
            cursor: 'pointer',
            marginRight: 8,
          }}
        >
          {mode === 'live' ? 'Live Mode' : 'Test Mode'}
        </button>
        <span style={{ color: '#888', fontSize: 14 }}>
          {mode === 'live'
            ? 'Rituals update glyph and lineage immediately.'
            : 'Rituals preview ghost glyphs. Commit to save.'}
        </span>
      </div>
      <div style={{ display: 'flex', gap: 16, alignItems: 'center', marginBottom: 16 }}>
        <RitualButtons glyph={glyph} setGlyphSvg={(svg, glyphJson) => setGlyphSvgAndUpdate(svg, glyphJson, 'ritual')} />
        <button
          onClick={dreaming ? stopDreamLoop : startDreamLoop}
          style={{
            background: dreaming ? '#ef4444' : '#2563eb',
            color: '#fff',
            border: 'none',
            borderRadius: 8,
            padding: '8px 22px',
            fontWeight: 700,
            fontSize: 16,
            cursor: 'pointer',
            boxShadow: dreaming ? '0 0 8px #ef4444' : '0 0 4px #2563eb',
            transition: 'background 0.2s',
          }}
        >
          🌀 {dreaming ? 'Stop Dream Loop' : 'Start Dream Loop'}
        </button>
        {dreaming && (
          dreamPaused ? (
            <button onClick={resumeDreamLoop} style={{ background: '#f59e42', color: '#fff', border: 'none', borderRadius: 8, padding: '8px 18px', fontWeight: 600, fontSize: 14, cursor: 'pointer' }}>Resume</button>
          ) : (
            <button onClick={pauseDreamLoop} style={{ background: '#6366f1', color: '#fff', border: 'none', borderRadius: 8, padding: '8px 18px', fontWeight: 600, fontSize: 14, cursor: 'pointer' }}>Pause</button>
          )
        )}
        <button
          onClick={downloadDreamLog}
          style={{ background: '#10b981', color: '#fff', border: 'none', borderRadius: 8, padding: '6px 18px', fontWeight: 600, fontSize: 14, cursor: 'pointer' }}
        >
          Download Dream Log
        </button>
        {dreaming && (
          <div style={{ marginLeft: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ color: '#6366f1', fontWeight: 600 }}>Dreaming…</span>
            <span className="dream-spinner" style={{ width: 18, height: 18, border: '3px solid #6366f1', borderTop: '3px solid #fff', borderRadius: '50%', display: 'inline-block', animation: 'spin 1s linear infinite' }} />
            <span style={{ color: '#888', fontSize: 13 }}>Step {dreamStep}</span>
          </div>
        )}
      </div>
      <GlyphLineageTree lineage={lineage} onRestore={handleRestore} />
      <div style={{ margin: '8px 0 24px 0', display: 'flex', alignItems: 'center', gap: 16 }}>
        <strong>Lineage:</strong>
        <button
          onClick={() => downloadHistory(lineage)}
          style={{ background: '#0070f3', color: '#fff', border: 'none', borderRadius: 8, padding: '6px 18px', fontWeight: 600, fontSize: 14, cursor: 'pointer' }}
        >
          Download History (JSON)
        </button>
      </div>
      <div style={{ display: 'flex', gap: 8, overflowX: 'auto', marginTop: 8 }}>
        <TransitionGroup component={null}>
          {lineage.map((entry, i) => (
            <CSSTransition key={i} timeout={350} classNames="fade">
              <div
                style={{
                  minWidth: 60,
                  minHeight: 60,
                  border: '1px solid #eee',
                  background:
                    entry.ritual === 'evolve' ? '#e0f2fe' :
                    entry.ritual === 'mutate' ? '#fef9c3' :
                    entry.ritual === 'reflect' ? '#ede9fe' : '#fafafa',
                  borderRadius: 6,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer',
                  position: 'relative',
                  boxShadow:
                    entry.ritual === 'evolve' ? '0 0 8px #2563eb' :
                    entry.ritual === 'mutate' ? '0 0 8px #f59e42' :
                    entry.ritual === 'reflect' ? '0 0 8px #6366f1' : undefined,
                  transition: 'background 0.3s, box-shadow 0.3s',
                }}
                title={`Restore glyph #${i + 1}`}
                onClick={() => handleLineageClick(entry)}
              >
                <div dangerouslySetInnerHTML={{ __html: entry.svg }} />
                <div style={{ display: 'flex', gap: 4, marginTop: 2 }}>
                  <button
                    onClick={e => { e.stopPropagation(); downloadGlyph(entry.svg, entry.glyph, i); }}
                    style={{ background: '#10b981', color: '#fff', border: 'none', borderRadius: 6, padding: '2px 8px', fontSize: 11, cursor: 'pointer' }}
                    title="Download SVG & JSON"
                  >
                    ⬇️
                  </button>
                </div>
                {entry.ritual && (
                  <div style={{ position: 'absolute', top: 2, right: 4, fontSize: 11, color: '#888' }}>
                    {entry.ritual}
                  </div>
                )}
                {entry.ritual === 'reflect' && entry.insight && (
                  <div style={{ position: 'absolute', bottom: 2, left: 4, fontSize: 11, color: '#6366f1' }} title={entry.insight}>
                    🧠
                  </div>
                )}
              </div>
            </CSSTransition>
          ))}
        </TransitionGroup>
      </div>
      {oracleInsight && (
        <div style={{ position: 'fixed', top: 40, right: 40, background: '#6366f1', color: '#fff', padding: '18px 28px', borderRadius: 16, fontWeight: 600, fontSize: 18, boxShadow: '0 4px 24px #6366f188', zIndex: 1000, pointerEvents: 'none', animation: 'fadeInOut 3.5s' }}>
          <span>🧠 Oracle: {oracleInsight}</span>
        </div>
      )}
      {ghostGlyph && showCommit && (
        <div style={{ margin: '18px 0', padding: 16, background: '#fffbe6', border: '1.5px solid #f59e42', borderRadius: 10 }}>
          <div style={{ fontWeight: 600, marginBottom: 8 }}>Ghost Glyph Preview (Test Mode)</div>
          <div
            dangerouslySetInnerHTML={{ __html: ghostGlyph.svg }}
            style={{ border: '1px solid #eee', background: '#fafafa', borderRadius: 6, minHeight: 60, minWidth: 60, display: 'inline-block', marginBottom: 8 }}
          />
          <div>
            <button
              onClick={handleCommit}
              style={{ background: '#10b981', color: '#fff', border: 'none', borderRadius: 8, padding: '8px 18px', fontWeight: 600, fontSize: 15, marginRight: 8, cursor: 'pointer' }}
            >
              Commit this glyph
            </button>
            <button
              onClick={handleCancel}
              style={{ background: '#ef4444', color: '#fff', border: 'none', borderRadius: 8, padding: '8px 18px', fontWeight: 600, fontSize: 15, cursor: 'pointer' }}
            >
              Cancel
            </button>
          </div>
        </div>
      )}
      <div
        dangerouslySetInnerHTML={{ __html: glyphSvg || '<p>Loading...</p>' }}
        style={{ marginTop: '2rem', border: '1px solid #ccc', padding: '1rem' }}
      />
      <GeneAssistant suggestions={geneSuggestions} onConfirm={handleGeneSuggestion} />
      <style>{`
        .fade-enter {
          opacity: 0;
          transform: scale(0.8);
        }
        .fade-enter-active {
          opacity: 1;
          transform: scale(1);
          transition: opacity 350ms, transform 350ms;
        }
        .fade-exit {
          opacity: 1;
          transform: scale(1);
        }
        .fade-exit-active {
          opacity: 0;
          transform: scale(0.8);
          transition: opacity 350ms, transform 350ms;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        @keyframes fadeInOut {
          0% { opacity: 0; }
          10% { opacity: 1; }
          90% { opacity: 1; }
          100% { opacity: 0; }
        }
      `}</style>
    </div>
  );
}

