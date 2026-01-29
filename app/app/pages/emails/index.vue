<script setup lang="ts">
import axios from "axios";
import { ref, onMounted, watch, reactive } from "vue";
import { useAuthStore } from "~/stores/auth";
import { useAppToast } from "~/composables/useAppToast";
import type { IEmail, IListResponse } from "~/types/response";

const UButton = resolveComponent("UButton");
const Icon = resolveComponent("Icon");

const config = useRuntimeConfig();
const authStore = useAuthStore();
const { toastError } = useAppToast();

const loading = ref(false);
const emails = ref<IEmail[]>([]);
const total = ref(0);

const filters = reactive({
	page: 1,
	limit: 5,
});

const showModal = ref(false);
const selectedEmail = ref<IEmail | null>(null);

const columns = [
	{
		accessorKey: "#",
		header: "Vizualizar",
		cell: ({ row }: { row: any }) => {
			return h(
				UButton,
				{
					color: "neutral",
					variant: "ghost",
					onClick: () => (selectedEmail.value = row.original) && (showModal.value = true),
				},
				() => h(Icon, { name: "i-lucide-eye" }, () => null),
			);
		},
	},
	{
		accessorKey: "category",
		header: "Categoria",
	},
	{
		accessorKey: "_id",
		header: "ID",
	},
	{
		accessorKey: "created_at",
		header: "Data",
		cell: ({ row }: { row: any }) => {
			return new Date(row.getValue("created_at")).toLocaleString("pt-BR");
		},
	},
];

async function fetchEmails() {
	loading.value = true;
	try {
		const token = await authStore.getToken();
		if (!token) {
			toastError("Usuário não autenticado.");
			return;
		}

		const offset = (filters.page - 1) * filters.limit;

		const response = await axios.post<IListResponse>(
			`${config.public.apiUrl}/email/listar`,
			{ offset, limit: filters.limit },
			{ headers: { token } },
		);

		if (response.status !== 200) {
			toastError("Erro ao buscar emails.");
			return;
		}

		emails.value = response.data.emails;
		total.value = response.data.total;
	} catch (err) {
		toastError("Erro ao buscar emails.");
	} finally {
		loading.value = false;
	}
}

onMounted(() => {
	fetchEmails();
});
</script>

<template>
	<div class="flex flex-col gap-5 w-full">
		<UCard>
			<template #header>
				<div class="flex items-center gap-3 justify-center">
					<Icon name="i-lucide-table" class="w-7 h-7" />
					<span class="font-semibold">Emails Salvos</span>
				</div>
			</template>

			<UTable :data="emails" :columns="columns" :loading="loading" />

			<div class="flex justify-end mt-4">
				<UPagination
					:default-page="1"
					:items-per-page="filters.limit"
					:total="total"
					@update:page="
						(p) => {
							filters.page = p;
							fetchEmails();
						}
					"
				/>
			</div>
		</UCard>

		<UModal
			v-model:open="showModal"
			:close="{
				color: 'error',
				variant: 'outline',
				class: 'rounded-full',
			}"
			:fullscreen="true"
		>
			<template #body>
				<UCard>
					<template #header>
						<div class="flex items-center gap-3">
							<Icon name="i-lucide-mail-open" class="w-6 h-6" />
							<span class="font-semibold">Detalhes do Email:</span>
						</div>
					</template>

					<div v-if="selectedEmail" class="flex flex-col gap-3">
						<div class="flex gap-3 flex-col md:flex-row w-full">
							<div class="w-full md:w-1/2">
								<UFormField label="Categoria:">
									<UInput v-model="selectedEmail.category" disabled class="w-full" />
								</UFormField>
							</div>

							<div class="w-full md:w-1/2">
								<UFormField label="Data de Criação:">
									<UInput :model-value="new Date(selectedEmail.created_at).toLocaleString('pt-BR')" disabled class="w-full" />
								</UFormField>
							</div>
						</div>

						<UFormField label="Conteúdo:">
							<UTextarea v-model="selectedEmail.content" disabled :rows="7" style="resize: none" class="w-full" />
						</UFormField>

						<UFormField label="Justificativa:">
							<UTextarea v-model="selectedEmail.justification" disabled :rows="3" style="resize: none" class="w-full" />
						</UFormField>

						<UFormField label="Resposta sugerida:">
							<UTextarea v-model="selectedEmail.response" disabled :rows="7" style="resize: none" class="w-full" />
						</UFormField>
					</div>
				</UCard>
			</template>
		</UModal>
	</div>
</template>
