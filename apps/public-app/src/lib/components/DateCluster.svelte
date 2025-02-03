<script lang="ts">
	import { formatDate } from '$lib/utils/dates';

	export let cluster: {
		start_date: string;
		end_date: string;
		dates: string[];
		duration: number;
	};
</script>

<div class="cluster">
	<div class="cluster-header">
		<span class="dates">
			{formatDate(cluster.start_date)} - {formatDate(cluster.end_date)}
		</span>
		<span class="duration">{cluster.duration} days</span>
	</div>
	<div class="cluster-dates">
		{#each cluster.dates as date}
			<span class="date-chip">{formatDate(date, { day: 'numeric' })}</span>
		{/each}
	</div>
</div>

<style>
	.cluster {
		background: var(--color-surface-variant);
		border-radius: 8px;
		padding: 1rem;
		margin-bottom: 1rem;
	}

	.cluster-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.5rem;
	}

	.dates {
		font-weight: bold;
	}

	.duration {
		color: var(--color-secondary);
	}

	.cluster-dates {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.date-chip {
		background: var(--color-surface);
		padding: 0.25rem 0.75rem;
		border-radius: 16px;
		font-size: 0.9rem;
	}
</style>
