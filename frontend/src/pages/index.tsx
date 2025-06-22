import React from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import Link from 'next/link';
import GeneAssistant from '../components/GeneAssistant';

const Dashboard: React.FC = () => {
  return (
    <>
      <Container maxWidth="md" sx={{ mt: 8 }}>
        <Typography variant="h3" gutterBottom>Spiral Codex Dashboard</Typography>
        <Typography variant="h6" gutterBottom>
          Welcome to your living, evolving knowledge system.
        </Typography>
        <Box mt={4} display="flex" gap={2} flexWrap="wrap">
          <Link href="/rituals" passHref legacyBehavior>
            <Button variant="contained" color="primary">Rituals</Button>
          </Link>
          <Link href="/glyphs" passHref legacyBehavior>
            <Button variant="outlined" color="primary">Glyphs</Button>
          </Link>
          <Link href="/a0-integration" passHref legacyBehavior>
            <Button variant="outlined" color="secondary">A0 Integration</Button>
          </Link>
          <Link href="/glyphcyclopedia" passHref legacyBehavior>
            <Button variant="outlined" color="secondary">Glyphcyclopedia</Button>
          </Link>
          <Link href="/sigil-tree" passHref legacyBehavior>
            <Button variant="outlined" color="info">Sigil Tree</Button>
          </Link>
          <Link href="/debug" passHref legacyBehavior>
            <Button variant="outlined" color="error">Debug</Button>
          </Link>
          <Button variant="outlined" disabled>Research Lineage (coming soon)</Button>
        </Box>
        
        {/* Gene Assistant Info */}
        <Box mt={6} p={3} bgcolor="background.paper" borderRadius={2} border={1} borderColor="divider">
          <Typography variant="h6" gutterBottom color="primary">
            🤖 Gene Assistant
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            Your symbolic AI companion is ready to assist with rituals, vaults, and glyphs. 
            Press <strong>Ctrl+Shift+G</strong> (or <strong>Cmd+Shift+G</strong> on Mac) to summon Gene anytime.
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Gene understands your current context and can provide targeted assistance for dream loops, 
            vault comparisons, synchronization, and symbolic evolution.
          </Typography>
        </Box>
      </Container>
      
      {/* Gene Assistant Component */}
      <GeneAssistant />
    </>
  );
};

export default Dashboard; 