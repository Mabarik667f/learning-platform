<script lang="ts">
import { defineComponent, ref } from "vue";
import register from "../api/register";

import RegisterButton from "./RegisterButton.vue";
import { RegisterFormInterface } from "../interfaces/RegisterForm.ts";
import { RegFormValidator } from "../helpers/formValidation";

import { ErrorsType } from "@/interfaces/errorsInterfaces";

import errorsIsEmpty from "@/helpers/errorsIsEmpty";
import { useRouter } from "vue-router";

export default defineComponent({
    name: "reg-form",
    components: {
        RegisterButton,
    },
    setup() {
        const router = useRouter();

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
                    const serverErrors = await register(formData.value);
                    if (Array.isArray(serverErrors)) {
                        router.push("login");
                    } else {
                        Object.keys(serverErrors).forEach((key) => {
                            errors.value[key].push(serverErrors[key]);
                        });

                        formData.value.password = "";
                        formData.value.password2 = "";
                    }
                }
            } catch (error) {
                console.log(error);
            }
        };
        return { formData, errors, router, registerHook };
    },
});
</script>

<template>
    <c-form class="reg-form" @submit.prevent="registerHook">
        <template v-slot:header>
            <h1>Регистрация</h1>
        </template>
        <template v-slot:fields>
            <div class="wrapper">
                <div class="mb-4">
                    <cf-label :for="'username'" class="cf-label"
                        >Логин<span
                            class="error"
                            v-for="error in errors.username"
                        >
                            {{ error }}</span
                        ></cf-label
                    >
                    <c-input
                        :id="'username'"
                        :placeholder="'Логин'"
                        v-model="formData.username"
                        required
                    />
                </div>

                <div class="mb-4">
                    <cf-label :for="'email'"
                        >Email
                        <span class="error" v-for="error in errors.email">
                            {{ error }}</span
                        ></cf-label
                    >
                    <c-input
                        :id="'email'"
                        :type="'email'"
                        :placeholder="'Email'"
                        v-model="formData.email"
                        required
                    />
                </div>

                <div class="mb-4">
                    <cf-label :for="'password'">Пароль</cf-label>
                    <c-input
                        :id="'password'"
                        :type="'password'"
                        :placeholder="'Пароль'"
                        v-model="formData.password"
                        required
                    />
                </div>

                <div class="mb-5">
                    <cf-label :for="'password2'">Повтор пароля</cf-label>
                    <c-input
                        :id="'password2'"
                        :type="'password'"
                        :placeholder="'Повтор пароля'"
                        v-model="formData.password2"
                        required
                    />
                    <div class="pass-errors">
                        <span class="error" v-for="error in errors.password">
                            {{ error }}</span
                        >
                    </div>
                </div>
            </div>
        </template>
        <template v-slot:footer>
            <div class="footer">
                <RegisterButton />
                <p class="log-url">
                    Уже есть аккаунт? <a @click="router.push('login')">Войти</a>
                </p>
            </div>
        </template>
    </c-form>
</template>

<style scoped>
.reg-form {
    display: flex;
    flex-direction: column;
    background: inherit;
    border: 2px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(20px);
    color: #fff;
    width: 420px;
    height: 700px;
    padding: 30px 40px;
    border-radius: 10px;
}

.pass-errors {
    display: flex;
    flex-direction: column;
    text-align: left;
    margin-top: 5px;
    margin-left: 10px;
}
.wrapper {
    width: 100%;
}

.cf-label .error {
    display: block;
    margin-top: 5px;
    word-wrap: break-word;
    white-space: normal;
}

a {
    font-weight: bold;
}

a:hover {
    text-decoration: underline !important;
}

.log-url {
    margin-top: 5px;
}

.footer {
    display: flex;
    flex-grow: 1;
    flex-direction: column;
    justify-content: space-evenly;
}
</style>
