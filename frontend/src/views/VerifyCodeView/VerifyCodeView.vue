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
    <div class="con">
        <VerifyForm></VerifyForm>
    </div>
</template>

<style scroped>
.con {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
}
</style>
