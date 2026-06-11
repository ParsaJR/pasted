<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter()
setTimeout(() => {
    router.push("/")
}, 2000);

</script>
<template>
    you lost? Let's get back to the home route.
</template>
