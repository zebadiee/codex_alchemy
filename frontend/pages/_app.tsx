import FloatingGeneAssistant from '../components/FloatingGeneAssistant';

function MyApp({ Component, pageProps }) {
  return (
    <>
      <FloatingGeneAssistant />
      <Component {...pageProps} />
    </>
  );
}

export default MyApp; 