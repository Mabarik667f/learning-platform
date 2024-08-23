<script lang="ts">
import { ref } from "vue";
import { defineComponent } from "vue";
export default defineComponent({
    setup() {
        const query = ref<string>("");
        return { query };
    },
});
</script>

<template>
    <c-input v-model="query" class="search-query"></c-input>
</template>

<style scoped>
.search-query {
    border: none;
    background-color: #fff;
    border-radius: 15px;
    flex-grow: 1;
}
</style>
