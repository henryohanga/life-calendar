<script lang="ts">
	import { fade, fly } from 'svelte/transition';
	import CalendarGrid from '$lib/components/CalendarGrid.svelte';
	import type { GoodDatesResponse } from '$lib/types';

	let birthDate = '';
	let goodDates: GoodDatesResponse | null = null;
	let loading = false;
	let error: string | null = null;

	async function handleSubmit() {
		if (!birthDate) return;

		loading = true;
		error = null;

		try {
			const response = await fetch('/api/good-dates', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					birth_date: birthDate,
					match_on_single_digit: true,
					year: new Date().getFullYear()
				})
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.detail || 'Failed to fetch good dates');
			}

			goodDates = await response.json();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Something went wrong. Please try again.';
		} finally {
			loading = false;
		}
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
	<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
		<div class="text-center mb-12" in:fly={{ y: 20, duration: 300, delay: 150 }}>
			<h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
				<span class="inline-block">✨</span>
				Good Dates Calendar
			</h1>
			<p class="text-base sm:text-lg text-gray-600 max-w-2xl mx-auto">
				Find the most auspicious dates based on your numerology number and plan your important
				events accordingly
			</p>
		</div>

		{#if !goodDates}
			<div
				class="bg-white rounded-2xl shadow-xl p-6 sm:p-8 max-w-lg mx-auto border border-gray-100"
				in:fly={{ y: 20, duration: 300 }}
			>
				<form on:submit|preventDefault={handleSubmit} class="space-y-6">
					<div>
						<label for="birthDate" class="block text-sm font-medium text-gray-700 mb-2">
							Your Birth Date
						</label>
						<div class="relative">
							<input
								type="date"
								id="birthDate"
								bind:value={birthDate}
								class="block w-full px-4 py-3 rounded-lg border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors shadow-sm"
								required
							/>
							<div
								class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-gray-400"
							>
								<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
									/>
								</svg>
							</div>
						</div>
					</div>

					{#if error}
						<div
							class="p-4 rounded-lg bg-red-50 border border-red-200 text-red-600 flex items-center space-x-2"
							role="alert"
							in:fade
						>
							<svg
								class="w-5 h-5"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
								/>
							</svg>
							{error}
						</div>
					{/if}

					<button
						type="submit"
						class="w-full bg-gradient-to-r from-indigo-500 to-indigo-600 text-white rounded-lg px-6 py-3.5 text-base font-medium hover:from-indigo-600 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 shadow-sm"
						disabled={loading}
					>
						{#if loading}
							<svg
								class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
								xmlns="http://www.w3.org/2000/svg"
								fill="none"
								viewBox="0 0 24 24"
							>
								<circle
									class="opacity-25"
									cx="12"
									cy="12"
									r="10"
									stroke="currentColor"
									stroke-width="4"
								/>
								<path
									class="opacity-75"
									fill="currentColor"
									d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
								/>
							</svg>
							<span>Finding Good Dates...</span>
						{:else}
							<span class="text-lg mr-2">✨</span>
							<span>Find Good Dates</span>
						{/if}
					</button>

					<p class="text-sm text-gray-500 text-center mt-4">
						Enter your birth date to discover dates that align with your numerology number
					</p>
				</form>
			</div>
		{:else}
			<div in:fly={{ y: 20, duration: 300 }}>
				<CalendarGrid {goodDates} />
			</div>
		{/if}
	</div>
</div>
