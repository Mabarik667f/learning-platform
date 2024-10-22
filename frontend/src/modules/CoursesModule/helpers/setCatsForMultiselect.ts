import convertForMultiselect from "@/helpers/convertForMultiselect";
import { MultiselectOption } from "@/interfaces/objectsInterfaces";
import { getCategories } from "@/modules/CategoriesModule";

export default async function setCatsForMultiselect(): Promise<
  MultiselectOption[]
> {
  const baseCats = await getCategories();
  return convertForMultiselect(baseCats);
}
