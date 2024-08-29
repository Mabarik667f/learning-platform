<template>
    <div class="home">
        <SearchField />
        <FilterBar />
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
    flex: 1;
}
</style>
