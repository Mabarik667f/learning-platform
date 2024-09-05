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
            type: [String, Number, Boolean] as PropType<
                string | number | boolean
            >,
        },
    },
    emits: ["update:modelValue"],
});
</script>

<template>
    <input
        :type="type"
        :value="modelValue"
        :id="id"
        :placeholder="placeholder"
        class="inp"
        @input="
            $emit(
                'update:modelValue',
                ($event.target as HTMLInputElement).value,
            )
        "
    />
</template>

<style scroped>
.inp {
    width: 100%;
    height: 100%;
    background: transparent;
    color: inherit;
    border: none;
    outline: none;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 40px;
    color: inherit;
    padding: 10px 35px 10px 20px;
}

.inp::placeholder {
    color: inherit;
    font-weight: bold;
}
</style>
