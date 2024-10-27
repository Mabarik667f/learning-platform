import fetchApiV1 from "@/api";
import { CourseCreate, CourseResponse } from "../interfaces";
import Cookies from "js-cookie";
import convertToFormData from "@/helpers/convertToFormData";

export default async function createCourse(
  course: CourseCreate,
): Promise<CourseResponse> {
  const formData = convertToFormData(course);
  // @ts-ignore
  formData.set("categories", course.categories);
  const options = {
    method: "POST",
    headers: {
      Authorization: `Bearer ${Cookies.get("access")}`,
    },
    body: formData,
  };
  const response = await fetchApiV1("courses/create", options);

  const data = await response.json();
  if (response.ok) {
    return data;
  } else {
    throw new Error(data.detail);
  }
}
