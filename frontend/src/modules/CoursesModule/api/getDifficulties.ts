import fetchApiV1 from "@/api";
import { FilterOption } from "@/modules/FiltersModule/interfaces/FilterOption";

export default async function getDifficulties(): Promise<FilterOption[]> {
  const options = {
    method: "GET",
    headers: {
      "Content-Type": "application-json",
    },
  };
  const response: Response = await fetchApiV1(
    "courses/all-difficulties",
    options,
  );

  const data = await response.json();

  try {
    return data as FilterOption[];
  } catch (error) {
    return [];
    console.log(error);
  }
}
