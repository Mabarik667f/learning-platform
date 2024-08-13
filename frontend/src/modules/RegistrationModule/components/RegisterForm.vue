<script lang="ts">
import { defineComponent, ref } from "vue";
import register from "../api/register";

import RegisterButton from "./RegisterButton.vue";
import { RegisterFormInterface } from "../interfaces/RegisterForm.ts";
import { RegFormValidator } from "../helpers/formValidation";

import { User, Role } from "@/interfaces/userInterfaces";
import { ErrorsType } from "@/interfaces/errorsInterfaces";

import errorsIsEmpty from "@/helpers/errorsIsEmpty";

export default defineComponent({
    name: "reg-form",
    components: {
        RegisterButton,
    },
    setup() {
        const registerData = ref<User>({
            username: "",
            email: "",
            role: Role.Default,
        });

        const errors = ref<ErrorsType>({
            username: [],
            password: [],
            email: [],
        });

        const formData = ref<RegisterFormInterface>({
            username: "",
            email: "",
            password: "",
            password2: "",
        });

        const registerHook = async () => {
            try {
                const validator = new RegFormValidator(formData.value);
                errors.value = validator.formValidation();
                if (errorsIsEmpty(errors.value)) {
                    registerData.value,
                        (errors.value = await register(formData.value));
                }
                if (errorsIsEmpty(errors.value)) {
                    // redirect to login page
                } else {
                    formData.value.password = "";
                    formData.value.password2 = "";
                    console.log(errors.value);
                }
            } catch (error) {
                console.log(error);
            }
        };
        return { formData, registerHook };
    },
});
</script>

<template>
    <c-form class="reg-form" @submit.prevent="registerHook">
        <template v-slot:header> </template>
        <template v-slot:fields>
            <div class="fields">
                <label :for="'username'">Логин</label>
                <c-input
                    :id="'username'"
                    v-model="formData.username"
                    required
                />

                <label :for="'email'">Email</label>
                <c-input
                    :id="'email'"
                    :type="'email'"
                    v-model="formData.email"
                    required
                />

                <label :for="'password'">Пароль</label>
                <c-input
                    :id="'password'"
                    :type="'password'"
                    v-model="formData.password"
                    required
                />

                <label :for="'password2'">Повтор пароля</label>
                <c-input
                    :id="'password2'"
                    :type="'password'"
                    v-model="formData.password2"
                    required
                />
            </div>
        </template>
        <template v-slot:buttons>
            <div class="buttons">
                <RegisterButton />
            </div>
        </template>
    </c-form>
</template>

<style scoped>
.reg-form {
    display: grid;
    border: 1px black solid;
    margin: auto;
}
</style>
