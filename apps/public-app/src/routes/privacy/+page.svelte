<script lang="ts">
	import { fly } from 'svelte/transition';
	import LegalLayout from '$lib/components/LegalLayout.svelte';
</script>

<div in:fly={{ y: 20, duration: 300 }}>
	<LegalLayout title="Privacy Policy">
		<h2>Introduction</h2>
		<p>
			At Good Dates, we take your privacy seriously. This Privacy Policy explains how we collect,
			use, and protect your personal information when you use our service.
		</p>

		<h2>Information We Collect</h2>
		<p>We collect the following information when you use Good Dates:</p>
		<ul>
			<li>Your birth date (for numerology calculations)</li>
			<li>Basic usage data (for service improvement)</li>
		</ul>

		<h2>How We Use Your Information</h2>
		<p>We use your information to:</p>
		<ul>
			<li>Calculate auspicious dates based on your numerology number</li>
			<li>Improve our service and user experience</li>
			<li>Maintain and secure our platform</li>
		</ul>

		<h2>Data Protection</h2>
		<p>
			We implement appropriate technical and organizational measures to protect your personal
			information. Your birth date is only used for calculations and is not stored permanently.
		</p>

		<h2>Third-Party Services</h2>
		<p>
			We do not share your personal information with third parties. Our service uses minimal
			external services to provide core functionality.
		</p>

		<h2>Your Rights</h2>
		<p>You have the right to:</p>
		<ul>
			<li>Access your personal information</li>
			<li>Request deletion of your data</li>
			<li>Object to processing of your data</li>
		</ul>

		<h2>Contact Us</h2>
		<p>
			If you have any questions about this Privacy Policy, please contact us at
			<a href="mailto:privacy@gooddates.app">privacy@gooddates.app</a>.
		</p>

		<h2>Updates to This Policy</h2>
		<p>
			We may update this Privacy Policy from time to time. The latest version will always be
			available on this page.
		</p>

		<p class="text-sm text-gray-500 mt-8">Last updated: {new Date().toLocaleDateString()}</p>
	</LegalLayout>
</div>
