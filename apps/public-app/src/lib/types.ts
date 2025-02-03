export interface GoodDateResponse {
	dates: string[];
	numerology_number: number;
	number_meaning: string;
	total_matches: number;
	zodiac_sign?: {
		name: string;
		symbol: string;
		element: string;
		date_range: string;
		power_periods: Array<{
			start_date: string;
			end_date: string;
			dates: string[];
			duration: number;
		}>;
		date_specific_advice: Record<
			string,
			{
				activities: string[];
				timing: string;
				power_level: number;
				category: 'career' | 'personal' | 'rest' | 'financial';
			}
		>;
		career: string[];
		personal: string[];
		rest: string[];
		financial: string[];
	};
}

export interface GoodDatesRequest {
	birth_date: string;
	match_on_single_digit: boolean;
	year?: number;
	include_zodiac: boolean;
}

export interface CalendarEvent {
	id: string;
	start: string;
	end: string;
	title: string;
	color?: string;
	textColor?: string;
	display?: 'auto' | 'block' | 'list-item' | 'background' | 'inverse-background' | 'none';
	allDay?: boolean;
}
