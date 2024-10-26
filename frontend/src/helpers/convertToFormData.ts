export default function (obj: Object): FormData {
  const formData = new FormData();
  for (const [key, val] of Object.entries(obj)) {
    if (
      (val instanceof Array || val instanceof Object) &&
      !(val instanceof File || val instanceof Blob) &&
      key !== "categories"
    ) {
      formData.append(key, JSON.stringify(val));
    } else {
      formData.append(key, val);
    }
  }
  return formData;
}
