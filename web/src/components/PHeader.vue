<template>
    <header class="h-auto flex px-6 py-3 sm:hidden w-full items-center justify-between bg-primary">
        <div>
            <a href="#">
                <img class="h-8 w-auto text-left" src="../assets/logo.svg" width="120" height="120">
            </a>
        </div>
        <div>
            <button class="flex items-center" @click="appStore.toggleSidebar()">
                <AlignRightIcon />
            </button>
        </div>
    </header>
</template>

<script lang="ts" setup>
import { useAppStore } from '@/stores/appStore';
import AlignRightIcon from './icons/AlignRightIcon.vue';


const appStore = useAppStore()
</script>

<style></style>
