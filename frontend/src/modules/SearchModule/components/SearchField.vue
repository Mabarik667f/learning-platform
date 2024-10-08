<script lang="ts">
import { defineComponent, SetupContext } from "vue";
import SearchButton from "./SearchButton.vue";
import SearchInput from "./SearchInput.vue";
export default defineComponent({
    components: {
        SearchInput,
        SearchButton,
    },
    emits: ["getSearchQuery"],
    setup(_, { emit }: SetupContext) {
        const getSearchQuery = (query: string) => {
            emit("getSearchQuery", query);
        };
        return { getSearchQuery };
    },
});
</script>

<template>
    <div class="search">
        <SearchInput @search="getSearchQuery" />
        <SearchButton />
    </div>
</template>

<style scoped>
.search {
    display: flex;
    align-items: center;
    align-self: flex-start;
    position: relative;
    height: 7vh;
    padding: 5px;
    width: 100%;
    margin: auto;
}

.search::after {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    background: #6d8a51;
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    z-index: -1;
    border-radius: 20px;
}
</style>
