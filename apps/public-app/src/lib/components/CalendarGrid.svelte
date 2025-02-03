<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import Calendar from '@event-calendar/core';
	import dayGridPlugin from '@event-calendar/day-grid';
	import type { GoodDateResponse } from '$lib/types';
	import Tooltip from './Tooltip.svelte';
	import Modal from './Modal.svelte';

	export let goodDates: GoodDateResponse;
	let calendarEl: HTMLElement;
	let selectedDate: string | null = null;
	let calendar: Calendar;
	let showModal = false;

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
					options: {
						view: 'dayGridMonth',
						height: 'auto',
						events: goodDates.dates.map((date) => ({
							start: date,
							end: date,
							display: 'background',
							backgroundColor: 'rgb(99 102 241 / 0.15)', // Increased opacity
							classNames: ['good-date-bg']
						})),
						headerToolbar: {
							start: 'prev',
							center: 'title',
							end: 'next today'
						},
						dateClick: (info: { dateStr: string }) => {
							selectedDate = info.dateStr;
							showModal = true;
						},
						dayCellDidMount: (info: any) => {
							const dateStr = info.date.toISOString().split('T')[0];
							if (isGoodDate(dateStr)) {
								// Create indicator container
								const indicatorEl = document.createElement('div');
								indicatorEl.className = 'absolute inset-0 flex items-start justify-end p-2';

								// Create indicator content
								const indicator = document.createElement('div');
								indicator.className = 'good-date-indicator';
								indicator.innerHTML = '✨';
								indicatorEl.appendChild(indicator);

								info.el.appendChild(indicatorEl);

								new Tooltip({
									target: indicator,
									props: {
										text: `This date resonates with your numerology number ${goodDates.numerology_number}`,
										position: 'top'
									}
								});
							}
						}
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
					Found {goodDates.dates.length} matching dates in {new Date().getFullYear()}
				</span>
			</div>
		</div>
	</div>

	<div class="calendar-wrapper">
		<div class="calendar-inner">
			<div bind:this={calendarEl} />
		</div>
	</div>
</div>

<Modal bind:show={showModal} title="Date Details">
	{#if selectedDate}
		<p class="text-gray-600 text-lg">
			{#if isGoodDate(selectedDate)}
				<span class="text-xl mr-2">✨</span>
				<span class="font-medium text-indigo-600">{selectedDate}</span>
				<span class="ml-1.5">
					is a good date that resonates with your numerology number {goodDates.numerology_number}!
				</span>
			{:else}
				<span class="font-medium text-gray-900">{selectedDate}</span>
				<span class="ml-1.5">is not aligned with your numerology number.</span>
			{/if}
		</p>
	{/if}

	<div slot="footer">
		<button
			on:click={() => (showModal = false)}
			class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
		>
			Close
		</button>
		{#if selectedDate && isGoodDate(selectedDate)}
			<button
				class="px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors ml-2"
			>
				Add to Calendar
			</button>
		{/if}
	</div>
</Modal>
