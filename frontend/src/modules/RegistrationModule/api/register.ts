import { RegisterFormInterface } from "../interfaces/RegisterForm";

export default async function register(formData: RegisterFormInterface) {
  const response: Response = await fetch("/v1/users/create-user", {
    method: "POST",
    body: JSON.stringify({
      ...formData,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });

  const result = await response.json();
  if (response.ok) {
    return [];
  } else {
    return result.detail;
  }
}
