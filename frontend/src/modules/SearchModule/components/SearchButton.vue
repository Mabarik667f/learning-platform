<script lang="ts">
import { defineComponent } from "vue";
import searchIcon from "@/assets/icons/search.svg";
export default defineComponent({
    setup() {
        return { searchIcon };
    },
});
</script>

<template>
    <c-button class="search-btn">
        <img :src="searchIcon" />
    </c-button>
</template>

<style scoped>
.search-btn {
    width: 30% !important;
    height: 100% !important;
    border: none !important;
    box-shadow: none !important;
    background-color: inherit !important;
    transition: box-shadow 0.3s ease;
    border-radius: 10px;
    margin-left: 1px;
}

.search-btn:hover {
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3) !important;
}

.search-btn img {
    width: 100%;
    height: 80%;
}
</style>
