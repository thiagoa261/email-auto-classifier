<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const { toastSuccess } = useAppToast();

const items = computed<NavigationMenuItem[]>(() => [
	{
		label: "Inicio",
		icon: "i-lucide-home",
		to: "/",
		active: route.path === "/",
	},
	{
		label: "Emails",
		icon: "i-lucide-mail",
		to: "/emails",
		active: route.path.startsWith("/emails"),
	},
]);

async function logout() {
	await authStore.logout();
	toastSuccess("Deslogando...");
	await router.push("/login");
}
</script>

<template>
	<UHeader mode="slideover">
		<template #title>
			<p>Classificador de Emails</p>
		</template>

		<UNavigationMenu :items="items" />

		<template #right>
			<UTooltip text="Abrir no GitHub">
				<UButton
					color="neutral"
					variant="ghost"
					to="https://github.com/thiagoa261/email-auto-classifier"
					target="_blank"
					icon="i-simple-icons-github"
					aria-label="GitHub"
				/>
			</UTooltip>

			<UTooltip text="Sair">
				<UButton color="error" variant="ghost" icon="i-lucide-log-out" aria-label="Logout" @click="logout" />
			</UTooltip>
		</template>

		<template #body>
			<UNavigationMenu :items="items" orientation="vertical" />
		</template>
	</UHeader>
</template>
