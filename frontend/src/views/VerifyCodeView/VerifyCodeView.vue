<script lang="ts">
import { VerifyForm } from "@/modules/VerifyCodeModule";
import { defineComponent } from "vue";

export default defineComponent({
    components: {
        VerifyForm,
    },
    setup() {
        return {};
    },
});
</script>

<template>
    <VerifyForm></VerifyForm>
</template>

<style scroped></style>
