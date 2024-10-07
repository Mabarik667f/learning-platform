import { Ref } from "vue";
import { FilterOption } from "../interfaces";

export const selectOption = async (
  selectedOptions: Ref<FilterOption[]>,
  option: FilterOption,
) => {
  selectedOptions.value.push(option);
};

export const unSelectOption = async (
  selectedOptions: Ref<FilterOption[]>,
  option: FilterOption,
) => {
  selectedOptions.value = selectedOptions.value.filter(
    (opt) => option.title != opt.title,
  );
};
