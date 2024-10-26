<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { CourseCreate, CourseResponse } from "../interfaces";
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
        const router = useRouter();
        const course = ref<CourseCreate>({
            title: "",
            describe: "",
            price: 0,
            img: null,
            difficulty: "",
            categories: [],
        });
        const handleCreateCourse = async () => {
            const courseObj: CourseResponse = await createCourse(course.value);
            router.push({ name: "struct", params: { id: courseObj.id } });
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
        :method="'post'"
        @submit.prevent="handleCreateCourse"
        class="create-form"
    >
        <template v-slot:header>
            <h2>Создать Курс</h2>
        </template>
        <template v-slot:fields>
            <div class="mb-3">
                <cf-label :for="'title'">Название</cf-label>
                <c-input v-model="course.title" :id="'title'" required />
            </div>
            <div class="mb-3">
                <cf-label :for="'price'">Цена</cf-label>
                <c-input
                    v-model="course.price"
                    :type="'number'"
                    :id="'price'"
                    required
                />
            </div>
            <div class="mb-3">
                <cf-label :for="'img'">Изображение</cf-label>
                <c-file @change="handleImageChange" :id="'img'" required />
            </div>
            <div class="mb-3">
                <cf-label :for="'difficulty'">Сложность</cf-label>
                <c-select
                    v-model="course.difficulty"
                    :options="difficulties"
                    :id="'difficulty'"
                    class="form-select"
                    required
                />
            </div>
            <div class="mb-3">
                <cf-label :for="'cats'">Категории</cf-label>
                <Multiselect
                    v-model="course.categories"
                    :options="categories"
                    mode="multiple"
                    class="fm-select"
                    :id="'cats'"
                    required
                />
            </div>
            <div class="mb-3">
                <cf-label :for="'describe'">Описание</cf-label>
                <c-text v-model="course.describe" :id="'describe'" />
            </div>
        </template>
        <template v-slot:footer>
            <c-button class="create-btn">Создать</c-button>
        </template>
    </c-form>
</template>

<style scoped>
h2 {
    margin-bottom: 20px;
}
.create-form {
    color: #fff;
    backdrop-filter: blur(20px);
    padding: 30px 40px;
    border-radius: 20px;
    width: 500px;
    max-width: 500px;
    height: 100%;
}
.create-btn {
    width: 200px !important;
    margin-top: 20px;
}

.fm-select,
.form-select {
    border-radius: 40px;
    height: 40px;
    cursor: pointer;
    color: black;
}

#describe {
    max-height: 400px !important;
}
</style>
