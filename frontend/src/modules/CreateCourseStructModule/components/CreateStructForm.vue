<script lang="ts">
import { defineComponent, ref } from "vue";
import createCourseStruct from "../api/createCourseStruct";
import CreateStructBtn from "./CreateStructBtn.vue";
import CreateCourseStruct from "../helpers/courseStruct";
import { NewSectionFields } from "@/modules/SectionModule";
import { useRoute } from "vue-router";
export default defineComponent({
    components: {
        CreateStructBtn,
        NewSectionFields,
    },
    setup() {
        const route = useRoute();
        const courseId = ref<number>(parseInt(route.params.id as string));
        const structObj = new CreateCourseStruct();

        const struct = structObj.struct;
        const handleSubmit = async () => {
            if (struct.value) {
                await createCourseStruct(struct.value, courseId.value);
            }
        };
        return { struct, structObj, handleSubmit, courseId };
    },
});
</script>
<template>
    <c-form :method="'post'" @submit.prevent="handleSubmit">
        <template v-slot:header>
            {{ struct }}
            <h2>Создание разделов</h2>
        </template>
        <template v-slot:fields>
            <div v-for="sec in struct?.sections" :key="sec.position">
                <NewSectionFields :sec="sec" :structObj="structObj" />
            </div>
            <c-button :type="'button'" @click="structObj.addSection()"
                >Новая секция</c-button
            >
        </template>
        <template v-slot:footer>
            <CreateStructBtn />
        </template>
    </c-form>
</template>
<style scoped></style>
