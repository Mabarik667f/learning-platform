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
    <button :type="type" class="btn">
        <slot> </slot>
    </button>
</template>
<style scoped></style>
