<script lang="ts">
	import type { ZodiacSign } from '$lib/types';
	import { fade, slide } from 'svelte/transition';

	export let zodiacSign: ZodiacSign;

	const elementColors = {
		Fire: { bg: 'rgba(239, 68, 68, 0.1)', text: '#ef4444', icon: '🔥' },
		Earth: { bg: 'rgba(16, 185, 129, 0.1)', text: '#10b981', icon: '🌍' },
		Air: { bg: 'rgba(59, 130, 246, 0.1)', text: '#3b82f6', icon: '💨' },
		Water: { bg: 'rgba(14, 165, 233, 0.1)', text: '#0ea5e9', icon: '💧' }
	};

	$: elementStyle =
		elementColors[zodiacSign.element as keyof typeof elementColors] || elementColors.Fire;
</script>

<div class="zodiac-info" in:fade={{ duration: 300 }}>
	<div class="zodiac-header">
		<div class="symbol-container">
			<span class="symbol">{zodiacSign.symbol}</span>
		</div>
		<div class="title-container">
			<h2>{zodiacSign.name}</h2>
			<div
				class="element-badge"
				style:background-color={elementStyle.bg}
				style:color={elementStyle.text}
			>
				<span class="element-icon">{elementStyle.icon}</span>
				{zodiacSign.element} Element
			</div>
		</div>
	</div>

	<div class="date-range" in:slide={{ duration: 300, delay: 200 }}>
		<div class="date-range-content">
			<span class="label">Birth Date Range</span>
			<span class="value">{zodiacSign.date_range}</span>
		</div>
	</div>

	<div class="traits-section" in:slide={{ duration: 300, delay: 300 }}>
		<h3>Key Traits</h3>
		<div class="traits-grid">
			{#each ['Ambitious', 'Practical', 'Patient', 'Determined'] as trait}
				<div class="trait-item">
					<span class="trait-icon">✨</span>
					{trait}
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.zodiac-info {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.zodiac-header {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.symbol-container {
		width: 64px;
		height: 64px;
		display: flex;
		align-items: center;
		justify-content: center;
		background: linear-gradient(
			135deg,
			var(--color-primary, #4f46e5),
			var(--color-primary-dark, #4338ca)
		);
		border-radius: 16px;
		box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2);
	}

	.symbol {
		font-size: 2rem;
		color: white;
	}

	.title-container {
		flex: 1;
	}

	.title-container h2 {
		margin: 0;
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--color-on-surface, #1f2937);
	}

	.element-badge {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.25rem 0.75rem;
		border-radius: 1rem;
		font-size: 0.875rem;
		font-weight: 500;
		margin-top: 0.5rem;
	}

	.element-icon {
		font-size: 1rem;
	}

	.date-range {
		padding: 1rem;
		background: var(--color-surface-variant, #f8fafc);
		border-radius: 12px;
	}

	.date-range-content {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.traits-section {
		margin-top: 0.5rem;
	}

	.traits-section h3 {
		font-size: 1rem;
		font-weight: 600;
		color: var(--color-on-surface, #1f2937);
		margin: 0 0 1rem 0;
	}

	.traits-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
		gap: 1rem;
	}

	.trait-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem;
		background: var(--color-surface-variant, #f8fafc);
		border-radius: 8px;
		font-size: 0.875rem;
		color: var(--color-on-surface, #1f2937);
		transition: all 0.2s ease;
	}

	.trait-item:hover {
		transform: translateY(-1px);
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
	}

	.label {
		font-size: 0.875rem;
		color: var(--color-on-surface-variant, #64748b);
	}

	.value {
		font-size: 0.875rem;
		font-weight: 600;
		color: var(--color-on-surface, #1f2937);
	}

	@media (max-width: 640px) {
		.symbol-container {
			width: 48px;
			height: 48px;
		}

		.symbol {
			font-size: 1.5rem;
		}

		.title-container h2 {
			font-size: 1.25rem;
		}
	}
</style>
