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
        <div class="mb-3">
            <cf-label :for="sub.position">Название</cf-label>
            <c-input v-model="sub.title" required :id="sub.position" />
        </div>
        <del-btn
            @click="structObj.delSubSection(sec.position - 1, sub.position - 1)"
        />
    </div>
</template>
<style scoped></style>
