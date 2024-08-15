<script setup lang="ts"></script>

<template>
    <router-view />
    <div></div>
</template>

<style>
.logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
}

a {
    cursor: pointer;
    text-decoration: none;
    color: inherit;
}

a:hover {
    color: inherit;
    text-decoration: underline;
}

.logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
    filter: drop-shadow(0 0 2em #42b883aa);
}

.auth-input {
    border-radius: 40px;
}
</style>
