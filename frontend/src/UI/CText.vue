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
    width: 100%;
    resize: none;
    background: transparent;
    color: inherit;
    border: none;
    outline: none;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 25px;
    color: inherit;
    padding: 10px 30px 10px 20px;
}
</style>
