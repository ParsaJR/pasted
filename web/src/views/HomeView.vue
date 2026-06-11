<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { codeToHtml } from 'shiki'
import flourite from 'flourite'

import { useAppStore } from '../stores/appStore'
import { useFormStore } from '@/stores/formStore'
import { userWelcomeText } from '@/statics/inventory'

const appState = useAppStore()


const highlighted = ref('')


const code = defineModel<string>('code')

 function DetectLanguage(code: string): string {
     const language = flourite(code, { shiki: true, noUnknown: true });
     console.info(`Detected language: ${language.language}`)
     return language.language
 }

watch(() => appState.isViewMode, async () => {
	if (appState.isViewMode && code.value) {
		const lang = DetectLanguage(code.value)
		highlighted.value = await codeToHtml(code.value, {
			lang: lang,
			theme: 'github-light'
		})
	}
})

</script>

<template>
	<div class="font-mono text-sm h-auto">
		<div v-if="appState.isViewMode" v-html="highlighted"
			class="h-full w-full resize-none outline-none overflow-auto" placeholder="fmt.Println(&Equal;)"></div>

		<textarea v-else v-model="code" name="code" class="h-full w-full text-code-primary resize-none overflow-auto outline-none"
			:placeholder=userWelcomeText></textarea>
	</div>
</template>


<style scoped>
textarea::placeholder {
	opacity: 0.4
}
</style>
