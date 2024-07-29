<script lang="ts">
import { defineComponent, PropType } from "vue";
export default defineComponent({
    name: "c-input",
    props: {
        type: {
            default: "",
            type: String as PropType<string>,
        },
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
});
</script>

<template>
    <input
        :type="type"
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

<style scroped></style>
