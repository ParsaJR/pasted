<script setup lang="ts">
import Envelope from './icons/EnvelopeIcon.vue';
import Github from './icons/GithubIcon.vue';
import RefreshIcon from './icons/RefreshIcon.vue';
import SaveIcon from './icons/SaveIcon.vue';
import ForkIcon from './icons/ForkIcon.vue';
import PButton from './PButton.vue';
import PSelect from './PSelect.vue';
import PCheckBox from './PCheckbox.vue';
import { useAppStore } from '../stores/appStore'
import PModal from './PModal.vue';
import { useModal } from '@/composables/modal';
import {moreInfoText} from '@/statics/inventory';
import { computed, watch } from 'vue';

const appStore = useAppStore()

const modal = useModal()
 const MoreInfoDialog = () => {
     modal.show(moreInfoText)
 }

const selectedDuration = defineModel<string>('selectedDuration')

const is_one_time = defineModel<boolean>('is_one_time')

 const emit = defineEmits(['on-clear', 'on-save', 'on-fork'])

 

const selectOptions = computed(() =>
  appStore.apiCapabilities.expiry_durations.map(item => ({
    value: item.code,
    label: item.name,
  }))
)


</script>

<template>
    <div :class="appStore.isSideBarVisible ? 'mask' : ''" @click.self="appStore.toggleSidebar()">
        <aside :class="[
            appStore.isSideBarVisible ? 'translate-x-0' : 'translate-x-full',
            'fixed top-0 right-0 z-40 h-screen w-[75%] sm:w-[35%]',
            'bg-[#f8fafc] transition-transform duration-200',
            'sm:translate-x-0'
        ]" class="" aria-label="Sidebar">
            <div class="h-full px-7 pt-12 pb-8 overflow-y-auto bg-[#f8fafc] flex flex-col items-center gap-3">
                <div
                    class="flex flex-col items-center justify-center px-2 py-1.5 text-body rounded-base hover:bg-neutral-tertiary hover:text-fg-brand group">
                    <img src="../assets/logo.svg" width="120" height="120">
                    <h1 class="text-xl lg:text-[1.8vw] font-bold">Javan's Pastebin</h1>
                    <p class="text-xs lg:text-[0.9vw] font-medium">A Public, Generic pastebin service</p>
                </div>
                <div class="flex flex-col w-full">
                    <div v-if="!appStore.isViewMode" class="flex flex-col gap-4">
                        <PSelect v-model:selected="selectedDuration" :options="selectOptions">
                            <template>
                                Select expiry duration
                            </template>
                        </PSelect>

			<PCheckBox scaleBy="1.3" v-model="is_one_time">
			    Burn on reading
			</PCheckBox>

                        <PButton text="Save" @click="emit('on-save')">
                            <template v-slot:icon>
                                <SaveIcon />
                            </template>
                        </PButton>

                        <PButton text="Clear" @click="emit('on-clear')">
                            <template v-slot:icon>
                                <RefreshIcon />
                            </template>
                        </PButton>
                    </div>
                    <div v-if="appStore.isViewMode" class="flex flex-col gap-4">
                        <PButton title="Fork the code/message and make it yours!" text="Fork" @click="emit('on-fork')">
                            <template v-slot:icon>
                                <ForkIcon />
                            </template>
                        </PButton>
                    </div>
                </div>

                <p class="text-xs font-light mx-2">
                    Keep in mind that, all the information that you save here is possibly available to the
                    public.
		    <span class="underline">
			<button type="button" @click="MoreInfoDialog" class="underline hover:cursor-pointer">More
			    Info</button>
		    </span>
                </p>
                <div class="sidebar-footer flex flex-row gap-5 ">
                    <a href="https://github.com/ParsaJR/pasted" class="p-2 rounded-3xl bg-btn-primary hover:brightness-90">
                        <Github />
                    </a>
                    <a href="mailto:hi@parsajr.ir" class="p-2 rounded-3xl bg-btn-primary hover:brightness-90">
                        <Envelope />
                    </a>
                </div>
            </div>

        </aside>
    </div>



    <PModal :content="appStore.modal.content" :is-open="appStore.modal.isVisible" @on-close="modal.toggle()" />
</template>
<style scoped>
.sidebar-footer {
    margin-top: auto;
}

.mask {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    transition: opacity 0.3s ease;
}
input[type=checkbox] {
    transform: scale(1.5);
}
</style>
