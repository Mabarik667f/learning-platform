import Cookies from "js-cookie";
import { Tokens } from "@/modules/LoginModule";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

export default async function fetchApiV1(
  endpoint: string,
  options: {
    method: string;
    headers?: object;
    body?: any;
  },
): Promise<Response> {
  try {
    const response = await fetch(`v1/${endpoint}`, {
      method: options.method,
      headers: {
        ...options.headers,
      },
      body: options.body,
    });

    if (response.status === 401) {
      await refresh_token();
      const response = await fetch(`v1/${endpoint}`, {
        method: options.method,
        headers: {
          ...options.headers,
        },
        body: options.body,
      });
      return response;
    }

    return response;
  } catch (error) {
    throw error;
  }
}

async function refresh_token() {
  const access: string | undefined = Cookies.get("access");
  const refresh: string | undefined = Cookies.get("refresh");
  const tokens = ref<Tokens>({
    refresh_token: "",
    access_token: "",
  });

  const response = await fetch("v1/auth/token/refresh", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${access}`,
    },
    body: JSON.stringify({ refresh_token: refresh }),
  });

  const data = await response.json();

  if (response.ok) {
    tokens.value = data;
  } else {
    router.push("login");
  }
}
