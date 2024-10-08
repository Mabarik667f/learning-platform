<script lang="ts">
import { defineComponent, PropType, watch, computed } from "vue";
import CourseCard from "./CourseCard.vue";
import { useCourseStore } from "@modules/CoursesModule";
export default defineComponent({
    components: {
        CourseCard,
    },
    props: {
        queryParams: {
            default: "",
            type: String as PropType<string>,
        },
    },
    setup(props) {
        const store = useCourseStore();
        const searchQuery = computed({
            get: () => store.courseSearchQuery,
            set: (value: string) => store.setCourseQuery(value),
        });

        const courses = computed({
            get: () => store.courses,
            set: async () => await store.fetchCourses(props.queryParams),
        });

        watch(
            () => props.queryParams,
            async (newParams) => {
                await store.fetchCourses(newParams);
            },
        );

        watch(
            () => searchQuery.value,
            (query) => {
                store.setCourseQuery(query);
                store.filterCourses();
            },
        );

        return { courses };
    },
});
</script>
<template>
    <ul class="courses-list">
        <div v-if="courses.length < 1">
            <h2>Ничего не найдено!</h2>
        </div>
        <li v-else v-for="course in courses" :key="course.id">
            <CourseCard :course="course" />
        </li>
    </ul>
</template>
<style scoped>
.courses-list {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
}
</style>
