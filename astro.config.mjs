// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  // 项目仓库部署: URL 为 https://zing110.github.io/zing.github.io/
  // base 必须与仓库名一致,否则资源路径会 404
  site: 'https://zing110.github.io',
  base: '/zing.github.io/',

  vite: {
    plugins: [tailwindcss()]
  },

  integrations: [react()]
});