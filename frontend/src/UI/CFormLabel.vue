<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
    name: "cf-label",
});
</script>

<template>
    <label class="form-label lb"><slot></slot></label>
</template>

<style scoped>
.lb {
    display: block;
    text-align: left;
    margin-left: 10px;
}
</style>
