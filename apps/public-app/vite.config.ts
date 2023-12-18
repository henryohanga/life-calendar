import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

import postcss from './postcss.config';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	},
	css: {
		postcss
	}
});
