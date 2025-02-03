<script lang="ts">
	import type { CalendarProps } from '$lib/types/calendar';
	import type { EventInput } from '@fullcalendar/core';
	import { Calendar } from '@fullcalendar/core';
	import dayGridPlugin from '@fullcalendar/daygrid';
	import timeGridPlugin from '@fullcalendar/timegrid';
	import listPlugin from '@fullcalendar/list';
	import { onMount, createEventDispatcher } from 'svelte';
	import { categoryColors, timeMap } from '$lib/constants/calendar';

	export let results: CalendarProps['results'];
	const dispatch = createEventDispatcher<{
		dateSelect: string;
	}>();

	// Add type for zodiac sign
	type ZodiacSign = {
		name: string;
		symbol: string;
		element: string;
		date_range: string;
		date_advice: Array<{
			date: string;
			category: 'career' | 'personal' | 'rest' | 'financial';
			timing: 'morning' | 'afternoon' | 'evening' | 'night';
			power_level: number;
			activities: string[];
		}>;
		power_periods: Array<{
			start_date: string;
			end_date: string;
			dates: string[];
			duration: number;
		}>;
	};

	// Helper functions
	function formatDate(date: string) {
		return new Date(date).toLocaleDateString('en-US', {
			weekday: 'long',
			month: 'long',
			day: 'numeric'
		});
	}

	function createTooltipContent(event: EventInput): string {
		const { extendedProps } = event;

		if (extendedProps?.isGoodDate) {
			return `
				<div class="tooltip-header">
					<strong>${formatDate(event.start?.toISOString() || '')}</strong>
				</div>
				<div class="tooltip-content">
					<p>✨ Auspicious date for Life Path ${extendedProps.numerologyNumber}</p>
					${extendedProps.category ? `<p>📌 Category: ${extendedProps.category}</p>` : ''}
					${
						extendedProps.powerLevel > 1
							? `<p>⭐ Power Level: ${'⭐'.repeat(extendedProps.powerLevel - 1)}</p>`
							: ''
					}
					${createActivitiesList(extendedProps.activities)}
				</div>
			`;
		}

		// ... rest of tooltip content logic
	}

	function createActivitiesList(activities?: string[]): string {
		if (!activities?.length) return '';

		return `
			<div class="tooltip-activities">
				<p>Recommended activities:</p>
				<ul>
					${activities.map((activity) => `<li>• ${activity}</li>`).join('')}
				</ul>
			</div>
		`;
	}

	function createCalendarEvents(): EventInput[] {
		// Add debug logging for event creation
		console.log('Creating calendar events with:', {
			dates: results.dates,
			advice: results.zodiac_sign?.recommendations?.date_specific_advice,
			powerPeriods: results.zodiac_sign?.recommendations?.power_periods
		});

		const events: EventInput[] = [];
		console.log('Creating events with dates:', results.dates);
		console.log(
			'Date specific advice:',
			results.zodiac_sign?.recommendations?.date_specific_advice
		);

		// Add all good dates as background events with more info
		results.dates.forEach((date) => {
			const dateInfo = results.zodiac_sign?.recommendations?.date_specific_advice?.[date];
			if (!dateInfo) {
				console.log(`No date info found for ${date}`);
				return;
			}

			// Add debug logging for each date
			console.log(`Processing date ${date}:`, dateInfo);

			// Background event for good date
			events.push({
				id: `base-${date}`,
				start: date,
				allDay: true,
				display: 'background',
				backgroundColor: categoryColors[dateInfo.category].bg,
				extendedProps: {
					isGoodDate: true,
					numerologyNumber: results.numerology_number,
					category: dateInfo.category,
					powerLevel: dateInfo.power_level,
					activities: dateInfo.activities,
					meaning: results.number_meaning
				}
			});

			// Add category event for the day
			events.push({
				id: `day-${date}`,
				title: `${categoryColors[dateInfo.category].icon} ${dateInfo.category.toUpperCase()}`,
				start: date,
				allDay: true,
				backgroundColor: categoryColors[dateInfo.category].bg,
				borderColor: categoryColors[dateInfo.category].base,
				textColor: categoryColors[dateInfo.category].base,
				classNames: ['category-day', `category-${dateInfo.category}`],
				extendedProps: {
					category: dateInfo.category,
					powerLevel: dateInfo.power_level,
					timing: dateInfo.timing,
					zodiacSign: results.zodiac_sign?.name,
					activities: dateInfo.activities
				}
			});

			// Add the activities as separate events for better visibility
			if (dateInfo.activities && dateInfo.activities.length > 0) {
				console.log(`Adding activities for ${date}:`, dateInfo.activities);
				const timeSlot = timeMap[dateInfo.timing] || timeMap.morning;
				dateInfo.activities.forEach((activity, index) => {
					const eventStart = new Date(`${date}T${timeSlot.start}`);
					eventStart.setMinutes(eventStart.getMinutes() + index * 45);

					const eventEnd = new Date(eventStart);
					eventEnd.setMinutes(eventEnd.getMinutes() + 30);

					events.push({
						id: `activity-${date}-${index}`,
						title: activity,
						start: eventStart.toISOString(),
						end: eventEnd.toISOString(),
						backgroundColor: categoryColors[dateInfo.category].base,
						borderColor: categoryColors[dateInfo.category].base,
						textColor: 'white',
						extendedProps: {
							category: dateInfo.category,
							timing: dateInfo.timing,
							powerLevel: dateInfo.power_level,
							zodiacSign: results.zodiac_sign?.name
						}
					});
				});
			}
		});

		// Add power periods as background events
		results.zodiac_sign?.recommendations?.power_periods?.forEach((period) => {
			events.push({
				start: period.start_date,
				end: period.end_date,
				display: 'background',
				backgroundColor: 'rgba(79, 70, 229, 0.1)',
				classNames: ['power-period'],
				extendedProps: {
					isPowerPeriod: true,
					duration: period.duration,
					dates: period.dates
				}
			});
		});

		console.log('Generated events:', events);
		return events;
	}

	function handleDateClick(date: string) {
		dispatch('dateSelect', date);
	}

	onMount(() => {
		const calendarEl = document.getElementById('calendar');
		if (!calendarEl) return;

		const calendar = new Calendar(calendarEl, {
			plugins: [dayGridPlugin, timeGridPlugin, listPlugin],
			initialView: 'dayGridMonth',
			events: createCalendarEvents(),
			height: '100%', // Use container height
			headerToolbar: {
				left: 'prev,next today',
				center: 'title',
				right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
			},
			// Calendar view customization
			views: {
				dayGrid: {
					dayMaxEvents: true, // Show "+more" when too many events
					dayMaxEventRows: true
				},
				timeGrid: {
					slotMinTime: '06:00:00',
					slotMaxTime: '22:00:00',
					slotDuration: '00:30:00',
					nowIndicator: true,
					slotEventOverlap: false
				}
			},
			// General calendar options
			allDaySlot: true,
			allDayText: 'Full Day',
			slotLabelFormat: {
				hour: 'numeric',
				minute: '2-digit',
				meridiem: 'short'
			},
			eventTimeFormat: {
				hour: 'numeric',
				minute: '2-digit',
				meridiem: 'short'
			},
			// Event handling
			eventDidMount: (info) => {
				// Enhanced tooltip content
				const tooltip = document.createElement('div');
				tooltip.className = 'calendar-tooltip';

				if (info.event.extendedProps?.isGoodDate) {
					// Tooltip for good dates
					tooltip.innerHTML = createTooltipContent(info.event);
				} else if (info.event.extendedProps?.isPowerPeriod) {
					// Tooltip for power periods
					tooltip.innerHTML = `
						<div class="tooltip-header">
							<strong>Power Period</strong>
						</div>
						<div class="tooltip-content">
							<p>♈ ${info.event.extendedProps.zodiacSign}</p>
							<div class="tooltip-dates">
								<p>Dates included:</p>
								<ul>
									${info.event.extendedProps.dates
										.map(
											(date: string) => `
										<li>• ${formatDate(date)}</li>
									`
										)
										.join('')}
								</ul>
							</div>
						</div>
					`;
				} else {
					// Tooltip for regular events
					tooltip.innerHTML = `
						<div class="tooltip-header">
							<strong>${info.event.title}</strong>
						</div>
						<div class="tooltip-content">
							${info.event.extendedProps?.category ? `<p>Category: ${info.event.extendedProps.category}</p>` : ''}
							${info.event.extendedProps?.timing ? `<p>Best Time: ${info.event.extendedProps.timing}</p>` : ''}
							${
								info.event.extendedProps?.powerLevel > 1
									? `
								<p>Power Level: ${'⭐'.repeat(info.event.extendedProps.powerLevel - 1)}</p>
							`
									: ''
							}
						</div>
					`;
				}

				const showTooltip = () => {
					const rect = info.el.getBoundingClientRect();
					tooltip.style.display = 'block';

					// Position tooltip
					const tooltipHeight = tooltip.offsetHeight;
					const spaceBelow = window.innerHeight - rect.bottom;
					const spaceAbove = rect.top;

					if (spaceBelow < tooltipHeight && spaceAbove > tooltipHeight) {
						// Show above if not enough space below
						tooltip.style.top = `${rect.top - tooltipHeight - 5}px`;
					} else {
						// Show below by default
						tooltip.style.top = `${rect.bottom + 5}px`;
					}

					// Horizontal positioning
					const tooltipWidth = tooltip.offsetWidth;
					let left = rect.left;
					if (left + tooltipWidth > window.innerWidth) {
						left = window.innerWidth - tooltipWidth - 5;
					}
					tooltip.style.left = `${Math.max(5, left)}px`;

					document.body.appendChild(tooltip);
				};

				info.el.addEventListener('mouseover', showTooltip);
				info.el.addEventListener('mouseout', () => tooltip.remove());
				info.el.addEventListener('mousemove', (e) => {
					// Prevent tooltip flicker on child elements
					e.stopPropagation();
				});
			},
			// Add date click handler
			dateClick: (info) => {
				// Only dispatch if it's a good date
				if (results.dates.includes(info.dateStr)) {
					dispatch('dateSelect', info.dateStr);
				}
			},
			// Add event click handler
			eventClick: (info) => {
				if (info.event.extendedProps?.isGoodDate) {
					dispatch('dateSelect', info.event.startStr);
				}
			}
		});

		calendar.render();

		return () => {
			calendar.destroy();
		};
	});

	$: {
		if (results) {
			console.log('Calendar received results:', {
				dates: results.dates?.length,
				hasZodiacSign: !!results.zodiac_sign,
				hasDateSpecificAdvice: results.zodiac_sign?.recommendations?.date_specific_advice?.length,
				sampleDate: results.dates?.[0],
				sampleAdvice: results.dates?.[0]
					? results.zodiac_sign?.recommendations?.date_specific_advice?.[results.dates[0]]
					: null
			});
		}
	}
