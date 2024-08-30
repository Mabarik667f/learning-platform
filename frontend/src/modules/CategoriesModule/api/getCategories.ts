import fetchApiV1 from "@/api";
import Cookies from "js-cookie";
import { Category } from "@modules/CategoriesModule";

const access: string | undefined = Cookies.get("access");

export default async function getCategories(): Promise<Category[]> {
  const options = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${access}`,
    },
  };
  try {
    const response: Response = await fetchApiV1("categories/list", options);

    const data = await response.json();

    if (response.ok) {
      return data as Category[];
    } else {
      throw new Error("ERROR loading categories");
    }
  } catch (error) {
    console.log(error);
    return [];
  }
}
