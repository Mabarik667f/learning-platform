<script lang="ts">
import { defineComponent } from "vue";
import { PropType } from "vue";
import { FilterOption } from "../interfaces/FilterOption";

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
            type: Array as PropType<Array<FilterOption>>,
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
        <ul class="filter-options">
            <li
                v-for="option in options"
                :key="option.id ? option.id : option.title"
            >
                <c-input :type="'checkbox'" />
                <span>{{ option.title }}</span>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.filter-options {
    list-style: none;
}

.filter-options li {
    display: flex;
    flex-direction: row;
    margin: 5px;
}
</style>