</script>

<div class="calendar-wrapper">
	<div class="calendar-header">
		<h2 class="calendar-title">
			{results.zodiac_sign.name} Good Dates
			<span class="subtitle">Life Path {results.numerology_number}</span>
		</h2>
		<div class="calendar-stats">
			<div class="stat-item">
				<span class="stat-label">Total Dates</span>
				<span class="stat-value">{results.dates.length}</span>
			</div>
			<div class="stat-item">
				<span class="stat-label">Power Periods</span>
				<span class="stat-value">{results.zodiac_sign.recommendations.power_periods.length}</span>
			</div>
		</div>
	</div>
	<div class="legend">
		{#each Object.entries(categoryColors) as [category, { base, icon }]}
			<div class="legend-item">
				<span class="legend-color" style="background-color: {base}">
					<span class="legend-icon">{icon}</span>
				</span>
				<span class="capitalize">{category}</span>
			</div>
		{/each}
		<div class="legend-item">
			<span class="legend-color power-period" />
			<span>✨ Power Period</span>
		</div>
	</div>
	<div id="calendar" class="calendar-container" />
</div>

<style>
	.calendar-wrapper {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		padding: 2rem;
		min-height: calc(100vh - 4rem);
		background: var(--color-surface, white);
	}

	.calendar-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding-bottom: 1rem;
		border-bottom: 1px solid var(--color-outline, #e2e8f0);
	}

	.calendar-title {
		font-size: 1.875rem;
		font-weight: 600;
		color: var(--color-on-surface, #1f2937);
		margin: 0;
	}

	.subtitle {
		font-size: 1.125rem;
		color: var(--color-on-surface-variant, #64748b);
		margin-left: 1rem;
	}

	.calendar-stats {
		display: flex;
		gap: 2rem;
	}

	.stat-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.25rem;
	}

	.stat-label {
		font-size: 0.875rem;
		color: var(--color-on-surface-variant, #64748b);
	}

	.stat-value {
		font-size: 1.5rem;
		font-weight: 600;
		color: var(--color-on-surface, #1f2937);
	}

	.legend {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		padding: 1rem;
		background: linear-gradient(to right, rgba(79, 70, 229, 0.05), rgba(124, 58, 237, 0.05));
		border-radius: 8px;
		border: 1px solid rgba(79, 70, 229, 0.1);
	}

	.calendar-container {
		flex: 1;
		min-height: 0;
		background: white;
		border-radius: 8px;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
		padding: 1rem;
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.875rem;
		padding: 0.25rem 0.75rem;
		border-radius: 1rem;
		background: rgba(255, 255, 255, 0.8);
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
		transition: transform 0.2s ease;
	}

	.legend-item:hover {
		transform: translateY(-1px);
	}

	.legend-color {
		width: 24px;
		height: 24px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
	}

	.legend-icon {
		font-size: 0.875rem;
	}

	.legend-color.power-period {
		background-color: rgba(79, 70, 229, 0.15);
		border: 1px solid rgba(79, 70, 229, 0.4);
	}

	.capitalize {
		text-transform: capitalize;
	}

	:global(.fc) {
		--fc-border-color: var(--color-outline, #e2e8f0);
		--fc-button-text-color: #ffffff;
		--fc-button-bg-color: var(--color-primary, #4f46e5);
		--fc-button-border-color: var(--color-primary, #4f46e5);
		--fc-button-hover-bg-color: var(--color-primary-dark, #4338ca);
		--fc-button-hover-border-color: var(--color-primary-dark, #4338ca);
		--fc-button-active-bg-color: var(--color-primary-dark, #4338ca);
		--fc-button-active-border-color: var(--color-primary-dark, #4338ca);
		--fc-event-bg-color: var(--color-primary, #4f46e5);
		--fc-event-border-color: transparent;
		--fc-event-text-color: #ffffff;
		--fc-today-bg-color: var(--color-surface-variant, #f8fafc);
		--fc-now-indicator-color: var(--color-primary, #4f46e5);
		--fc-list-event-hover-bg-color: var(--color-surface-variant, #f8fafc);
		--fc-neutral-bg-color: transparent;
		--fc-page-bg-color: transparent;
		height: 100% !important;
	}

	/* Button styles */
	:global(.fc .fc-button-primary) {
		background-color: var(--fc-button-bg-color) !important;
		border-color: var(--fc-button-border-color) !important;
		color: var(--fc-button-text-color) !important;
		padding: 0.5rem 1rem;
		font-weight: 500;
		border-radius: 0.375rem;
		transition: all 0.2s;
		opacity: 1 !important;
	}

	:global(.fc .fc-button-primary:hover) {
		background-color: var(--fc-button-hover-bg-color) !important;
		border-color: var(--fc-button-hover-border-color) !important;
		color: var(--fc-button-text-color) !important;
	}

	:global(.fc .fc-button-primary:disabled) {
		opacity: 0.65 !important;
	}

	:global(.fc .fc-button-primary:not(:disabled):active),
	:global(.fc .fc-button-primary:not(:disabled).fc-button-active) {
		background-color: var(--fc-button-active-bg-color) !important;
		border-color: var(--fc-button-active-border-color) !important;
		color: var(--fc-button-text-color) !important;
	}

	:global(.fc .fc-button-group) {
		gap: 0.25rem;
	}

	:global(.fc .fc-button-group .fc-button-primary) {
		border-radius: 0.375rem !important;
	}

	:global(.fc .fc-toolbar) {
		flex-wrap: wrap;
		gap: 1rem;
		padding: 0.5rem;
		background: var(--color-surface-variant, #f8fafc);
		border-radius: 0.5rem;
		margin-bottom: 1rem !important;
	}

	:global(.fc .fc-toolbar-chunk) {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	:global(.fc .fc-toolbar-title) {
		font-size: 1.25rem;
		font-weight: 600;
		color: var(--color-on-surface, #1f2937);
		padding: 0.5rem;
	}

	:global(.fc-theme-standard td, .fc-theme-standard th) {
		border-color: var(--color-outline, #e2e8f0);
	}

	:global(.fc-day-today) {
		background: var(--color-surface-variant, #f8fafc) !important;
	}

	:global(.fc-event) {
		border-radius: 4px;
		margin: 1px 0;
		padding: 2px 4px;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	:global(.fc-event:hover) {
		filter: brightness(1.1);
	}

	:global(.fc-event-title) {
		font-weight: 500;
		font-size: 0.875rem;
		padding: 2px 4px;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	:global(.fc-event-time) {
		font-size: 0.75rem;
		opacity: 0.9;
		padding: 0 4px;
	}

	:global(.fc-timegrid-slot-label) {
		font-size: 0.875rem;
		color: var(--color-on-surface, #1f2937);
	}

	:global(.fc-list-event td) {
		padding: 8px !important;
	}

	:global(.fc-list-day-cushion) {
		background: var(--color-surface-variant, #f8fafc) !important;
	}

	:global(.calendar-tooltip) {
		position: fixed;
		z-index: 1000;
		background: white;
		padding: 0;
		border-radius: 8px;
		box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
		font-size: 0.875rem;
		pointer-events: none;
		max-width: 300px;
		line-height: 1.4;
		border: 1px solid var(--color-outline, #e2e8f0);
	}

	:global(.calendar-tooltip .tooltip-header) {
		background: var(--color-surface-variant, #f8fafc);
		padding: 0.75rem;
		border-radius: 8px 8px 0 0;
		border-bottom: 1px solid var(--color-outline, #e2e8f0);
	}

	:global(.calendar-tooltip .tooltip-content) {
		padding: 0.75rem;
	}

	:global(.calendar-tooltip .tooltip-activities) {
		margin-top: 0.5rem;
	}

	:global(.calendar-tooltip ul) {
		margin: 0.25rem 0 0 0;
		padding: 0;
		list-style: none;
	}

	:global(.calendar-tooltip li) {
		margin: 0.25rem 0;
		padding-left: 1rem;
		position: relative;
	}

	:global(.good-date) {
		cursor: pointer !important;
	}

	:global(.fc-day-today.good-date) {
		background: linear-gradient(
			to right,
			rgba(79, 70, 229, 0.15),
			var(--fc-today-bg-color)
		) !important;
	}

	:global(.power-period) {
		opacity: 1 !important;
		background: linear-gradient(
			45deg,
			rgba(79, 70, 229, 0.15) 25%,
			rgba(79, 70, 229, 0.25) 50%,
			rgba(79, 70, 229, 0.15) 75%
		) !important;
		background-size: 200% 200% !important;
		animation: shimmer 3s ease-in-out infinite !important;
	}

	@keyframes shimmer {
		0% {
			background-position: 0% 0%;
		}
		50% {
			background-position: 200% 200%;
		}
		100% {
			background-position: 0% 0%;
		}
	}

	:global(.activity-event) {
		border-left: 3px solid currentColor !important;
	}

	:global(.category-day) {
		border-radius: 4px !important;
		border: 1px solid currentColor !important;
		transition:
			transform 0.2s ease,
			box-shadow 0.2s ease;
	}

	:global(.category-day:hover) {
		transform: translateY(-1px);
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	:global(.category-career) {
		border-left: 3px solid #4f46e5 !important;
	}

	:global(.category-personal) {
		border-left: 3px solid #0891b2 !important;
	}

	:global(.category-rest) {
		border-left: 3px solid #059669 !important;
	}

	:global(.category-financial) {
		border-left: 3px solid #7c3aed !important;
	}

	@media (max-width: 768px) {
		.calendar-wrapper {
			padding: 1rem;
			min-height: calc(100vh - 2rem);
		}

		.calendar-header {
			flex-direction: column;
			gap: 1rem;
			text-align: center;
		}

		.calendar-title {
			font-size: 1.5rem;
		}

		.subtitle {
			display: block;
			margin: 0.5rem 0 0 0;
			font-size: 1rem;
		}

		.calendar-stats {
			width: 100%;
			justify-content: center;
		}

		:global(.fc .fc-toolbar) {
			flex-direction: column;
			gap: 1rem;
		}

		:global(.fc .fc-toolbar-chunk) {
			width: 100%;
			justify-content: center;
		}

		:global(.fc .fc-toolbar-title) {
			text-align: center;
		}

		:global(.fc .fc-button-group) {
			flex-wrap: wrap;
			justify-content: center;
		}

		:global(.fc-header-toolbar) {
			margin-bottom: 1.5rem !important;
		}

		.calendar-container {
			padding: 0.5rem;
		}
	}
</style>
