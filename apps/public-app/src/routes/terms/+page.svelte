<script lang="ts">
	import { fly } from 'svelte/transition';
	import LegalLayout from '$lib/components/LegalLayout.svelte';
</script>

<div in:fly={{ y: 20, duration: 300 }}>
	<LegalLayout title="Terms of Service">
		<h2>Agreement to Terms</h2>
		<p>
			By accessing and using Good Dates, you agree to be bound by these Terms of Service and all
			applicable laws and regulations.
		</p>

		<h2>Use License</h2>
		<p>
			We grant you a personal, non-exclusive, non-transferable license to use Good Dates for
			personal or business purposes in accordance with these terms.
		</p>

		<h2>Disclaimer</h2>
		<p>
			Good Dates provides numerology-based date suggestions for informational purposes only. We make
			no guarantees about the accuracy or reliability of these suggestions.
		</p>

		<h2>Limitations</h2>
		<p>You agree not to:</p>
		<ul>
			<li>Use the service for any unlawful purpose</li>
			<li>Attempt to gain unauthorized access to our systems</li>
			<li>Interfere with other users' access to the service</li>
			<li>Modify, adapt, or hack the service</li>
		</ul>

		<h2>Intellectual Property</h2>
		<p>
			The service and its original content, features, and functionality are owned by Good Dates and
			are protected by international copyright, trademark, and other intellectual property laws.
		</p>

		<h2>Termination</h2>
		<p>
			We reserve the right to terminate or suspend access to our service immediately, without prior
			notice, for any breach of these Terms of Service.
		</p>

		<h2>Changes to Terms</h2>
		<p>
			We reserve the right to modify or replace these terms at any time. The latest version will
			always be available on this page.
		</p>

		<h2>Contact Us</h2>
		<p>
			If you have any questions about these Terms, please contact us at
			<a href="mailto:legal@gooddates.app">legal@gooddates.app</a>.
		</p>

		<p class="text-sm text-gray-500 mt-8">Last updated: {new Date().toLocaleDateString()}</p>
	</LegalLayout>
</div>
