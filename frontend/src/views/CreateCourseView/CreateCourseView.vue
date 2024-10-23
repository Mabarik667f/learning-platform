<script lang="ts">
import { defineComponent, ref } from "vue";
import { CreateCourseForm } from "@/modules/CoursesModule";
export default defineComponent({
    setup() {},
    components: {
        CreateCourseForm,
    },
});
</script>

<template>
    <div class="con">
        <CreateCourseForm />
    </div>
</template>

<style scoped>
.con {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}
</style>
