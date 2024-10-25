import fetchApiV1 from "@/api";
import { CourseStruct } from "../interfaces";
import Cookies from "js-cookie";

export default async function createCourseStruct(
  struct: CourseStruct,
  courseId: number,
) {
  const options = {
    method: "POST",
    headers: {
      "Content-type": "application/json",
      Authorization: `Bearer ${Cookies.get("access")}`,
    },
    body: {
      sections: struct.sections,
    },
  };
  const response: Response = await fetchApiV1(
    `courses/struct/${courseId}`,
    options,
  );

  const data = await response.json();
  console.log(data);
}
