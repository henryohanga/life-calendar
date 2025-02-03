import type { CategoryColors, TimeMap } from '$lib/types/calendar';

export const elementColors = {
	Fire: '#ef4444', // red-500
	Earth: '#10b981', // emerald-500
	Air: '#3b82f6', // blue-500
	Water: '#0ea5e9' // sky-500
};

export const categoryColors: CategoryColors = {
	career: {
		base: '#4f46e5', // indigo-600
		bg: 'rgba(79, 70, 229, 0.1)',
		icon: '💼'
	},
	personal: {
		base: '#0891b2', // cyan-600
		bg: 'rgba(8, 145, 178, 0.1)',
		icon: '🌟'
	},
	rest: {
		base: '#059669', // emerald-600
		bg: 'rgba(5, 150, 105, 0.1)',
		icon: '🌿'
	},
	financial: {
		base: '#7c3aed', // violet-600
		bg: 'rgba(124, 58, 237, 0.1)',
		icon: '💰'
	}
};

export const timeMap: TimeMap = {
	morning: { start: '09:00', end: '12:00' },
	afternoon: { start: '13:00', end: '16:00' },
	evening: { start: '17:00', end: '20:00' },
	night: { start: '20:00', end: '23:00' }
};
