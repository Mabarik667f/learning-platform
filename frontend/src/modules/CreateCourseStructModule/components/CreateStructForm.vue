<script lang="ts">
import { defineComponent, ref } from "vue";
import CreateStructBtn from "./CreateStructBtn.vue";
import { CourseStruct } from "../interfaces";
export default defineComponent({
    components: {
        CreateStructBtn,
    },
    setup() {
        const struct = ref<CourseStruct>();
        return { struct };
    },
});
</script>
<template>
    <c-form :method="'post'">
        <template v-slot:header>
            <h2>Создание разделов</h2>
        </template>
        <template v-slot:fields> </template>
        <template v-slot:footer>
            <CreateStructBtn />
        </template>
    </c-form>
</template>
<style scoped></style>
