<script lang="ts">
import { PropType, ref, SetupContext } from "vue";
import { defineComponent } from "vue";
import { updateSingleVal } from "@modules/FiltersModule";
import { watch } from "vue";

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
        queryVal: {
            default: "",
            type: String as PropType<string>,
        },
    },
    emits: ["updateFilterInp"],
    setup(props, { emit }: SetupContext) {
        const modelVal = ref<string>("");
        watch(
            () => props.queryVal,
            (newQuery: string) => {
                modelVal.value = newQuery;
            },
        );

        const handleInp = async (event: Event) => {
            await updateSingleVal(event, modelVal.value, emit);
        };
        return { modelVal, handleInp };
    },
});
</script>

<template>
    <div class="filter-inp">
        <span class="filter-header">{{ header }}</span>
        <c-input
            :placeholder="placeholder"
            :type="type"
            v-model="modelVal"
            :id="id"
            @input="handleInp($event)"
        />
    </div>
</template>

<style scoped></style>
