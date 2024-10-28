<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
    name: "del-btn",
});
</script>
<template>
    <c-button :type="'button'">&#x2717</c-button>
</template>
<style scoped>
button {
    margin-top: 15px;
    width: 50px !important;
    background-color: red !important;
    color: white !important;
    border-radius: 8px !important;
}
</style>
