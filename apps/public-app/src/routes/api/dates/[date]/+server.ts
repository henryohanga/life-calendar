import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { config } from '$lib/config';

export const GET: RequestHandler = async ({ params }) => {
	try {
		// Format date from YYYYMMDD to YYYY-MM-DD
		const date = params.date;
		const formattedDate = `${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)}`;

		const apiUrl = `${config.apiUrl}/good-dates`;

		// Make request to backend API
		const response = await fetch(apiUrl, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				birth_date: formattedDate,
				match_on_single_digit: true,
				year: new Date().getFullYear(),
				include_zodiac: true
			})
		});

		if (!response.ok) {
			const errorData = await response.json();
			return new Response(JSON.stringify({ error: errorData.detail || 'Failed to fetch dates' }), {
				status: response.status,
				headers: {
					'Content-Type': 'application/json'
				}
			});
		}

		const data = await response.json();
		console.log('API Response:', data); // For debugging
		return json(data);
	} catch (error) {
		console.error('API Error:', error); // For debugging
		return new Response(JSON.stringify({ error: 'Failed to fetch dates' }), {
			status: 500,
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}
};
