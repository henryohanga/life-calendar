<script>
	import '@event-calendar/core/index.css';
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import '$lib/styles/calendar.css';
</script>

<div class="flex flex-col min-h-screen">
	<Navbar />
	<main class="flex-1 pt-16">
		<slot />
	</main>
	<Footer />
</div>
