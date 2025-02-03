import type { GoodDateResponse } from './api';

export type CategoryColor = {
	base: string;
	bg: string;
	icon: string;
};

export type CategoryColors = Record<string, CategoryColor>;

export type TimeSlot = {
	start: string;
	end: string;
};

export type TimeMap = Record<string, TimeSlot>;

export type CalendarProps = {
	results: GoodDateResponse;
};
