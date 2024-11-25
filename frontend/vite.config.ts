import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// Exporta a configuração do Vite
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': '/src', 
        },
    },
});
