import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, List, ListItem, ListItemText, TextField, Button, Paper } from '@mui/material';

interface Glyph {
  id: number;
  symbol: string;
}

interface Ritual {
  id: number;
  name: string;
  description: string;
  glyphs?: Glyph[];
}

const RitualsPage: React.FC = () => {
  const [rituals, setRituals] = useState<Ritual[]>([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRituals = async () => {
    console.log('🔄 Fetching rituals...');
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/gene/rituals_with_glyphs');
      console.log('📡 Response status:', response.status);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('✅ Rituals loaded:', data);
      setRituals(data);
    } catch (error) {
      console.error('❌ Failed to fetch rituals:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch rituals');
    }
    setLoading(false);
  };

  useEffect(() => {
    console.log('🚀 RitualsPage mounted, fetching data...');
    fetchRituals();
  }, []);

  // Debug: Log rituals whenever they change
  useEffect(() => {
    console.log('📊 Current rituals state:', rituals);
  }, [rituals]);

  const handleAdd = async () => {
    if (!name.trim()) return;
    try {
      const response = await fetch('http://localhost:8000/api/gene/rituals', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, description }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      setName('');
      setDescription('');
      fetchRituals();
    } catch (error) {
      console.error('Failed to add ritual:', error);
      setError(error instanceof Error ? error.message : 'Failed to add ritual');
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Rituals</Typography>
      
      {error && (
        <Paper sx={{ p: 2, mb: 2, bgcolor: 'error.light', color: 'error.contrastText' }}>
          <Typography variant="h6">Error</Typography>
          <Typography>{error}</Typography>
        </Paper>
      )}
      
      <Paper sx={{ p: 2, mb: 4 }}>
        <Typography variant="h6">Add New Ritual</Typography>
        <Box display="flex" gap={2} mt={2}>
          <TextField label="Name" value={name} onChange={e => setName(e.target.value)} />
          <TextField label="Description" value={description} onChange={e => setDescription(e.target.value)} />
          <Button variant="contained" onClick={handleAdd}>Add</Button>
        </Box>
      </Paper>
      
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6">
          All Rituals ({rituals.length}) 
          {loading && ' - Loading...'}
        </Typography>
        
        {/* Debug info */}
        <Box sx={{ mb: 2, p: 1, bgcolor: 'grey.100', fontSize: '0.8em' }}>
          <Typography variant="caption">
            Debug: {loading ? 'Loading...' : rituals.length === 0 ? 'No rituals found' : `${rituals.length} rituals loaded`}
          </Typography>
        </Box>
        
        <List>
          {loading ? (
            <ListItem><ListItemText primary="Loading rituals..." /></ListItem>
          ) : rituals.length === 0 ? (
            <ListItem><ListItemText primary="No rituals found" /></ListItem>
          ) : (
            rituals.map(r => (
              <ListItem key={r.id} divider>
                <ListItemText
                  primary={<>
                    {r.name} {r.glyphs && r.glyphs.length > 0 && (
                      <span style={{ fontSize: '1.5em', marginLeft: 8 }}>
                        {r.glyphs.map(g => g.symbol).join(' ')}
                      </span>
                    )}
                  </>}
                  secondary={r.description}
                />
              </ListItem>
            ))
          )}
        </List>
      </Paper>
    </Container>
  );
};

export default RitualsPage; 