<script lang="ts">
import { defineComponent, ref } from "vue";
import VerifyButton from "./VerifyButton.vue";
import verify from "../api/verify";
import { authStore } from "@/store/authStore";
import { useRouter } from "vue-router";

export default defineComponent({
    components: { VerifyButton },
    setup() {
        const code = ref<string>("");
        const error = ref<string>("");

        const router = useRouter();
        const store = authStore();

        const { setIsAuth } = store;

        const verifyHook = async () => {
            try {
                await verify(code.value);
                setIsAuth(true);
                router.push("/");
            } catch (e) {
                console.log(e);
                error.value = "Неверный код доступа!";
                code.value = "";
            }
        };
        return { code, error, verifyHook };
    },
});
</script>

<template>
    <c-form :method="'post'" @submit.prevent="verifyHook" class="ver-form">
        <template v-slot:header>
            <div class="mb-5">
                <h1>Вход</h1>
                <p>
                    6-ти значный Код придет на почту, указанную при регистрации
                </p>
                <span class="error">{{ error }}</span>
            </div>
        </template>
        <template v-slot:fields>
            <div class="mb-4">
                <c-input
                    class="code"
                    maxlength="6"
                    :placeholder="'123456'"
                    pattern="\d{6}"
                    v-model="code"
                    required
                />
            </div>
        </template>
        <template v-slot:footer>
            <VerifyButton />
        </template>
    </c-form>
</template>

<style scoped>
.ver-form {
    display: flex;
    color: #fff;
    flex-direction: column;
    background: inherit;
    padding: 30px 40px;
    width: 420px;
    height: 400px;
    border-radius: 10px;
    backdrop-filter: blur(20px);
    border: 2px solid rgba(255, 255, 255, 0.2);
}

.code {
    text-align: center;
}
</style>
