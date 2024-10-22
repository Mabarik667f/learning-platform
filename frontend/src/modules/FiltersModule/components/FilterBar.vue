<script lang="ts">
import {
    defineComponent,
    onMounted,
    SetupContext,
    ref,
    watch,
    computed,
} from "vue";
import { useRouter, useRoute } from "vue-router";
import { getDifficulties } from "@modules/CoursesModule";
import { getQueryParams, updateRouteQueryParams } from "../helpers/queryParams";
import { FilterOption, Prices } from "../interfaces";
import FilterInp from "./FilterInp.vue";
import FilterBetween from "./FilterBetween.vue";
import FilterList from "./FilterList.vue";
import ApplyButton from "./ApplyButton.vue";
import { useCategoryStore } from "@/modules/CategoriesModule";

export default defineComponent({
    components: {
        FilterInp,
        FilterBetween,
        FilterList,
        ApplyButton,
    },
    emits: ["updateQueryParams"],
    setup(_, { emit }: SetupContext) {
        const categoryStore = useCategoryStore();

        const router = useRouter();
        const route = useRoute();

        const categories = computed({
            get: () => categoryStore.categories,
            set: async () => await categoryStore.fetchCategories(),
        });

        const difficulties = ref<FilterOption[]>([]);

        const selectedCats = ref<FilterOption[]>([]);
        const selectedDifficulties = ref<FilterOption[]>([]);

        const queryCat = computed({
            get: () => categoryStore.categorySearchQuery,
            set: (query: string) => categoryStore.setCategoryQuery(query),
        });

        const prices = ref<Prices>({
            min_price: "",
            max_price: "",
        });

        onMounted(async () => {
            await setQueryParams();
            emit("updateQueryParams", route.fullPath);
        });

        const setQueryParams = async () => {
            await categoryStore.fetchCategories();
            difficulties.value = await getDifficulties();

            const queryDifficulties: string[] =
                (route.query.difficulties as string[]) || [];

            const categoryIds: number[] =
                (route.query.categories as string[])?.map((id) => Number(id)) ||
                [];

            selectedCats.value =
                categories.value.filter((cat) =>
                    categoryIds.includes(Number(cat.id)),
                ) || [];
            selectedDifficulties.value =
                difficulties.value.filter((diff) =>
                    queryDifficulties.includes(diff.title),
                ) || [];

            categoryStore.setCategoryQuery(
                (route.query.queryCat as string) || "",
            );
            prices.value.min_price = (route.query.min_price as string) || "";
            prices.value.max_price = (route.query.max_price as string) || "";
        };

        watch(
            () => queryCat.value,
            (_) => {
                categoryStore.filterCategories();
            },
        );

        const handleSingleInp = async (newVal: any, model: string) => {
            switch (model) {
                case "queryCat":
                    categoryStore.setCategoryQuery(newVal);
                    await updateRoute();
                    break;
                case "minPrice":
                    prices.value.min_price = newVal;
                    break;
                case "maxPrice":
                    prices.value.max_price = newVal;
                    break;
            }
        };

        const handleListUpdate = async (
            values: FilterOption[],
            model: string,
        ) => {
            switch (model) {
                case "category":
                    selectedCats.value = values;
                    break;
                case "difficulty":
                    selectedDifficulties.value = values;
                    break;
            }
            await updateRoute();
        };

        const updateRoute = async () => {
            const queryParams = getQueryParams(
                prices.value,
                queryCat.value,
                selectedDifficulties.value,
                selectedCats.value,
            );
            await updateRouteQueryParams(router, queryParams);
        };

        watch(
            () => route.fullPath,
            async (newPath: string) => {
                emit("updateQueryParams", newPath);
            },
        );
        return {
            categories,
            difficulties,
            selectedCats,
            selectedDifficulties,
            queryCat,
            prices,
            handleSingleInp,
            handleListUpdate,
            updateRoute,
        };
    },
});
</script>

<template>
    <div class="filter-bar">
        <h3>Фильтры</h3>
        <ApplyButton @click="updateRoute" />
        {{ selectedCats }}
        {{ selectedDifficulties }}
        <FilterBetween
            :header="'Цена'"
            :type="'number'"
            :idFirst="'min-price'"
            :idSecond="'max-price'"
            @updateVal1="handleSingleInp($event, 'minPrice')"
            @updateVal2="handleSingleInp($event, 'maxPrice')"
            :queryVal1="prices.min_price"
            :queryVal2="prices.max_price"
        />
        <FilterList
            :header="'Сложность'"
            :id="'difficulty'"
            :options="difficulties"
            :queryList="selectedDifficulties"
            @updateListVal="handleListUpdate($event, 'difficulty')"
        />
        <div>
            <FilterInp
                :header="'Категория'"
                :id="'search-cat'"
                :queryVal="queryCat"
                @updateFilterInp="handleSingleInp($event, 'queryCat')"
            />
            <FilterList
                :id="'categories'"
                :options="categories"
                :queryList="selectedCats"
                @updateListVal="handleListUpdate($event, 'category')"
            />
        </div>
    </div>
</template>

<style scoped>
.filter-bar {
    display: flex;
    flex-direction: column;
    background: #6d8a51;
    border-radius: 20px;
    padding: 10px;
}
</style>
