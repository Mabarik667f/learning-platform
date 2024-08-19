<script lang="ts">
import { useRouter } from "vue-router";
import { defineComponent, ref } from "vue";
import { authStore } from "@/store/authStore";

import errorsIsEmpty from "@/helpers/errorsIsEmpty";
import login from "../api/login";

import { UserLogin } from "../interfaces/UserLogin";
import { ErrorsType } from "@/interfaces/errorsInterfaces";

import LoginButton from "./LoginButton.vue";

export default defineComponent({
    setup() {
        const router = useRouter();
        const store = authStore();
        const { setToken } = store;

        const formData = ref<UserLogin>({
            username: "",
            password: "",
        });

        const errors = ref<ErrorsType>({
            username: [],
            password: [],
        });

        const accessToken = ref<string>("");
        const loginHook = async () => {
            const result = await login(formData.value);
            errors.value = result.errors;
            accessToken.value = result.data.access_token;

            if (errorsIsEmpty(errors.value)) {
                setToken(accessToken.value);
                router.push("verify-code");
            } else {
                formData.value.password = "";
            }
        };
        return { formData, errors, loginHook, router };
    },
    components: { LoginButton },
});
</script>

<template>
    <c-form method="post" @submit.prevent="loginHook" class="log-form">
        <template v-slot:header>
            <h1>Войти</h1>
        </template>
        <template v-slot:fields>
            <div class="wrapper">
                <div class="mb-3">
                    <cf-label :for="'username'"
                        >Логин
                        <span class="error" v-for="error in errors.username">
                            {{ error }}</span
                        >
                    </cf-label>
                    <c-input
                        v-model="formData.username"
                        :id="'username'"
                        :placeholder="'Логин'"
                        class="auth-input"
                        required
                    />
                </div>

                <div class="mb-4">
                    <cf-label :for="'password'"
                        >Пароль
                        <span class="error" v-for="error in errors.password">
                            {{ error }}</span
                        >
                    </cf-label>
                    <c-input
                        :id="'password'"
                        :type="'password'"
                        :placeholder="'Пароль'"
                        class="auth-input"
                        v-model="formData.password"
                        required
                    />
                </div>
            </div>
        </template>
        <template v-slot:footer>
            <LoginButton class="mb-3" />
            <div class="mb-3">
                <p>
                    Нет аккаунта?
                    <a @click="router.push('register')">Зарегистрироваться</a>
                </p>
            </div>
        </template>
    </c-form>
</template>

<style scoped>
.log-form {
    width: 420px;
    height: 420px;
    background: inherit;
    border: 2px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(20px);
    padding: 30px 40px;
    border-radius: 10px;
    color: #fff;
}

.wrapper {
    width: 100%;
}

.auth-input {
    border-radius: 40px;
}

a {
    font-weight: bold;
}

a:hover {
    text-decoration: underline !important;
}
</style>
