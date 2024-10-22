<script lang="ts">
import { defineComponent, ref } from "vue";
import { CourseCreate } from "../interfaces";
import createCourse from "../api/createCourse";
export default defineComponent({
    setup() {
        const course = ref<CourseCreate>({
            title: "abab",
            describe: "bab",
            price: 100,
            img: null,
            difficulty: "easy",
            categories: [6],
        });
        const handleCreateCourse = async () => {
            await createCourse(course.value);
        };

        const handleImageChange = (event: Event) => {
            course.value.img =
                (event.target as HTMLInputElement).files?.[0] || null;
        };
        return { course, handleCreateCourse, handleImageChange };
    },
});
</script>

<template>
    <c-form
        method="post"
        @submit.prevent="handleCreateCourse"
        class="create-form"
    >
        <template v-slot:header>
            <h2>Создать Курс</h2>
        </template>
        <template v-slot:fields>
            <div class="mb-3">
                <c-input v-model="course.title" />
            </div>
            <div class="mb-3">
                <c-input v-model="course.price" :type="'number'" />
            </div>
            <div class="mb-3">
                <c-input @change="handleImageChange" :type="'file'" />
            </div>
            <div class="mb-3">
                <c-text v-model="course.describe" />
            </div>
            <!-- select difficulty, select categories-->
        </template>
        <template v-slot:footer>
            <c-button>Создать</c-button>
        </template>
    </c-form>
</template>

<style scoped>
* {
    background: blue;
}
.create-form {
    padding: 30px 40px;
    border-radius: 20px;
    max-width: 600px;
    height: 100%;
}
</style>
