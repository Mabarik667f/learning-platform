<script lang="ts">
import { defineComponent, PropType } from "vue";
export default defineComponent({
    name: "c-text",
    props: {
        placeholder: {
            default: "",
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
    emits: ["update:modelValue"],
});
</script>

<template>
    <textarea
        :value="modelValue"
        :id="id"
        :placeholder="placeholder"
        @input="
            $emit(
                'update:modelValue',
                ($event.target as HTMLInputElement).value,
            )
        "
    />
</template>

<style scroped>
textarea {
    border: 1px solid black;
    border-radius: 8px;
    resize: none;
}
</style>
