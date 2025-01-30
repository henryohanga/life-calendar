interface CalendarEvent {
	title: string;
	description: string;
	startDate: string;
	endDate: string;
}

function formatICalDate(dateStr: string): string {
	const date = new Date(dateStr);
	return date
		.toISOString()
		.replace(/[-:]/g, '')
		.replace(/\.\d{3}/, '');
}

export function generateICalFile(event: CalendarEvent): string {
	const icalContent = [
		'BEGIN:VCALENDAR',
		'VERSION:2.0',
		'PRODID:-//Good Dates//Calendar//EN',
		'CALSCALE:GREGORIAN',
		'BEGIN:VEVENT',
		`DTSTART:${formatICalDate(event.startDate)}`,
		`DTEND:${formatICalDate(event.endDate)}`,
		`SUMMARY:${event.title}`,
		`DESCRIPTION:${event.description.replace(/\n/g, '\\n')}`,
		'END:VEVENT',
		'END:VCALENDAR'
	].join('\r\n');

	return icalContent;
}

export function downloadICalFile(event: CalendarEvent): void {
	const icalContent = generateICalFile(event);
	const blob = new Blob([icalContent], { type: 'text/calendar;charset=utf-8' });
	const link = document.createElement('a');
	link.href = window.URL.createObjectURL(blob);
	link.download = 'good-date.ics';
	document.body.appendChild(link);
	link.click();
	document.body.removeChild(link);
}
