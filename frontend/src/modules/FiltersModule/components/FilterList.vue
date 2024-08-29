<script lang="ts">
import { defineComponent } from "vue";
import { PropType } from "vue";

export default defineComponent({
    props: {
        header: {
            default: "",
            type: String as PropType<string>,
        },
        id: {
            type: String as PropType<string>,
        },
        options: {
            required: true,
            type: Array as PropType<Array<object>>,
        },
        modelValue: {
            required: true,
            default: "",
            type: [String, Number] as PropType<string | number>,
        },
    },
});
</script>

<template>
    <div class="filter-list">
        <span v-if="header">
            {{ header }}
        </span>
        <select></select>
    </div>
</template>

<style scoped></style>
