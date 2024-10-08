import { defineStore } from "pinia";
import { ref } from "vue";
import { FilterOption } from "@modules/FiltersModule";
import getCategories from "./api/getCategories";

export const useCategoryStore = defineStore("category", () => {
  const categorySearchQuery = ref<string>("");
  const categories = ref<FilterOption[]>([]);
  const defaultCategoriesValue = ref<FilterOption[]>([]);

  const setCategoryQuery = (query: string) => {
    categorySearchQuery.value = query;
  };

  const fetchCategories = async () => {
    categories.value = await getCategories();
    defaultCategoriesValue.value = categories.value;
  };

  const filterCategories = () => {
    categories.value = defaultCategoriesValue.value.filter((cat) =>
      cat.title
        .toLowerCase()
        .startsWith(categorySearchQuery.value.toLowerCase()),
    );
  };

  return {
    categories,
    categorySearchQuery,
    setCategoryQuery,
    fetchCategories,
    filterCategories,
  };
});
