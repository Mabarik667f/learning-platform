<script lang="ts">
import { defineComponent } from "vue";
import CreateStructBtn from "./CreateStructBtn.vue";
import CreateCourseStruct from "../helpers/courseStruct";
import { NewSectionFields } from "@/modules/SectionModule";
export default defineComponent({
    components: {
        CreateStructBtn,
        NewSectionFields,
    },
    setup() {
        const structObj = new CreateCourseStruct();

        const handleSubmit = async () => {
            console.log(1);
        };
        const struct = structObj.struct;
        return { struct, structObj, handleSubmit };
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
