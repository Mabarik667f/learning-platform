import { UserLogin } from "../interfaces/UserLogin";

export default async function login(formData: UserLogin) {
  const bodyData = new URLSearchParams();
  const params = Object.keys(formData);

  params.forEach((param) => {
    bodyData.append(param, formData[param as keyof UserLogin]);
  });

  bodyData.append("grant_type", "password");
  bodyData.append("scope", "me");

  const response: Response = await fetch("/v1/auth/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: bodyData.toString(),
  });
  const res = await response.json();
  if (response.ok) {
    return { data: res, errors: [] };
  } else {
    return { data: "", errors: res.detail };
  }
}
