<script lang="ts">
import { useRouter, useRoute } from "vue-router";
import { defineComponent, ref } from "vue";
import { getCategories } from "@/modules/CategoriesModule";
import { FilterOption } from "../interfaces/FilterOption";
import { Prices } from "../interfaces/Prices";
import FilterInp from "./FilterInp.vue";
import FilterBetween from "./FilterBetween.vue";
import FilterList from "./FilterList.vue";
import ApplyButton from "./ApplyButton.vue";
import { onMounted } from "vue";
import { getDifficulties } from "@modules/CoursesModule";
import { getQueryParams, updateRouteQueryParams } from "../helpers/queryParams";

export default defineComponent({
    components: {
        FilterInp,
        FilterBetween,
        FilterList,
        ApplyButton,
    },
    setup() {
        const router = useRouter();
        const route = useRoute();

        const categories = ref<FilterOption[]>([]);
        const difficulties = ref<FilterOption[]>([]);

        const selectedCats = ref<FilterOption[]>([]);
        const selectedDifficulties = ref<FilterOption[]>([]);

        const queryCat = ref<string>("");
        const prices = ref<Prices>({
            minPrice: "",
            maxPrice: "",
        });

        onMounted(async () => {
            categories.value = await getCategories();
            difficulties.value = await getDifficulties();

            const queryDifficulties: string[] =
                (route.query.difficulties as string)?.split(",") || [];

            const categoryIds: number[] =
                (route.query.categories as string)
                    ?.split(",")
                    .map((id) => Number(id)) || [];

            selectedCats.value =
                categories.value.filter((cat) =>
                    categoryIds.includes(Number(cat.id)),
                ) || [];
            selectedDifficulties.value =
                difficulties.value.filter((diff) =>
                    queryDifficulties.includes(diff.title),
                ) || [];

            queryCat.value = (route.query.queryCat as string) || "";
            prices.value.minPrice = (route.query.minPrice as string) || "";
            prices.value.maxPrice = (route.query.maxPrice as string) || "";
        });

        const handleSingleInp = (newVal: any, model: string) => {
            switch (model) {
                case "queryCat":
                    queryCat.value = newVal;
                    break;
                case "minPrice":
                    prices.value.minPrice = newVal;
                    break;
                case "maxPrice":
                    prices.value.maxPrice = newVal;
                    break;
            }
        };

        const handleListUpdate = (values: FilterOption[], model: string) => {
            switch (model) {
                case "category":
                    selectedCats.value = values;
                    break;
                case "difficulty":
                    selectedDifficulties.value = values;
                    break;
            }
            updateRoute();
        };

        const updateRoute = () => {
            const queryParams = getQueryParams(
                prices.value,
                queryCat.value,
                selectedDifficulties.value,
                selectedCats.value,
            );
            updateRouteQueryParams(router, queryParams);
        };
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
            :queryVal1="prices.minPrice"
            :queryVal2="prices.maxPrice"
        />
        <FilterList
            :header="'Сложность'"
            :id="'difficulty'"
            :options="difficulties"
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
