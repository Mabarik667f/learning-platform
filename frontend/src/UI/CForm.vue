<script lang="ts">
import { defineComponent, PropType } from "vue";

export default defineComponent({
    name: "c-form",
    props: {
        method: {
            default: "post",
            type: String as PropType<"post" | "get">,
        },
    },
});
</script>

<template>
    <form :method="method">
        <slot name="header"></slot>
        <slot name="fields"></slot>
        <slot name="buttons"></slot>
    </form>
</template>
<style scoped></style>
