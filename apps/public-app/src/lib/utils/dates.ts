export function formatDate(
	date: string | Date,
	options: Intl.DateTimeFormatOptions = { month: 'short', day: 'numeric' }
): string {
	const dateObj = typeof date === 'string' ? new Date(date) : date;
	return new Intl.DateTimeFormat('en-US', options).format(dateObj);
}
