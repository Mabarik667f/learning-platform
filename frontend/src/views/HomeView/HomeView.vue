<template>
    <div class="home">
        <div class="search-con">
            <SearchField />
        </div>
        <div class="filters-con">
            <FilterBar />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { SearchField } from "@/modules/SearchModule";
import { FilterBar } from "@/modules/FiltersModule";

export default defineComponent({
    components: {
        SearchField,
        FilterBar,
    },
    setup() {
        return {};
    },
});
</script>

<style scoped>
.home {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
}

.search-con {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
}

.filters-con {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    margin: 0;
    padding: 0;
    width: 100%;
}
</style>
