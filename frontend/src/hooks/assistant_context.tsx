import React, { createContext, useContext, useMemo } from 'react';

export interface AssistantContextType {
  isStaleGlyph: (glyphName: string) => boolean;
  isUnlinkedGlyph: (glyphName: string) => boolean;
  isRapidDrift: (glyphName: string) => boolean;
}

// Default: All functions return false until symbolic logic is added
const defaultContext: AssistantContextType = {
  isStaleGlyph: () => false,
  isUnlinkedGlyph: () => false,
  isRapidDrift: () => false,
};

const AssistantContext = createContext<AssistantContextType>(defaultContext);

interface AssistantProviderProps {
  children: React.ReactNode;
}

export const AssistantProvider = ({ children }: AssistantProviderProps) => {
  const isStaleGlyph = (glyphName: string): boolean => false;
  const isUnlinkedGlyph = (glyphName: string): boolean => false;
  const isRapidDrift = (glyphName: string): boolean => false;

  const value = useMemo(
    () => ({ isStaleGlyph, isUnlinkedGlyph, isRapidDrift }),
    []
  );

  return (
    <AssistantContext.Provider value={value}>
      {children}
    </AssistantContext.Provider>
  );
};

export const useAssistantContext = (): AssistantContextType =>
  useContext(AssistantContext); 