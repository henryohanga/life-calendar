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

		let data = await response.json();

		if (!response.ok) {
			return json(data, { status: response.status });
		}

		// Enhance with AI recommendations if enabled
		if (data.include_zodiac) {
			const aiResponse = await fetch(`${config.apiUrl}/ai/recommendations`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					numerology_number: data.numerology_number,
					zodiac_sign: data.zodiac_sign.name,
					dates: data.dates
				})
			});

			const aiData = await aiResponse.json();
			data = { ...data, ai_recommendations: aiData };
		}

		return json(data);
	} catch (error) {
		console.error('API Error:', error);
		return json(
			{ detail: 'Failed to connect to the service. Please try again later.' },
			{ status: 500 }
		);
	}
};
