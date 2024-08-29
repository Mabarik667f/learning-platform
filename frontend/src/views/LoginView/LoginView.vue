<script lang="ts">
import { LoginForm } from "@/modules/LoginModule";
import { defineComponent } from "vue";

export default defineComponent({
    components: { LoginForm },
    setup() {
        return {};
    },
});
</script>

<template>
    <div class="con">
        <LoginForm></LoginForm>
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
