<script setup lang="ts">
import { computed, onBeforeMount, ref, Teleport, useTemplateRef, watch } from 'vue';
import PHeader from './components/PHeader.vue';
import { assert, onClickOutside } from '@vueuse/core';
import { useRoute, useRouter } from 'vue-router';
import { useAPI } from './composables/api';
import type { ApiError, ApiResponse } from '@/types/ApiTypes';
import { useAppStore } from './stores/appStore'
import { useFormStore } from './stores/formStore';
import { useToast } from './composables/toast';

const appState = useAppStore()
const formState = useFormStore()

onBeforeMount(async () => {
	try {
		const capabilities = await useAPI().getApiCapabilities()
		appState.populateApiCapabilities(capabilities)
	}
	catch (error) {
		console.log(error)
	}
})

const selectedDuration = ref()


// The empty string means the first option on the PSelect component, which is the placeholder.
selectedDuration.value = ""

// Faciliates the toggle functionality between the mobile toggle button and the sidebar.
const sideBarOpen = ref(false)

// On click outside, Close the sidebar.
const target = useTemplateRef<HTMLElement>('target')

onClickOutside(target, () => sideBarOpen.value = false)


const route = useRoute()

const router = useRouter()

watch(
	() => route.params.shortcode,
	async (shortcode) => {
		if (shortcode && !Array.isArray(shortcode) && !appState.isViewMode) {
			try {
				const result = await useAPI().getPasted(shortcode) as ApiResponse
				formState.mutateCode(result.content)
				appState.toggleViewMode()
			}
			catch (apiError) {
				const error = apiError as ApiError
				formState.mutateCode(`${error.detail}`)
			}

		}
	}
)


async function save() {
	if (!formState.code) {
		useToast("An empty text, cannot be saved.", 'info')
		return
	}
	if (!formState.duration) {
	    useToast("Please select an expiry duration.", 'info')
	    return
	}

	if (formState.duration) {
		const code = formState.code
		const duration = formState.duration
		const is_one_time = formState.is_one_time

		try {
			const result = await useAPI().postPasted({
				content: code,
				expiry_code: duration,
				is_one_time: is_one_time
			})
			appState.toggleViewMode()

			router.push(result)
		}
		catch (error) {
			const err = error as ApiError
			useToast(err.statusText, 'error')
		}

	}
	else {
		useToast("Fill the required fields", 'error')
	}
}
</script>

<template>
	<PHeader />
	<div class="px-5 py-3 flex-1 flex">
		<Suspense>
			<RouterView name="default" class="w-full sm:w-[65%]" v-model:code="formState.code"></RouterView>
			<template #fallback>
				Loading...
			</template>
		</Suspense>
		<RouterView ref="target" name="RightSidebar" v-model:selectedDuration="formState.duration"
			@on-clear="formState.mutateCode('')" @on-save="save" @on-fork="appState.toggleViewMode()"
			v-model:is_one_time="formState.is_one_time">
		</RouterView>
	</div>
</template>

<style scoped></style>
