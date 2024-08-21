import fetchApiV1 from "@/api";
import Cookies from "js-cookie";

export default async function verify(verifyCode: string) {
  const options = {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${Cookies.get("access")}`,
    },
    body: JSON.stringify({ code: verifyCode }),
  };
  const response = await fetchApiV1("auth/code", options);

  if (!response.ok) {
    throw new Error("Неверный код");
  }
}
