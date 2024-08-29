<script lang="ts">
import { defineComponent } from "vue";
import { RegisterForm } from "@modules/RegistrationModule";

export default defineComponent({
    components: {
        RegisterForm,
    },
});
</script>

<template>
    <div class="con">
        <RegisterForm />
    </div>
</template>

<style scroped>
.con {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
}
</style>
