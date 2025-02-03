interface ZodiacSign {
	name: string;
	symbol: string;
	element: string;
	dateRange: string;
	traits: string[];
	favorableActivities: string[];
}

export const zodiacSigns: Record<string, ZodiacSign> = {
	aries: {
		name: 'Aries',
		symbol: '♈',
		element: 'Fire',
		dateRange: 'March 21 - April 19',
		traits: ['Leadership', 'Energy', 'Adventure'],
		favorableActivities: ['Starting new projects', 'Physical activities', 'Competitive events']
	},
	taurus: {
		name: 'Taurus',
		symbol: '♉',
		element: 'Earth',
		dateRange: 'April 20 - May 20',
		traits: ['Stability', 'Patience', 'Determination'],
		favorableActivities: ['Financial planning', 'Creative work', 'Nature activities']
	},
	gemini: {
		name: 'Gemini',
		symbol: '♊',
		element: 'Air',
		dateRange: 'May 21 - June 20',
		traits: ['Adaptability', 'Communication', 'Curiosity'],
		favorableActivities: ['Learning', 'Social events', 'Writing']
	},
	cancer: {
		name: 'Cancer',
		symbol: '♋',
		element: 'Water',
		dateRange: 'June 21 - July 22',
		traits: ['Intuition', 'Nurturing', 'Emotional depth'],
		favorableActivities: ['Family gatherings', 'Home improvement', 'Self-care']
	},
	leo: {
		name: 'Leo',
		symbol: '♌',
		element: 'Fire',
		dateRange: 'July 23 - August 22',
		traits: ['Confidence', 'Creativity', 'Generosity'],
		favorableActivities: ['Performance', 'Leadership roles', 'Creative expression']
	},
	virgo: {
		name: 'Virgo',
		symbol: '♍',
		element: 'Earth',
		dateRange: 'August 23 - September 22',
		traits: ['Analysis', 'Practicality', 'Service'],
		favorableActivities: ['Organization', 'Health routines', 'Problem-solving']
	},
	libra: {
		name: 'Libra',
		symbol: '♎',
		element: 'Air',
		dateRange: 'September 23 - October 22',
		traits: ['Balance', 'Harmony', 'Justice'],
		favorableActivities: ['Negotiations', 'Art appreciation', 'Social harmony']
	},
	scorpio: {
		name: 'Scorpio',
		symbol: '♏',
		element: 'Water',
		dateRange: 'October 23 - November 21',
		traits: ['Intensity', 'Passion', 'Investigation'],
		favorableActivities: ['Research', 'Transformation', 'Deep connections']
	},
	sagittarius: {
		name: 'Sagittarius',
		symbol: '♐',
		element: 'Fire',
		dateRange: 'November 22 - December 21',
		traits: ['Optimism', 'Adventure', 'Philosophy'],
		favorableActivities: ['Travel', 'Learning', 'Sports']
	},
	capricorn: {
		name: 'Capricorn',
		symbol: '♑',
		element: 'Earth',
		dateRange: 'December 22 - January 19',
		traits: ['Ambition', 'Discipline', 'Responsibility'],
		favorableActivities: ['Career planning', 'Goal setting', 'Business']
	},
	aquarius: {
		name: 'Aquarius',
		symbol: '♒',
		element: 'Air',
		dateRange: 'January 20 - February 18',
		traits: ['Innovation', 'Humanitarianism', 'Independence'],
		favorableActivities: ['Networking', 'Technology', 'Social causes']
	},
	pisces: {
		name: 'Pisces',
		symbol: '♓',
		element: 'Water',
		dateRange: 'February 19 - March 20',
		traits: ['Intuition', 'Creativity', 'Compassion'],
		favorableActivities: ['Artistic pursuits', 'Meditation', 'Helping others']
	}
};

export function getZodiacSign(birthDate: string): ZodiacSign {
	const date = new Date(birthDate);
	const month = date.getMonth() + 1;
	const day = date.getDate();
	const mmdd = `${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;

	if (mmdd >= '03-21' && mmdd <= '04-19') return zodiacSigns.aries;
	if (mmdd >= '04-20' && mmdd <= '05-20') return zodiacSigns.taurus;
	if (mmdd >= '05-21' && mmdd <= '06-20') return zodiacSigns.gemini;
	if (mmdd >= '06-21' && mmdd <= '07-22') return zodiacSigns.cancer;
	if (mmdd >= '07-23' && mmdd <= '08-22') return zodiacSigns.leo;
	if (mmdd >= '08-23' && mmdd <= '09-22') return zodiacSigns.virgo;
	if (mmdd >= '09-23' && mmdd <= '10-22') return zodiacSigns.libra;
	if (mmdd >= '10-23' && mmdd <= '11-21') return zodiacSigns.scorpio;
	if (mmdd >= '11-22' && mmdd <= '12-21') return zodiacSigns.sagittarius;
	if (mmdd >= '12-22' || mmdd <= '01-19') return zodiacSigns.capricorn;
	if (mmdd >= '01-20' && mmdd <= '02-18') return zodiacSigns.aquarius;
	return zodiacSigns.pisces;
}
