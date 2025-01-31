<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	export let show = false;
	export let title: string;

	let dialog: HTMLDialogElement;

	onMount(() => {
		if (show) {
			dialog.showModal();
		}
	});

	$: if (dialog && show) {
		dialog.showModal();
	} else if (dialog && !show) {
		dialog.close();
	}

	function closeModal() {
		show = false;
	}

	function handleClose(event: Event) {
		if (event.target === dialog) {
			closeModal();
		}
	}
</script>

{#if show}
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<dialog
		bind:this={dialog}
		class="backdrop:bg-gray-800/50 rounded-lg shadow-xl p-0 w-full max-w-lg"
		on:click={handleClose}
	>
		<div
			transition:fade={{ duration: 200 }}
			class="relative bg-white rounded-lg shadow-xl"
			role="dialog"
			aria-modal="true"
			aria-labelledby="modal-title"
		>
			<div class="flex justify-between items-center p-4 border-b">
				<h2 id="modal-title" class="text-xl font-semibold">{title}</h2>
				<button
					on:click={closeModal}
					class="text-gray-500 hover:text-gray-700 p-2 rounded-lg transition-colors"
					aria-label="Close modal"
				>
					<span aria-hidden="true">✕</span>
				</button>
			</div>
			<div class="p-4">
				<slot />
			</div>
			<div class="flex justify-end gap-2 p-4 border-t bg-gray-50">
				<slot name="footer">
					<button
						on:click={closeModal}
						class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
					>
						Close
					</button>
				</slot>
			</div>
		</div>
	</dialog>
{/if}

<style>
	dialog {
		@apply border-0;
	}

	dialog::backdrop {
		@apply backdrop-blur-sm;
	}

	/* Prevent dialog from being highlighted */
	dialog:focus {
		outline: none;
	}

	/* Add focus styles to the dialog content instead */
	dialog > div:focus {
		@apply ring-2 ring-indigo-500 ring-opacity-50;
	}
</style>
