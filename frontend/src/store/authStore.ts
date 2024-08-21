import { defineStore } from "pinia";
import { ref } from "vue";
import Cookies from "js-cookie";
import { Tokens } from "@/modules/LoginModule";

export const authStore = defineStore("auth", () => {
  const isAuth = ref<boolean>(false);

  async function setIsAuth(flag: boolean) {
    isAuth.value = flag;
    Cookies.set("isAuth", flag.toString());
  }

  async function getCookieAuth() {
    isAuth.value = Cookies.get("isAuth") === "true";
  }

  async function setTokens(tokens: Tokens) {
    Cookies.set("access", tokens.access_token);
    Cookies.set("refresh", tokens.refresh_token);
  }

  async function clearCookies() {
    const allCookies = Cookies.get();

    for (const cookieName in allCookies) {
      if (allCookies.hasOwnProperty(cookieName)) {
        Cookies.remove(cookieName);
      }
    }
  }

  return { isAuth, setIsAuth, getCookieAuth, setTokens, clearCookies };
});
