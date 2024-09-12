import fetchApiV1 from "@/api";
import { ref } from "vue";

export default async function getCourseList(
  queryParams?: string,
  offset?: number,
  limit?: number,
) {
  const options = {
    method: "GET",
    headers: {
      "Content-Type": "application-json",
    },
  };

  const endpoint = ref<string>("courses/list");
  if (queryParams) {
    endpoint.value = endpoint.value + queryParams;
  }
  const response: Response = await fetchApiV1(endpoint.value, options);

  try {
    // create Interface +
    const data = await response.json();
    return data;
  } catch (error) {
    console.log(error);
    return [];
  }
}
