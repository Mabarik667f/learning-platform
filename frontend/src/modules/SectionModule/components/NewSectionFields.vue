<script lang="ts">
import { defineComponent, PropType } from "vue";
import { SectionCreate } from "../interfaces";
import { CreateCourseStruct } from "@/modules/CreateCourseStructModule";
import { NewSubSectionFields } from "@/modules/SubSectionModule";
export default defineComponent({
    components: {
        NewSubSectionFields,
    },
    props: {
        structObj: {
            type: CreateCourseStruct as PropType<CreateCourseStruct>,
            required: true,
        },
        sec: {
            type: Object as PropType<SectionCreate>,
            required: true,
        },
    },
});
</script>
<template>
    <div>
        <c-input v-model="sec.describe" required />
        <c-input v-model="sec.title" required />
        <c-button
            :type="'button'"
            @click="structObj.addSubSection(sec.position - 1)"
            >Новая подсекция</c-button
        >
        <div v-for="sub in sec.subsections" :key="sub.position">
            <NewSubSectionFields :sec="sec" :structObj="structObj" :sub="sub" />
        </div>
        <c-button
            :type="'button'"
            @click="structObj.delSection(sec.position - 1)"
            >Удалить</c-button
        >
    </div>
</template>
<style scoped></style>
