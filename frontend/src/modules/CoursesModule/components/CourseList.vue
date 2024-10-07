<script lang="ts">
import { defineComponent, ref, PropType, watch } from "vue";
import getCourseList from "../api/getCourseList";
export default defineComponent({
    props: {
        queryParams: {
            default: "",
            type: String as PropType<string>,
        },
    },
    setup(props) {
        const courses = ref<Object>({});
        const query = ref<string>(props.queryParams);

        const getCourses = async () => {
            courses.value = await getCourseList(query.value);
        };

        watch(
            () => props.queryParams,
            async (newParams) => {
                query.value = newParams;
                await getCourses();
            },
        );

        return { courses };
    },
});
</script>
<template>
    <div>
        {{ courses }}
    </div>
</template>
<style scoped></style>
