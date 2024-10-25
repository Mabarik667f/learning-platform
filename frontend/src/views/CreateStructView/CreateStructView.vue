<script lang="ts">
import { defineComponent } from "vue";
import { CreateStructForm } from "@/modules/CreateCourseStructModule";
export default defineComponent({
    components: {
        CreateStructForm,
    },
});
</script>
<template>
    <div class="con">
        <CreateStructForm />
    </div>
</template>
<style scoped></style>
