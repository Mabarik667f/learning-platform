import { defineStore } from "pinia";
import { ref } from "vue";
import { Course } from "./interfaces";
import getCourseList from "./api/getCourseList";

export const useCourseStore = defineStore("course", () => {
  const courses = ref<Array<Course>>([]);
  const defaultCourses = ref<Array<Course>>([]);

  const courseSearchQuery = ref<string>("");

  const setCourseQuery = (query: string) => {
    courseSearchQuery.value = query;
  };

  const fetchCourses = async (query: string) => {
    courses.value = await getCourseList(query);
    defaultCourses.value = courses.value;
  };

  const filterCourses = () => {
    courses.value = defaultCourses.value.filter((c) =>
      c.title.toLowerCase().startsWith(courseSearchQuery.value.toLowerCase()),
    );
  };

  return {
    courses,
    courseSearchQuery,
    setCourseQuery,
    fetchCourses,
    filterCourses,
  };
});
