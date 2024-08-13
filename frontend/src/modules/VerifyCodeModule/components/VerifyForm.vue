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

        const router = useRouter();
        const store = authStore();
        const { setIsAuth } = store;

        const verifyHook = async () => {
            try {
                await verify(code.value);
                setIsAuth(true);
                router.push("/");
            } catch (error) {
                console.log(error);
                code.value = "";
            }
        };
        return { code, verifyHook };
    },
});
</script>

<template>
    <c-form :method="'post'" @submit.prevent="verifyHook">
        <template v-slot:header> </template>
        <template v-slot:fields>
            <div>
                <c-input v-model="code" required />
            </div>
        </template>
        <template v-slot:buttons>
            <VerifyButton />
        </template>
    </c-form>
</template>

<style scoped></style>
