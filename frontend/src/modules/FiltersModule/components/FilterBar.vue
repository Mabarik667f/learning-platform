<script lang="ts">
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

export default defineComponent({
    components: {
        FilterInp,
        FilterBetween,
        FilterList,
        ApplyButton,
    },
    setup() {
        const categories = ref<FilterOption[]>([]);
        const difficulties = ref<FilterOption[]>([]);
        const queryCat = ref<string>("");
        const prices = ref<Prices>({
            minPrice: "",
            maxPrice: "",
        });
        onMounted(async () => {
            categories.value = await getCategories();
            difficulties.value = await getDifficulties();
        });

        const handleSingleInp = (newVal: any, model: string) => {
            console.log(newVal, model);
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
        return { categories, difficulties, queryCat, prices, handleSingleInp };
    },
});
</script>

<template>
    <div class="filter-bar">
        <h3>Фильтры</h3>
        <ApplyButton />
        {{ categories }}
        {{ difficulties }}
        <FilterBetween
            :header="'Цена'"
            :type="'number'"
            :idFirst="'min-price'"
            :idSecond="'max-price'"
            @updateVal1="handleSingleInp($event, 'minPrice')"
            @updateVal2="handleSingleInp($event, 'maxPrice')"
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
                @updateFilterInp="handleSingleInp($event, 'queryCat')"
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
    border-radius: 20px;
    padding: 10px;
}
</style>
