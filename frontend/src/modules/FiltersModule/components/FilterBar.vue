<script lang="ts">
import { defineComponent, ref } from "vue";
import { getCategories } from "@/modules/CategoriesModule";
import { FilterOption } from "../interfaces/FilterOption";
import { Prices } from "../interfaces/Prices";
import FilterInp from "./FilterInp.vue";
import FilterBetween from "./FilterBetween.vue";
import FilterList from "./FilterList.vue";
import { onMounted } from "vue";
import { getDifficulties } from "@modules/CoursesModule";

export default defineComponent({
    components: {
        FilterInp,
        FilterBetween,
        FilterList,
    },
    setup() {
        const categories = ref<FilterOption[]>([]);
        const difficulties = ref<FilterOption[]>([]);
        const queryCat = ref<string>("");
        const prices = ref<Prices>({
            minPrice: 0,
            maxPrice: 0,
        });
        onMounted(async () => {
            categories.value = await getCategories();
            difficulties.value = await getDifficulties();
        });
        return { categories, difficulties, queryCat, prices };
    },
});
</script>

<template>
    <div class="filter-bar">
        <h3>Фильтры</h3>
        {{ categories }}
        {{ difficulties }}
        <FilterBetween
            :header="'Цена'"
            :type="'number'"
            :idFirst="'min-price'"
            :idSecond="'max-price'"
            :modelValueFirst="prices.minPrice"
            :modelValueSecond="prices.maxPrice"
        />
        <FilterList
            :header="'Сложность'"
            :id="'diffuculty'"
            :options="difficulties"
            :modelValue="difficulties"
        />
        <div>
            <FilterInp
                :header="'Категория'"
                :id="'search-cat'"
                :modelValue="queryCat"
            />
            <FilterList
                :id="'categories'"
                :options="categories"
                :modelValue="categories"
            />
        </div>
    </div>
</template>

<style scoped>
.filter-bar {
    display: flex;
    flex-direction: column;
    background: #6d8a51;
}
</style>
