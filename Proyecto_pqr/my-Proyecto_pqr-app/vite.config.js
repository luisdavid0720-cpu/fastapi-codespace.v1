import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      '/get_': { target: 'http://localhost:8000', changeOrigin: true },
      '/create_': { target: 'http://localhost:8000', changeOrigin: true },
      '/update_': { target: 'http://localhost:8000', changeOrigin: true },
      '/delete_': { target: 'http://localhost:8000', changeOrigin: true },
    }
  }
});