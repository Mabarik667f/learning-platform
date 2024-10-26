<script lang="ts">
import { defineComponent, PropType } from "vue";
export default defineComponent({
    name: "c-file",
    props: {
        placeholder: {
            default: "",
            type: String as PropType<string>,
        },
        id: {
            type: String as PropType<string>,
        },
    },
});
</script>

<template>
    <input type="file" :id="id" :placeholder="placeholder" class="inp" />
</template>

<style scroped>
.inp {
    width: 100%;
    height: 100%;
    background: transparent;
    color: inherit;
    border: none;
    outline: none;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 40px;
    color: inherit;
    padding: 10px 35px 10px 20px;
}

.inp::placeholder {
    color: inherit;
    font-weight: bold;
}
</style>
