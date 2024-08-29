<script lang="ts">
import { defineComponent, ref } from "vue";
import FilterInp from "./FilterInp.vue";
import FilterBetween from "./FilterBetween.vue";
import FilterList from "./FilterList.vue";

export default defineComponent({
    components: {
        FilterInp,
        FilterBetween,
        FilterList,
    },
    setup() {},
});
</script>

<template>
    <div class="filter-bar">
        <h3>Фильтры</h3>

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
