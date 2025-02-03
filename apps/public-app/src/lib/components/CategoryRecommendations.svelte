<script lang="ts">
	import type { ZodiacRecommendations } from '$lib/types';
	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	export let recommendations: ZodiacRecommendations;

	type CategoryStyle = {
		bg: string;
		text: string;
	};

	type CategoryStyles = Record<string, CategoryStyle>;
	type CategoryIcon = Record<string, string>;

	const categoryIcons = {
		career: '💼',
		personal: '🌟',
		rest: '🌿',
		financial: '💰'
	} as const;

	const categoryColors = {
		career: {
			bg: 'rgba(79, 70, 229, 0.1)',
			text: '#4f46e5'
		},
		personal: {
			bg: 'rgba(8, 145, 178, 0.1)',
			text: '#0891b2'
		},
		rest: {
			bg: 'rgba(5, 150, 105, 0.1)',
			text: '#059669'
		},
		financial: {
			bg: 'rgba(124, 58, 237, 0.1)',
			text: '#7c3aed'
		}
	} satisfies CategoryStyles;

	function getCategoryStyle(category: string): CategoryStyle {
		return categoryColors[category as keyof typeof categoryColors] || categoryColors.career;
	}

	function getCategoryIcon(category: string): string {
		return categoryIcons[category as keyof typeof categoryIcons] || '✨';
	}
</script>

<div class="recommendations" in:slide={{ duration: 300, delay: 100, easing: quintOut }}>
	<h3 class="title">Astrological Recommendations</h3>
	<div class="categories-grid">
		{#each Object.entries(recommendations) as [category, items], i}
			{#if category !== 'power_periods' && category !== 'date_specific_advice'}
				{@const style = getCategoryStyle(category)}
				<div
					class="category-card"
					style:background-color={style.bg}
					style:color={style.text}
					in:slide={{ duration: 300, delay: 150 + i * 50, easing: quintOut }}
				>
					<div class="category-header">
						<span class="category-icon">
							{getCategoryIcon(category)}
						</span>
						<h4 class="category-title">{category}</h4>
					</div>
					<div class="recommendations-list">
						{#each items as item}
							<div class="recommendation-item">
								<span class="bullet">•</span>
								<p>{item}</p>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		{/each}
	</div>
</div>

<style>
	.recommendations {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.title {
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--color-on-surface, #1f2937);
		margin: 0;
	}

	.categories-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 1rem;
	}

	.category-card {
		padding: 1.25rem;
		border-radius: 12px;
		transition: all 0.2s ease;
	}

	.category-card:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
	}

	.category-header {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 1rem;
	}

	.category-icon {
		font-size: 1.5rem;
	}

	.category-title {
		margin: 0;
		font-size: 1.125rem;
		font-weight: 600;
		text-transform: capitalize;
	}

	.recommendations-list {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.recommendation-item {
		display: flex;
		gap: 0.5rem;
		align-items: flex-start;
		line-height: 1.4;
	}

	.bullet {
		opacity: 0.7;
	}

	.recommendation-item p {
		margin: 0;
		font-size: 0.875rem;
		opacity: 0.9;
	}

	@media (max-width: 640px) {
		.categories-grid {
			grid-template-columns: 1fr;
		}

		.category-card {
			padding: 1rem;
		}

		.category-icon {
			font-size: 1.25rem;
		}

		.category-title {
			font-size: 1rem;
		}
	}
</style>
