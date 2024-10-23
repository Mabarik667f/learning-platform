<script lang="ts">
import { defineComponent, PropType } from "vue";
import { BaseModel } from "@/interfaces/objectsInterfaces";
export default defineComponent({
    name: "c-select",
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
        options: {
            required: true,
            default: () => [],
            type: Array as PropType<BaseModel[]>,
        },
    },
    emits: ["update:modelValue"],
});
</script>

<template>
    <select
        :id="id"
        :placeholder="placeholder"
        :value="modelValue"
        @input="
            $emit(
                'update:modelValue',
                ($event.target as HTMLInputElement).value,
            )
        "
    >
        <option v-for="opt in options" :key="opt.id ? opt.id : opt.title">
            {{ opt.title }}
        </option>
    </select>
</template>

<style scroped></style>
