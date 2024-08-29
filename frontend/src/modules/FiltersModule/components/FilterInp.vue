<script lang="ts">
import { PropType } from "vue";
import { defineComponent } from "vue";

export default defineComponent({
    props: {
        placeholder: {
            default: "",
            type: String as PropType<string>,
        },
        type: {
            default: "",
            type: String as PropType<string>,
        },
        header: {
            required: true,
            type: String as PropType<string>,
        },
        id: {
            type: String as PropType<string>,
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
    <div class="filter-inp">
        <span class="filter-header">{{ header }}</span>
        <c-input
            :placeholder="placeholder"
            :type="type"
            v-model="modelValue"
            :id="id"
        />
    </div>
</template>

<style scoped></style>
