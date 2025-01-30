<script lang="ts">
	export let text: string;
	export let position: 'top' | 'bottom' | 'left' | 'right' = 'top';

	const positionClasses = {
		top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
		bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
		left: 'right-full top-1/2 -translate-y-1/2 mr-2',
		right: 'left-full top-1/2 -translate-y-1/2 ml-2'
	};
</script>

<div class="relative group">
	<slot />
	<div
		class="absolute hidden group-hover:block bg-gray-800 text-white text-sm rounded px-2 py-1 min-w-max z-10 {positionClasses[
			position
		]}"
	>
		{text}
		<div
			class="absolute w-2 h-2 bg-gray-800 transform rotate-45 {position === 'top'
				? 'top-full -translate-y-1 left-1/2 -translate-x-1/2'
				: position === 'bottom'
					? 'bottom-full translate-y-1 left-1/2 -translate-x-1/2'
					: position === 'left'
						? 'left-full -translate-x-1 top-1/2 -translate-y-1/2'
						: 'right-full translate-x-1 top-1/2 -translate-y-1/2'}"
		/>
	</div>
</div>
