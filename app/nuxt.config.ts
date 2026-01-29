// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	compatibilityDate: "2025-07-15",

	devtools: { enabled: false },

	modules: ["@nuxt/ui", "@pinia/nuxt"],

	css: ["~/assets/css/main.css"],

	runtimeConfig: {
		public: {
			apiUrl: process.env.API_URL,
		},
	},

	app: {
		pageTransition: { name: "page", mode: "out-in" },
		layoutTransition: { name: "layout", mode: "out-in" },

		head: {
			title: "Classificador de E-mails",
			link: [
				{ rel: 'icon', type: 'image/svg+xml', href: '/mail.svg' }
			]
		}
	},
});