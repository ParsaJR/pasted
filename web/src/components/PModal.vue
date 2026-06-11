<script setup lang="ts">
import PButton from './PButton.vue';


const props = defineProps({
    isOpen: Boolean,
    content: String,
})

const emit = defineEmits(['on-close'])

</script>
<template>
    <Teleport to="body">
        <transition name="modal">
            <div v-if="props.isOpen" class="modal-mask" @click.self="emit('on-close')">
                <div class="modal-container text-lg whitespace-pre-line pt-3 border border-2 pb-6 w-96 m-auto px-5 bg-white rounded-md shadow-black transition-all">
                    {{ props.content }}
		    <div class="flex justify-center">
		    <PButton @click="emit('on-close')" text="Understood"/>
		    </div>
                </div>
            </div>
        </transition>
    </Teleport>
</template>

<style scoped>
.modal-mask {
	position: fixed;
	z-index: 9998;
	width: 100%;
	height: 100%;
	top: 0;
	left: 0;
	background-color: rgba(200, 200, 200, 0.5);
	display: flex;
	color: black;
	transition: opacity 0.3s ease;
}

.modal-enter-from {
	opacity: 0;
}

.modal-leave-to {
	opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
	-webkit-transform: scale(1.1);
	transform: scale(1.1);
}
</style>
