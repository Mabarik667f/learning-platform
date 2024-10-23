import fetchApiV1 from "@/api";
import { CourseCreate } from "../interfaces";
import Cookies from "js-cookie";
import convertToFormData from "@/helpers/convertToFormData";

export default async function createCourse(course: CourseCreate) {
  const formData = convertToFormData(course);
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
    console.log("SUCCESS");
  }
  console.log(data);
}
