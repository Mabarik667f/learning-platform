<script lang="ts">
import { defineComponent, ref, SetupContext, watch, PropType } from "vue";
import { FilterOption } from "../interfaces/FilterOption";
import { selectOption, unSelectOption } from "../helpers/useToggleOptions";

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
    },
    emits: ["updateListVal"],
    setup(props, { emit }: SetupContext) {
        const options = ref<FilterOption[]>(props.options);
        const selectedOptions = ref<FilterOption[]>([]);
        const toggleOptions = ref<boolean[]>([]);

        // добавить checbox для выбранных
        watch(
            () => props.options,
            (newOptions: FilterOption[]) => {
                if (newOptions.length !== options.value.length) {
                    options.value = newOptions;
                    toggleOptions.value = newOptions.map(() => false);
                }
            },
        );

        const toggle = async (event: Event, index: number) => {
            toggleOptions.value[index] = (
                event.target as HTMLInputElement
            ).checked;

            if (toggleOptions.value[index]) {
                await selectOption(selectedOptions, props.options[index]);
            } else {
                await unSelectOption(selectedOptions, props.options[index]);
            }
            emit("updateListVal", selectedOptions.value);
        };

        return {
            selectedOptions,
            toggleOptions,
            toggle,
            selectOption,
            unSelectOption,
        };
    },
});
</script>

<template>
    <div class="filter-list">
        {{ selectedOptions }}
        <span v-if="header">
            {{ header }}
        </span>
        <ul class="filter-options">
            <li
                v-for="(option, i) in options"
                :key="option.id ? option.id : option.title"
            >
                <c-input
                    :type="'checkbox'"
                    @input="toggle($event, i)"
                    v-model="toggleOptions[i]"
                />
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
