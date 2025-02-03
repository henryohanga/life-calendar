<script lang="ts">
	import { elementColors, categoryColors } from '$lib/constants/calendar';
	import type { GoodDateResponse } from '$lib/types';
	import { formatDate } from '$lib/utils/dates';
	import ZodiacInfo from './ZodiacInfo.svelte';
	import CategoryRecommendations from './CategoryRecommendations.svelte';
	import GoodDatesCalendar from './GoodDatesCalendar.svelte';
	import { fade, fly, scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { onMount, onDestroy } from 'svelte';
	import { writable } from 'svelte/store';

	export let results: GoodDateResponse;

	// Track component state
	let state: 'initial' | 'loading' | 'loaded' | 'error' = results?.zodiac_sign
		? 'loaded'
		: 'initial';

	// Loading steps for animation
	const loadingSteps = [
		'Analyzing celestial alignments...',
		'Calculating astrological influences...',
		'Identifying power periods...',
		'Generating personalized recommendations...'
	];
	const currentStep = writable(0);
	let stepInterval: NodeJS.Timeout;

	// Track active view
	let activeView: 'month' | 'week' | 'list' = 'month';
	let currentDate = new Date();

	// Format current month
	$: currentMonthDisplay = new Intl.DateTimeFormat('en-US', {
		month: 'long',
		year: 'numeric'
	}).format(currentDate);

	// Start loading animation
	function startLoadingAnimation() {
		currentStep.set(0);
		stepInterval = setInterval(() => {
			currentStep.update((step) => (step + 1) % loadingSteps.length);
		}, 2000);
	}

	// Stop loading animation
	function stopLoadingAnimation() {
		if (stepInterval) {
			clearInterval(stepInterval);
			stepInterval = undefined;
		}
	}

	// Update state based on results
	$: {
		if (!results) {
			state = 'initial';
			stopLoadingAnimation();
		} else if (!results.zodiac_sign) {
			state = 'loading';
			startLoadingAnimation();
		} else {
			state = 'loaded';
			stopLoadingAnimation();
		}
	}

	// Cleanup on component destroy
	onDestroy(() => {
		stopLoadingAnimation();
	});

	// Group dates by month for better organization
	$: datesByMonth =
		results && results.dates && results.dates.length > 0
			? results.dates.reduce(
					(acc, date) => {
						const month = date.substring(0, 7);
						if (!acc[month]) acc[month] = [];
						acc[month].push(date);
						return acc;
					},
					{} as Record<string, string[]>
				)
			: {};

	// Get power periods for highlighting
	$: powerPeriods =
		results?.zodiac_sign && results.zodiac_sign.power_periods
			? results.zodiac_sign.power_periods
			: [];
	$: powerDates = new Set(powerPeriods.flatMap((period) => period.dates));

	// Extract recommendations
	$: recommendations = {
		career: [] as string[],
		personal: [] as string[],
		rest: [] as string[],
		financial: [] as string[]
	};

	// Process recommendations
	$: {
		if (results?.zodiac_sign && results.zodiac_sign.date_specific_advice) {
			Object.entries(results.zodiac_sign.date_specific_advice).forEach(([date, dateInfo]) => {
				if (dateInfo?.activities && dateInfo.activities.length > 0) {
					const category = dateInfo.category;
					if (category in recommendations) {
						recommendations[category].push(...dateInfo.activities);
					}
				}
			});

			// Deduplicate and limit recommendations
			Object.keys(recommendations).forEach((key) => {
				const category = key as keyof typeof recommendations;
				recommendations[category] = [...new Set(recommendations[category])].slice(0, 3);
			});
		}
	}

	// Format category names for display
	const formatCategory = (category: string) => {
		return category.charAt(0).toUpperCase() + category.slice(1);
	};

	// Get category color
	const getCategoryColor = (category: string) => {
		const colors = {
			career: 'var(--color-primary)',
			personal: 'var(--color-secondary)',
			rest: 'var(--color-tertiary)',
			financial: 'var(--color-quaternary)'
		};
		return colors[category as keyof typeof colors] || 'var(--color-primary)';
	};

	// Add selectedDate state
	let selectedDate: string | null = null;

	// Fix the dateSpecificAdvice path
	$: dateSpecificAdvice = results?.zodiac_sign?.date_specific_advice || {};

	// Add function to handle date selection
	function handleDateSelect(date: string) {
		selectedDate = date;
	}

	function changeView(view: typeof activeView) {
		activeView = view;
	}

	function navigateDate(direction: 'prev' | 'next' | 'today') {
		const newDate = new Date(currentDate);
		if (direction === 'prev') {
			newDate.setMonth(newDate.getMonth() - 1);
		} else if (direction === 'next') {
			newDate.setMonth(newDate.getMonth() + 1);
		} else {
			newDate.setTime(Date.now());
		}
		currentDate = newDate;
	}

	// Format element color with opacity
	function getElementColor(element: string): string {
		const color = elementColors[element as keyof typeof elementColors];
		return color ? `${color}33` : '#f8fafc'; // 33 is 20% opacity in hex
	}

	let showPanel = false;
</script>

{#if state === 'initial'}
	<!-- Initial state - show nothing -->
{:else if state === 'loading'}
	<div class="loading-container" in:fade={{ duration: 300 }}>
		<div class="loading-content" in:scale={{ duration: 300, start: 0.95 }}>
			<div class="loading-spinner" />
			{#key $currentStep}
				<p in:fade={{ duration: 200 }}>{loadingSteps[$currentStep]}</p>
			{/key}
			<div class="loading-progress">
				<div class="progress-bar" />
			</div>
			<div class="loading-steps">
				{#each loadingSteps as step, i}
					<div class="step-dot" class:active={i === $currentStep} />
				{/each}
			</div>
		</div>
	</div>
{:else if state === 'loaded' && results?.zodiac_sign}
	<div class="app-container">
		<aside class="side-panel">
			<div class="side-panel-header">
				<div class="brand">
					<svg class="calendar-icon" viewBox="0 0 24 24" width="24" height="24">
						<path
							fill="currentColor"
							d="M19,4H17V3a1,1,0,0,0-2,0V4H9V3A1,1,0,0,0,7,3V4H5A2,2,0,0,0,3,6V20a2,2,0,0,0,2,2H19a2,2,0,0,0,2-2V6A2,2,0,0,0,19,4Zm0,16H5V10H19ZM19,8H5V6H7V7A1,1,0,0,0,9,7V6h6V7a1,1,0,0,0,2,0V6h2Z"
						/>
					</svg>
					<h1>Good Dates</h1>
				</div>
			</div>

			<div class="side-panel-content">
				<div class="zodiac-profile">
					<div class="zodiac-badge">
						<span class="zodiac-symbol">{results.zodiac_sign.symbol}</span>
						<span class="zodiac-name">{results.zodiac_sign.name}</span>
						<span
							class="element-tag"
							style="background: {getElementColor(results.zodiac_sign.element)}"
						>
							{results.zodiac_sign.element}
						</span>
					</div>
				</div>

				<div class="zodiac-section">
					<h4 class="section-title">Your Zodiac Profile</h4>
					<ZodiacInfo zodiacSign={results.zodiac_sign} />
				</div>

				<div class="recommendations-section">
					<h4 class="section-title">Personalized Recommendations</h4>
					<CategoryRecommendations recommendations={results.zodiac_sign.recommendations} />
				</div>
			</div>
		</aside>

		<div class="main-section">
			<header class="app-header">
				<div class="header-content">
					<div class="toolbar">
						<button class="today-button" on:click={() => navigateDate('today')}>Today</button>
						<div class="date-navigation">
							<button class="nav-button" on:click={() => navigateDate('prev')}>
								<span class="icon">‹</span>
							</button>
							<button class="nav-button" on:click={() => navigateDate('next')}>
								<span class="icon">›</span>
							</button>
						</div>
						<h2 class="current-date">{currentMonthDisplay}</h2>
					</div>
					<div class="header-right">
						<div class="view-controls">
							<div class="view-switcher">
								<button
									class="view-option"
									class:active={activeView === 'month'}
									on:click={() => changeView('month')}
								>
									<span>Month</span>
								</button>
								<button
									class="view-option"
									class:active={activeView === 'week'}
									on:click={() => changeView('week')}
								>
									<span>Week</span>
								</button>
							</div>
						</div>
					</div>
				</div>
			</header>

			<main class="calendar-content">
				<GoodDatesCalendar {results} {currentDate} view={activeView} />
			</main>
		</div>
	</div>
{:else}
	<div class="error-container" in:fade>
		<div class="error-content" in:scale={{ duration: 300, start: 0.95 }}>
			<h2>Oops! Something went wrong</h2>
			<p>We couldn't load your personalized dates. Please try again.</p>
			<button class="retry-button" on:click={() => window.location.reload()}> Try Again </button>
		</div>
	</div>
{/if}

<style>
	:root {
		--header-height: 56px;
		--side-panel-width: 280px;
		--primary-color: #1a73e8;
		--primary-light: #e8f0fe;
		--primary-dark: #1557b0;
		--surface-color: #ffffff;
		--background-color: #f6f8fc;
		--text-primary: #0f172a;
		--text-secondary: #475569;
		--border-color: #e2e8f0;
		--accent-color: #1a73e8;
		--radius-lg: 16px;
		--radius-md: 8px;
		--radius-sm: 4px;
		--spacing-xs: 0.5rem;
		--spacing-sm: 1rem;
		--spacing-md: 1.5rem;
		--spacing-lg: 2rem;
		--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
		--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
		--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
	}

	:global(body) {
		background: var(--color-surface-variant, #f8fafc);
		margin: 0;
		padding: 0;
		min-height: 100vh;
		overflow-y: auto;
	}

	.app-container {
		display: flex;
		height: 100vh;
		background: var(--background-color);
	}

	.app-header {
		height: var(--header-height);
		background: var(--surface-color);
		border-bottom: 1px solid var(--border-color);
		position: sticky;
		top: 0;
		z-index: 10;
		width: 100%;
	}

	.header-content {
		margin: 0 auto;
		padding: 0 1.5rem;
		height: 100%;
		display: flex;
		justify-content: space-between;
		align-items: center;
		max-width: none;
	}

	.header-left {
		display: flex;
		align-items: center;
		gap: 2rem;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.brand-icon {
		font-size: 1.5rem;
	}

	.header-left h1 {
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--primary-color);
		margin: 0;
	}

	.zodiac-info {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.zodiac-badge {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 0.75rem;
		background: var(--background-color);
		border-radius: var(--radius-md);
		border: 1px solid var(--border-color);
	}

	.zodiac-symbol {
		font-size: 1.25rem;
	}

	.zodiac-name {
		font-weight: 500;
		color: var(--text-primary);
	}

	.main-section {
		flex: 1;
		margin-left: var(--side-panel-width);
		display: flex;
		flex-direction: column;
		min-width: 0;
	}

	.calendar-content {
		flex: 1;
		display: flex;
		min-width: 0;
		min-height: 0;
	}

	.calendar-wrapper {
		height: 100%;
		position: relative;
	}

	.calendar-container {
		background: var(--surface-color);
		box-sizing: border-box;
		height: 100%;
		width: 100%;
		padding: 0;
	}

	.calendar-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: var(--spacing-md);
		padding: var(--spacing-md) var(--spacing-lg);
		border-bottom: 1px solid var(--border-color);
	}

	.calendar-title h3 {
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--text-primary);
		margin: 0;
		margin-bottom: var(--spacing-xs);
	}

	.calendar-subtitle {
		color: var(--text-secondary);
		margin: 0;
		font-size: 0.875rem;
	}

	.action-button {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--primary-light);
		color: var(--primary-color);
		border: none;
		border-radius: var(--radius-md);
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s;
	}

	.action-button:hover {
		background: var(--primary-color);
		color: white;
	}

	.section-title {
		font-size: 1.125rem;
		font-weight: 600;
		color: var(--text-primary);
		margin: 0;
		margin-bottom: var(--spacing-md);
	}

	.info-panel {
		position: absolute;
		top: 0;
		right: -var(--panel-width);
		width: var(--panel-width);
		height: 100%;
		display: flex;
		flex-direction: column;
		gap: var(--spacing-lg);
		overflow-y: auto;
		background: var(--surface-color);
		border-left: 1px solid var(--border-color);
		transition: transform 0.3s ease;
		padding: var(--spacing-lg);
		box-sizing: border-box;
		z-index: 20;
		box-shadow: -4px 0 16px rgba(0, 0, 0, 0.1);
	}

	.info-panel.panel-open {
		transform: translateX(-100%);
	}

	.panel-toggle {
		position: absolute;
		left: -24px;
		top: 50%;
		transform: translateY(-50%);
		width: 24px;
		height: 48px;
		background: var(--surface-color);
		border: 1px solid var(--border-color);
		border-right: none;
		border-radius: var(--radius-md) 0 0 var(--radius-md);
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		color: var(--text-secondary);
		font-size: 1rem;
		transition: all 0.2s;
	}

	.panel-toggle:hover {
		background: var(--primary-light);
		color: var(--primary-color);
	}

	.loading-container {
		position: fixed;
		inset: 0;
		display: flex;
		justify-content: center;
		align-items: center;
		background: var(--color-surface-variant, #f8fafc);
		z-index: 50;
	}

	.loading-content {
		text-align: center;
		background: var(--color-surface, white);
		border-radius: 12px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
		padding: 2rem;
		max-width: 400px;
		width: 90%;
	}

	.loading-container p {
		font-size: 1.125rem;
		color: var(--color-on-surface-variant, #64748b);
		margin: 1rem 0;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 3px solid var(--color-surface-variant, #f8fafc);
		border-top-color: var(--color-primary, #4f46e5);
		border-radius: 50%;
		margin: 0 auto;
		animation: spin 1s linear infinite;
	}

	.loading-progress {
		width: 100%;
		height: 4px;
		background: var(--color-surface-variant, #f8fafc);
		border-radius: 2px;
		overflow: hidden;
		margin-top: 1rem;
	}

	.progress-bar {
		width: 30%;
		height: 100%;
		background: var(--color-primary, #4f46e5);
		border-radius: 2px;
		animation: progress 2s ease-in-out infinite;
	}

	.error-container {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: calc(100vh - 4rem);
		padding: 2rem;
	}

	.error-content {
		text-align: center;
		background: var(--color-surface, white);
		border-radius: 12px;
		padding: 2rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
		max-width: 400px;
		width: 90%;
	}

	.error-content h2 {
		color: var(--color-on-surface, #1f2937);
		margin-bottom: 1rem;
	}

	.retry-button {
		margin-top: 1.5rem;
		padding: 0.75rem 1.5rem;
		background: var(--color-primary, #4f46e5);
		color: white;
		border: none;
		border-radius: 6px;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s;
	}

	.retry-button:hover {
		background: var(--color-primary-dark, #4338ca);
		transform: translateY(-1px);
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	@keyframes progress {
		0% {
			transform: translateX(-100%);
		}
		50% {
			transform: translateX(100%);
		}
		100% {
			transform: translateX(300%);
		}
	}

	.loading-steps {
		display: flex;
		justify-content: center;
		gap: 0.5rem;
		margin-top: 1rem;
	}

	.step-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--color-surface-variant, #f8fafc);
		transition: all 0.3s ease;
	}

	.step-dot.active {
		background: var(--color-primary, #4f46e5);
		transform: scale(1.2);
	}

	.element-tag {
		font-size: 0.75rem;
		padding: 0.25rem 0.75rem;
		border-radius: 1rem;
		font-weight: 500;
	}

	.view-controls {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}

	.view-switcher {
		display: flex;
		background: var(--primary-light);
		padding: 0.25rem;
		border-radius: var(--radius-md);
		border: 1px solid var(--border-color);
	}

	.view-option {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		border: none;
		background: transparent;
		color: var(--text-secondary);
		font-weight: 500;
		cursor: pointer;
		border-radius: var(--radius-sm);
		transition: all 0.2s;
		font-size: 0.875rem;
	}

	.view-option.active {
		background: var(--primary-color);
		color: white;
	}

	.today-button {
		padding: 0.5rem 1.25rem;
		background: var(--primary-color);
		color: white;
		border: none;
		border-radius: var(--radius-md);
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s;
		height: 36px;
	}

	.today-button:hover {
		background: var(--primary-dark);
		box-shadow: var(--shadow-sm);
	}

	.date-navigation {
		display: flex;
		align-items: center;
		gap: 0.25rem;
	}

	.nav-button {
		width: 32px;
		height: 32px;
		border: none;
		background: transparent;
		color: var(--text-secondary);
		cursor: pointer;
		border-radius: 50%;
		transition: all 0.2s;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1.25rem;
	}

	.nav-button:hover {
		background: var(--primary-light);
		color: var(--primary-color);
	}

	.current-date {
		font-size: 1.375rem;
		font-weight: 400;
		color: var(--text-primary);
		margin: 0;
		margin-left: 1rem;
	}

	.calendar-icon {
		color: var(--primary-color);
	}

	.toolbar {
		display: flex;
		align-items: center;
		gap: 1rem;
		margin-left: 2rem;
	}

	.side-panel {
		width: var(--side-panel-width);
		background: var(--surface-color);
		border-right: 1px solid var(--border-color);
		height: 100vh;
		overflow-y: auto;
		position: fixed;
		left: 0;
		top: 0;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		z-index: 20;
		box-shadow: var(--shadow-sm);
	}

	.side-panel-header {
		padding: 1rem;
		border-bottom: 1px solid var(--border-color);
	}

	.side-panel-content {
		padding: 1rem;
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}

	.main-section {
		flex: 1;
		margin-left: var(--side-panel-width);
		display: flex;
		flex-direction: column;
	}

	.calendar-content {
		flex: 1;
		padding: 0;
	}

	:global(.calendar-content > *) {
		flex: 1;
		width: 100%;
		height: 100%;
		min-width: 0;
	}

	:global(.calendar-content .fc) {
		width: 100% !important;
		height: 100% !important;
		background: white;
		display: flex;
		flex-direction: column;
		min-width: 0;
	}

	:global(.calendar-content .fc-view-harness) {
		height: 100% !important;
		flex: 1;
		min-width: 0;
	}

	:global(.calendar-content .fc-view) {
		height: 100% !important;
		min-width: 0;
	}

	:global(.fc-header-toolbar) {
		display: none !important;
	}

	:global(.fc-view-harness) {
		background: white;
		border: none !important;
	}

	:global(.fc td, .fc th) {
		border-color: var(--border-color) !important;
	}

	:global(.fc-day-today) {
		background: var(--primary-light) !important;
	}

	:global(.fc-scrollgrid) {
		border: none !important;
		width: 100% !important;
	}

	:global(.fc-scrollgrid td:last-of-type) {
		border-right: none !important;
	}

	:global(.fc-scrollgrid tr:last-child td) {
		border-bottom: none !important;
	}

	:global(.fc-scroller) {
		height: 100% !important;
	}

	:global(.fc-view-harness-active) {
		height: 100% !important;
	}

	:global(.fc-scrollgrid-sync-table) {
		height: 100% !important;
	}

	:global(.fc-scrollgrid-section) {
		min-width: 0;
	}

	:global(.fc-scrollgrid-section table) {
		width: 100% !important;
	}

	:global(.fc-scrollgrid-section-header) {
		background: white;
		width: 100% !important;
	}

	:global(.fc-scrollgrid-section-body) {
		background: white;
		width: 100% !important;
	}

	:global(.fc-daygrid-body) {
		width: 100% !important;
	}

	:global(.fc-daygrid-body table) {
		width: 100% !important;
	}

	:global(.fc-col-header) {
		width: 100% !important;
	}

	:global(.fc-view table) {
		width: 100% !important;
	}

	@media (max-width: 1024px) {
		.side-panel {
			transform: translateX(-100%);
			transition: transform 0.3s ease;
			z-index: 30;
		}

		.side-panel.open {
			transform: translateX(0);
		}

		.main-section {
			margin-left: 0;
			width: 100%;
		}

		.header-content {
			padding: 0 1rem;
		}
	}
</style>
