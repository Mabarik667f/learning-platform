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
    <div class="sec">
        <div class="sec-inp">
            <div class="mb-3">
                <cf-label :for="sec.position">Название</cf-label>
                <c-input v-model="sec.title" :id="sec.position" required />
            </div>
            <div class="mb-3">
                <cf-label :for="sec.position">Описание</cf-label>
                <c-text v-model="sec.describe" :id="sec.position" />
            </div>
        </div>
        <div class="sec-opts">
            <del-btn @click="structObj.delSection(sec.position - 1)" />
            <c-button
                :type="'button'"
                @click="structObj.addSubSection(sec.position - 1)"
                >Новая подсекция</c-button
            >
        </div>

        <div class="subs">
            <div v-for="sub in sec.subsections" :key="sub.position">
                <NewSubSectionFields
                    :sec="sec"
                    :structObj="structObj"
                    :sub="sub"
                />
            </div>
        </div>
    </div>
</template>
<style scoped>
.sec {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 10px;
    flex-wrap: wrap;
}
.sec-inp,
.sec-opts {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 50%;
}

.subs {
    width: 100%;
    display: flex;
    flex-direction: row;
}

.subs div {
    margin: 10px;
}
</style>
