<script lang="ts">
	import { fade } from 'svelte/transition';
	import { createEventDispatcher } from 'svelte';

	export let isOpen = false;
	export let title = '';

	const dispatch = createEventDispatcher();

	function handleClose() {
		dispatch('close');
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' && isOpen) {
			handleClose();
		}
	}

	function handleBackdropClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			handleClose();
		}
	}
</script>

{#if isOpen}
	<div
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
		class="modal-backdrop"
		in:fade={{ duration: 200 }}
		out:fade={{ duration: 200 }}
		on:click={handleBackdropClick}
		on:keydown={handleKeydown}
		tabindex="-1"
	>
		<div class="modal-content" on:click|stopPropagation>
			<div class="modal-header">
				<h2 id="modal-title">{title}</h2>
				<button class="close-button" on:click={handleClose} aria-label="Close modal"> × </button>
			</div>
			<div class="modal-body">
				<slot />
			</div>
			<div class="modal-footer">
				<slot name="footer">
					<button on:click={handleClose} class="close-modal-button"> Close </button>
				</slot>
			</div>
		</div>
	</div>
{/if}

<style>
	.modal-backdrop {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		backdrop-filter: blur(2px);
	}

	.modal-content {
		background: white;
		border-radius: 8px;
		padding: 1.5rem;
		max-width: 500px;
		width: 90%;
		position: relative;
		max-height: 90vh;
		overflow-y: auto;
		box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
	}

	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid var(--color-outline, #e2e8f0);
	}

	.modal-header h2 {
		margin: 0;
		font-size: 1.25rem;
		font-weight: 600;
	}

	.modal-body {
		margin: 1rem 0;
	}

	.modal-footer {
		display: flex;
		justify-content: flex-end;
		gap: 0.5rem;
		margin-top: 1rem;
		padding-top: 1rem;
		border-top: 1px solid var(--color-outline, #e2e8f0);
	}

	.close-button {
		background: none;
		border: none;
		font-size: 1.5rem;
		cursor: pointer;
		padding: 0.5rem;
		border-radius: 4px;
		transition: background-color 0.2s;
	}

	.close-button:hover {
		background-color: var(--color-surface-variant, #f8fafc);
	}

	.close-button:focus {
		outline: 2px solid var(--color-primary, #4f46e5);
		outline-offset: 2px;
	}

	.close-modal-button {
		padding: 0.5rem 1rem;
		background: var(--color-surface-variant, #f8fafc);
		color: var(--color-on-surface, #1f2937);
		border: 1px solid var(--color-outline, #e2e8f0);
		border-radius: 6px;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s;
	}

	.close-modal-button:hover {
		background: var(--color-surface, white);
		border-color: var(--color-primary, #4f46e5);
		color: var(--color-primary, #4f46e5);
	}
</style>
