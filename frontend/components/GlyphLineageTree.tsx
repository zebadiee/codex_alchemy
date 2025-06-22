import React from 'react';
import ReactFlow, {
  MiniMap, Controls, Background,
  useNodesState, useEdgesState, Node, Edge,
} from 'react-flow-renderer';

interface GlyphLineageTreeProps {
  lineage: { svg: string; glyph: any; ritual?: string; timestamp?: string }[];
  onRestore: (glyph: any) => void;
}

export default function GlyphLineageTree({ lineage, onRestore }: GlyphLineageTreeProps) {
  const nodes: Node[] = lineage.map((entry, i) => ({
    id: String(i),
    data: {
      label: (
        <div
          onClick={() => onRestore(entry.glyph)}
          title={`Ritual: ${entry.ritual || 'Unknown'}\n${entry.timestamp || ''}`}
          style={{ width: 40, height: 40, cursor: 'pointer', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}
        >
          <div dangerouslySetInnerHTML={{ __html: entry.svg }} />
          <div style={{ fontSize: 10, color: '#0070f3', marginTop: 2 }}>{entry.ritual || ''}</div>
          <div style={{ fontSize: 9, color: '#888' }}>{entry.timestamp ? entry.timestamp.slice(11,19) : ''}</div>
        </div>
      ),
    },
    position: { x: i * 140, y: 0 },
    style: {
      width: 60,
      height: 60,
      background: '#fff',
      border: '1.5px solid #0070f3',
      borderRadius: 8,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    },
  }));

  const edges: Edge[] = lineage.slice(1).map((_, i) => ({
    id: `e${i}-${i + 1}`,
    source: String(i),
    target: String(i + 1),
    animated: true,
    style: { stroke: '#0070f3', strokeWidth: 2 },
  }));

  const [flowNodes] = useNodesState(nodes);
  const [flowEdges] = useEdgesState(edges);

  return (
    <div style={{ width: '100%', height: 160, margin: '24px 0' }}>
      <ReactFlow
        nodes={flowNodes}
        edges={flowEdges}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        zoomOnScroll={false}
        zoomOnPinch={false}
        panOnScroll={true}
        minZoom={0.5}
        maxZoom={1.5}
        defaultZoom={1}
        fitView
      >
        <MiniMap />
        <Controls showInteractive={false} />
        <Background color="#e0e7ef" gap={16} />
      </ReactFlow>
    </div>
  );
} 