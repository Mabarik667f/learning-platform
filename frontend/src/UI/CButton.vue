<script lang="ts">
import { defineComponent, PropType } from "vue";

export default defineComponent({
    name: "c-button",
    props: {
        type: {
            default: "submit",
            type: String as PropType<"submit" | "button" | "reset">,
        },
    },
});
</script>

<template>
    <button :type="type" class="c-btn">
        <slot> </slot>
    </button>
</template>
<style scoped>
.c-btn {
    width: 100%;
    height: 45px;
    background: #fff;
    border: none;
    outline: none;
    border-radius: 40px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    font-size: 16px;
    color: #333;
    font-weight: 600;
}
</style>
