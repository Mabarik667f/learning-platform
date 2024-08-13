import { defineStore } from "pinia";
import { ref } from "vue";
import Cookies from "js-cookie";

export const authStore = defineStore("auth", () => {
  const isAuth = ref<boolean>(false);

  async function setIsAuth(flag: boolean) {
    isAuth.value = flag;
    Cookies.set("isAuth", flag.toString());
  }

  async function getCookieAuth() {
    isAuth.value = Cookies.get("isAuth") === "true";
  }

  async function setToken(token: string) {
    Cookies.set("access", token);
  }

  return { isAuth, setIsAuth, getCookieAuth, setToken };
});
