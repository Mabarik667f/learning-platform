<script lang="ts">
import { PropType, ref } from "vue";
import { defineComponent, SetupContext } from "vue";
import { updateSingleVal } from "@modules/FiltersModule";

export default defineComponent({
    props: {
        type: {
            default: "",
            type: String as PropType<string>,
        },
        header: {
            required: true,
            type: String as PropType<string>,
        },
        idFirst: {
            type: String as PropType<string>,
        },
        idSecond: {
            type: String as PropType<string>,
        },
    },
    emits: ["updateVal1", "updateVal2"],
    setup(props, { emit }: SetupContext) {
        const postfix = ref<string>("");
        const modelVal1 = ref<string>("");
        const modelVal2 = ref<string>("");

        const handleInp = async (event: Event, model: string) => {
            if (model == "model1") {
                postfix.value = "Val1";
            } else {
                postfix.value = "Val2";
            }
            await updateSingleVal(event, modelVal1.value, emit, postfix.value);
        };

        return { modelVal1, modelVal2, handleInp };
    },
});
</script>

<template>
    <div class="filter-inp">
        <span class="filter-header">{{ header }}</span>
        <div class="filter-between">
            <c-input
                :placeholder="'От'"
                :type="type"
                v-model="modelVal1"
                :id="idFirst"
                @input="handleInp($event, 'model1')"
            />
            <c-input
                :placeholder="'До'"
                :type="type"
                v-model="modelVal2"
                :id="idSecond"
                @input="handleInp($event, 'model2')"
            />
        </div>
    </div>
</template>

<style scoped>
.filter-between {
    display: flex;
    flex-direction: row;
}
</style>
