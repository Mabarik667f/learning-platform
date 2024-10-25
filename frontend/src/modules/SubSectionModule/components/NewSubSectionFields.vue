<script lang="ts">
import { defineComponent, PropType } from "vue";
import { SectionCreate } from "@/modules/SectionModule";
import { SubSectionCreate } from "../interfaces";
import { CreateCourseStruct } from "@/modules/CreateCourseStructModule";
export default defineComponent({
    props: {
        structObj: {
            type: CreateCourseStruct as PropType<CreateCourseStruct>,
            required: true,
        },
        sub: {
            type: Object as PropType<SubSectionCreate>,
            required: true,
        },
        sec: {
            type: Object as PropType<SectionCreate>,
            required: true,
        },
    },
    setup() {},
});
</script>
<template>
    <div>
        <c-input v-model="sub.title" required />
        <c-button
            :type="'button'"
            @click="structObj.delSubSection(sec.position - 1, sub.position - 1)"
            >Удалить</c-button
        >
    </div>
</template>
<style scoped></style>
