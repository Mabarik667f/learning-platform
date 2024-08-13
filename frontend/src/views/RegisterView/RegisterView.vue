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
    <div class="register">
        <RegisterForm />
    </div>
</template>

<style scroped></style>
