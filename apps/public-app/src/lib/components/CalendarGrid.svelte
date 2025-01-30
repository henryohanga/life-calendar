<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import Calendar from '@event-calendar/core';
	import dayGridPlugin from '@event-calendar/day-grid';
	import type { GoodDatesResponse } from '$lib/types';

	export let goodDates: GoodDatesResponse;
	let calendarEl: HTMLElement;
	let selectedDate: string | null = null;
	let calendar: Calendar;

	$: isGoodDate = (date: string) => goodDates.dates.includes(date);

	function initializeCalendar() {
		if (calendarEl) {
			if (calendar) {
				calendar.$destroy();
			}

			calendar = new Calendar({
				target: calendarEl,
				props: {
					plugins: [dayGridPlugin],
					view: 'dayGridMonth',
					height: 'auto',
					events: goodDates.dates.map((date) => ({
						start: date,
						display: 'background',
						classNames: ['good-date-bg']
					})),
					headerToolbar: {
						start: 'prev',
						center: 'title',
						end: 'next'
					},
					dateClick: (info: { dateStr: string }) => {
						selectedDate = info.dateStr;
					}
				}
			});
		}
	}

	onMount(() => {
		initializeCalendar();
		return () => {
			if (calendar) {
				calendar.$destroy();
			}
		};
	});

	$: {
		if (goodDates && calendar) {
			initializeCalendar();
		}
	}
</script>

<div class="bg-white rounded-2xl shadow-xl p-6 sm:p-8 space-y-8 border border-gray-100">
	<div
		class="flex flex-col sm:flex-row items-start gap-6 p-6 bg-gradient-to-br from-indigo-50 via-white to-indigo-50/30 rounded-xl border border-indigo-100"
		in:fade={{ duration: 300 }}
	>
		<div class="flex-shrink-0">
			<div
				class="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-100/50"
			>
				<span class="text-3xl font-bold text-white">{goodDates.numerology_number}</span>
			</div>
		</div>
		<div class="flex-1">
			<h2 class="text-2xl font-semibold text-gray-900 mb-2">Your Numerology Number</h2>
			<p class="text-gray-600 mb-4 leading-relaxed text-base">{goodDates.number_meaning}</p>
			<div class="flex items-center text-sm font-medium">
				<span
					class="flex items-center text-indigo-600 bg-indigo-50 px-4 py-2 rounded-full border border-indigo-100"
				>
					<span class="text-lg mr-2">✨</span>
					Found {goodDates.total_matches} matching dates in {new Date().getFullYear()}
				</span>
			</div>
		</div>
	</div>

	{#if selectedDate}
		<div
			class="p-5 rounded-xl border border-indigo-100 bg-gradient-to-r from-indigo-50 via-white to-indigo-50"
			in:fade={{ duration: 200 }}
			role="status"
		>
			<p class="text-gray-600 flex items-center text-lg">
				{#if isGoodDate(selectedDate)}
					<span class="text-xl mr-2">✨</span>
					<span class="font-medium text-indigo-600">{selectedDate}</span>
					<span class="ml-1.5">is a good date for you!</span>
				{:else}
					<span class="font-medium text-gray-900">{selectedDate}</span>
					<span class="ml-1.5">is not aligned with your numerology number.</span>
				{/if}
			</p>
		</div>
	{/if}

	<div class="calendar-wrapper">
		<div class="calendar-inner">
			<div bind:this={calendarEl} />
		</div>
	</div>
</div>
