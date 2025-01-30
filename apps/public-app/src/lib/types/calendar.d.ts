declare module '@event-calendar/core' {
	export default class Calendar {
		constructor(options: { target: HTMLElement; props: any });
		$set(props: any): void;
		$destroy(): void;
	}
}

declare module '@event-calendar/day-grid' {
	const plugin: any;
	export default plugin;
}
