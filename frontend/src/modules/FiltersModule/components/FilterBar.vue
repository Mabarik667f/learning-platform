<script lang="ts">
import { defineComponent, ref } from "vue";
import { getCategories, Category } from "@/modules/CategoriesModule";
import FilterInp from "./FilterInp.vue";
import FilterBetween from "./FilterBetween.vue";
import FilterList from "./FilterList.vue";
import { onMounted } from "vue";

export default defineComponent({
    components: {
        FilterInp,
        FilterBetween,
        FilterList,
    },
    setup() {
        const categories = ref<Category[]>([]);
        onMounted(async () => {
            categories.value = await getCategories();
        });
        return { categories };
    },
});
</script>

<template>
    <div class="filter-bar">
        <h3>Фильтры</h3>
        {{ categories }}
        <FilterBetween
            :header="'Цена'"
            :type="'number'"
            :idFirst="'min-price'"
            :idSecond="'max-price'"
            :modelValueFirst="minPrice"
            :modelValueSecond="maxPrice"
        />
        <FilterList
            :header="'Сложность'"
            :id="'diffuculty'"
            :options="[]"
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
                :options="[]"
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
