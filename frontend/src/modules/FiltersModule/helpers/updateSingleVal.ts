import { SetupContext } from "vue";

export default async function updateSingleVal(
  event: Event,
  modelValue: any,
  emit: SetupContext["emit"],
  postfix: String = "FilterInp",
) {
  console.log(`update${postfix}`);
  emit(
    `update${postfix}`,
    (event.target as HTMLInputElement).value,
    modelValue,
  );
}
