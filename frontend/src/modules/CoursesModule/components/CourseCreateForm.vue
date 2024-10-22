<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { CourseCreate } from "../interfaces";
import { Difficulty, MultiselectOption } from "@/interfaces/objectsInterfaces";
import Multiselect from "@vueform/multiselect";
import createCourse from "../api/createCourse";
import getDifficulties from "../api/getDifficulties";
import setCatsForMultiselect from "../helpers/setCatsForMultiselect";
export default defineComponent({
    components: {
        Multiselect,
    },
    setup() {
        const course = ref<CourseCreate>({
            title: "",
            describe: "",
            price: 0,
            img: null,
            difficulty: "",
            categories: [],
        });
        const handleCreateCourse = async () => {
            await createCourse(course.value);
        };

        const difficulties = ref<Difficulty[]>([]);
        const categories = ref<MultiselectOption[]>([]);
        onMounted(async () => {
            difficulties.value = await getDifficulties();
            categories.value = await setCatsForMultiselect();
        });

        const handleImageChange = (event: Event) => {
            course.value.img =
                (event.target as HTMLInputElement).files?.[0] || null;
        };
        return {
            course,
            handleCreateCourse,
            handleImageChange,
            difficulties,
            categories,
        };
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
                <c-file @change="handleImageChange" />
            </div>
            <div class="mb-3">
                <c-text v-model="course.describe" />
            </div>
            <div class="mb-3">
                <c-select v-model="course.difficulty" :options="difficulties" />
            </div>
            <div class="mb-3">
                <Multiselect
                    v-model="course.categories"
                    :options="categories"
                    mode="multiple"
                />
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
