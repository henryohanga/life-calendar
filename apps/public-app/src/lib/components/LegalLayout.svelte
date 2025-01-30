<script lang="ts">
	export let title: string;
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 pt-24 pb-16">
	<div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="bg-white rounded-2xl shadow-xl p-8 sm:p-10 border border-gray-100">
			<h1 class="text-3xl font-bold text-gray-900 mb-8">{title}</h1>
			<div class="prose prose-indigo max-w-none">
				<slot />
			</div>
		</div>
	</div>
</div>
