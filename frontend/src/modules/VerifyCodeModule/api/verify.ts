import Cookies from "js-cookie";

export default async function verify(verifyCode: string) {
  const response: Response = await fetch("/v1/auth/code", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${Cookies.get("access")}`,
    },
    body: JSON.stringify({
      code: verifyCode,
    }),
  });

  if (!response.ok) {
    throw new Error("Неверный код");
  }
}
