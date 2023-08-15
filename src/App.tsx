import { QueryClient, QueryClientProvider } from 'react-query';
import './App.css';
import { AudioPlayer } from './components/AudioPlayer';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AudioPlayer />
    </QueryClientProvider>
  );
}

export default App;
