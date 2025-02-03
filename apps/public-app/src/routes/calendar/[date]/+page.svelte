<script lang="ts">
	import GoodDatesResults from '$lib/components/GoodDatesResults.svelte';
	import type { GoodDateResponse } from '$lib/types';
	import { fade, fly } from 'svelte/transition';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	let results: GoodDateResponse | null = null;
	let loading = true;
	let error: string | null = null;

	onMount(async () => {
		try {
			const dateOfBirth = $page.params.date;
			const response = await fetch(`/api/dates/${dateOfBirth}`);

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error || 'Failed to fetch results');
			}

			results = await response.json();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Something went wrong';
		} finally {
			loading = false;
		}
	});
</script>

{#if loading}
	<div class="loading" in:fade>
		<div class="loading-spinner" />
		<p>Loading your personalized calendar...</p>
	</div>
{:else if error}
	<div class="error" in:fly={{ y: 20, duration: 300 }}>
		<p>{error}</p>
		<button on:click={() => (window.location.href = '/')} class="back-button">
			Go Back
		</button>
	</div>
{:else if results}
	<GoodDatesResults {results} />
{/if}

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		height: 100vh;
		overflow: hidden;
	}

	.loading,
	.error {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100vh;
		font-size: 1.2rem;
		color: var(--text-primary);
		gap: 1rem;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 3px solid #f3f3f3;
		border-top: 3px solid var(--primary-color, #1a73e8);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	.error {
		color: #ef4444;
	}

	.back-button {
		margin-top: 1rem;
		padding: 0.5rem 1rem;
		background: var(--primary-color, #1a73e8);
		color: white;
		border: none;
		border-radius: 0.375rem;
		cursor: pointer;
		font-size: 1rem;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>
