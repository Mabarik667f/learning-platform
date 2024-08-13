<script lang="ts">
import { defineComponent, ref } from "vue";
import { UserLogin } from "../interfaces/UserLogin";
import LoginButton from "./LoginButton.vue";
import { ErrorsType } from "@/interfaces/errorsInterfaces";
import login from "../api/login";
import errorsIsEmpty from "@/helpers/errorsIsEmpty";
import { authStore } from "@/store/authStore";
import { useRouter } from "vue-router";

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
        return { formData, errors, loginHook };
    },
    components: { LoginButton },
});
</script>

<template>
    <c-form :method="'post'" @submit.prevent="loginHook">
        <template v-slot:header> </template>
        <template v-slot:fields>
            <div>
                <label :for="'username'">Логин</label>
                <c-input
                    v-model="formData.username"
                    :id="'username'"
                    required
                />
                <label :for="'password'">Пароль</label>
                <c-input
                    :id="'password'"
                    :type="'password'"
                    v-model="formData.password"
                    required
                />
            </div>
        </template>
        <template v-slot:buttons>
            <LoginButton />
        </template>
    </c-form>
</template>

<style scoped></style>
