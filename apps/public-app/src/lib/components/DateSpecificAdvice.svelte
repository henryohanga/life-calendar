<script lang="ts">
	type Activity = {
		activities: string[];
		timing: string;
		power_level: number;
		category: string;
	};

	export let dateAdvice: Activity;
</script>

<div class="date-advice">
	<div class="advice-header">
		<div class="timing">
			<span class="label">Best timing:</span>
			<span class="value">{dateAdvice.timing}</span>
		</div>
		<div class="power-level">
			<span class="label">Power level:</span>
			<span class="value">{'★'.repeat(dateAdvice.power_level)}</span>
		</div>
		<div class="category">
			<span class="label">Category:</span>
			<span class="value capitalize">{dateAdvice.category}</span>
		</div>
	</div>

	<div class="activities">
		<h4>Recommended activities:</h4>
		<ul>
			{#each dateAdvice.activities as activity}
				<li>{activity}</li>
			{/each}
		</ul>
	</div>
</div>

<style>
	.date-advice {
		background-color: var(--surface-2);
		padding: 1rem;
		border-radius: 0.5rem;
		margin: 1rem 0;
	}

	.advice-header {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.label {
		font-weight: 600;
		margin-right: 0.5rem;
	}

	.value {
		color: var(--brand);
	}

	.capitalize {
		text-transform: capitalize;
	}

	.activities h4 {
		margin: 0 0 0.5rem 0;
	}

	.activities ul {
		list-style-type: none;
		padding-left: 0;
		margin: 0;
	}

	.activities li {
		padding: 0.25rem 0;
		position: relative;
		padding-left: 1.5rem;
	}

	.activities li::before {
		content: '•';
		position: absolute;
		left: 0.5rem;
		color: var(--brand);
	}
</style>
