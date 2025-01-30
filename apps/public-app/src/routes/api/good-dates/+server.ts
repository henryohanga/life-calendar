import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { config } from '$lib/config';

export const POST: RequestHandler = async ({ request }) => {
	try {
		const response = await fetch(`${config.apiUrl}/good-dates/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(await request.json())
		});

		const data = await response.json();

		if (!response.ok) {
			return json(data, { status: response.status });
		}

		return json(data);
	} catch (error) {
		console.error('API Error:', error);
		return json(
			{ detail: 'Failed to connect to the numerology service. Please try again later.' },
			{ status: 500 }
		);
	}
};
