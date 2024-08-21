import fetchApiV1 from "@/api";
import { RegisterFormInterface } from "../interfaces/RegisterForm";

export default async function register(formData: RegisterFormInterface) {
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ...formData }),
  };

  const response: Response = await fetchApiV1("users/create-user", options);

  const result = await response.json();
  if (response.ok) {
    return [];
  } else {
    return result.detail;
  }
}
