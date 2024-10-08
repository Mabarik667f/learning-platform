<script lang="ts">
import { defineComponent, ref } from "vue";
import { SearchField } from "@/modules/SearchModule";
import { FilterBar } from "@/modules/FiltersModule";
import { CourseList, useCourseStore } from "@/modules/CoursesModule";

export default defineComponent({
    components: {
        SearchField,
        FilterBar,
        CourseList,
    },
    setup() {
        const store = useCourseStore();
        const setCourseSearchQuery = store.setCourseQuery;

        const queryParams = ref<string>("");
        const updateCourseList = async (params: string) => {
            queryParams.value = params;
        };

        return {
            updateCourseList,
            queryParams,
            setCourseSearchQuery,
        };
    },
});
</script>

<template>
    <div class="home">
        <div class="search-con">
            <SearchField @getSearchQuery="setCourseSearchQuery($event)" />
        </div>
        <div class="filters-con">
            <FilterBar @updateQueryParams="updateCourseList($event)" />
        </div>
        <div class="courses">
            <CourseList :queryParams="queryParams" />
        </div>
    </div>
</template>

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

.courses {
    display: flex;
    width: 100%;
}
</style>
