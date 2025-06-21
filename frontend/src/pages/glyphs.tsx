import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Grid, Card, CardContent, Paper, Chip } from '@mui/material';

interface VaultGlyph {
  name: string;
  vector: number[];
  hash: string;
}

const GlyphsPage: React.FC = () => {
  const [glyphs, setGlyphs] = useState<VaultGlyph[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchGlyphs = async () => {
    console.log('🔄 Fetching glyphs...');
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/vault/glyphs');
      console.log('📡 Glyphs response status:', response.status);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('✅ Glyphs loaded:', data);
      setGlyphs(data);
    } catch (error) {
      console.error('❌ Failed to fetch glyphs:', error);
      setError('Failed to load evolved glyphs from the vault');
    }
    setLoading(false);
  };

  useEffect(() => {
    console.log('🚀 GlyphsPage mounted, fetching data...');
    fetchGlyphs();
  }, []);

  // Debug: Log glyphs whenever they change
  useEffect(() => {
    console.log('📊 Current glyphs state:', glyphs);
  }, [glyphs]);

  const renderGlyphCard = (glyph: VaultGlyph) => (
    <Card key={glyph.hash} sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {glyph.name}
        </Typography>
        <Box sx={{ mb: 2 }}>
          <Chip 
            label={`Hash: ${glyph.hash.slice(0, 8)}...`} 
            size="small" 
            variant="outlined" 
            sx={{ mb: 1 }}
          />
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          Vector (first 4 values):
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {glyph.vector.slice(0, 4).map((val, idx) => (
            <Chip 
              key={idx}
              label={val.toFixed(3)} 
              size="small" 
              variant="outlined"
            />
          ))}
        </Box>
        <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
          Full vector: {glyph.vector.length} dimensions
        </Typography>
      </CardContent>
    </Card>
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Evolved Glyphs from the Codex Vault
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        These are the evolved glyphs recovered from your ritual evolution process.
      </Typography>
      
      {/* Debug info */}
      <Box sx={{ mb: 3, p: 2, bgcolor: 'grey.100', fontSize: '0.8em' }}>
        <Typography variant="caption">
          Debug: {loading ? 'Loading...' : error ? 'Error occurred' : `${glyphs.length} glyphs loaded`}
        </Typography>
      </Box>
      
      {loading && (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography>Loading evolved glyphs...</Typography>
        </Paper>
      )}
      
      {error && (
        <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'error.light' }}>
          <Typography color="error">{error}</Typography>
        </Paper>
      )}
      
      {!loading && !error && (
        <>
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Found {glyphs.length} evolved glyphs
            </Typography>
          </Box>
          
          <Grid container spacing={3}>
            {glyphs.map(renderGlyphCard)}
          </Grid>
        </>
      )}
    </Container>
  );
};

export default GlyphsPage; 