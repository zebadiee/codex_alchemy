import type { AppProps } from 'next/app';
import React from 'react';
import { AssistantProvider } from '../hooks/assistant_context';

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AssistantProvider>
      <Component {...pageProps} />
    </AssistantProvider>
  );
} 