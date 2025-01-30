export interface GoodDatesResponse {
	dates: string[];
	numerology_number: number;
	number_meaning: string;
	total_matches: number;
}

export interface GoodDatesRequest {
	birth_date: string;
	match_on_single_digit: boolean;
	year?: number;
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
