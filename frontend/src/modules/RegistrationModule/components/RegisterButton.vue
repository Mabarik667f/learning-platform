<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
    name: "reg-btn",
    setup() {
        return {};
    },
});
</script>

<template>
    <c-button class="reg-btn btn-primary">Зарегистрироваться</c-button>
</template>

<style scoped>
.reg-btn {
    width: 100%;
}
</style>
