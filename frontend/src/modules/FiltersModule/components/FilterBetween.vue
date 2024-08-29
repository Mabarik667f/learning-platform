<script lang="ts">
import { PropType } from "vue";
import { defineComponent } from "vue";

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
        modelValueFirst: {
            required: true,
            default: "",
            type: [String, Number] as PropType<string | number>,
        },
        modelValueSecond: {
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
        <div class="filter-between">
            <c-input
                :placeholder="'От'"
                :type="type"
                v-model="modelValueFirst"
                :id="idFirst"
            />
            <c-input
                :placeholder="'До'"
                :type="type"
                v-model="modelValueSecond"
                :id="idSecond"
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
