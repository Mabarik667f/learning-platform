import { BaseModel, MultiselectOption } from "@/interfaces/objectsInterfaces";

export default function convertForMultiselect(
  objects: BaseModel[],
): MultiselectOption[] {
  const new_objects: MultiselectOption[] = [];
  for (const obj of objects) {
    new_objects.push({
      label: obj.title,
      value: obj.id ? obj.id : obj.title,
    });
  }
  return new_objects;
}
