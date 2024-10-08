<script lang="ts">
import { defineComponent, PropType, ref, watch, onMounted } from "vue";
import { Course } from "../interfaces";
export default defineComponent({
    props: {
        course: {
            type: Object as PropType<Course>,
            require: true,
        },
    },
    setup(props) {
        const course = ref<Course>();
        onMounted(() => (course.value = props.course));
        watch(
            () => props.course,
            (newCourseData) => {
                course.value = newCourseData;
            },
        );
        return { course };
    },
});
</script>

<template>
    <div class="card">
        <div class="info">
            <h5>{{ course?.title }}</h5>
            <img :src="'/media/default.jpg'" class="course-img" />
        </div>
        <div class="course-pay">
            <div>{{ course?.price }} &#8381;</div>
        </div>
    </div>
</template>

<style scoped>
.card {
    border: 1px black solid;
    margin: 10px;
    height: 20vh;
    max-width: 250px;
    min-width: 150px;
    cursor: pointer;
}
.course-pay {
    display: flex;
    align-items: center;
}

.info {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.course-img {
    width: 50%;
}
</style>
