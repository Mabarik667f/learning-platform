import { ErrorsType } from "@/interfaces/errorsInterfaces";
export default function errorsIsEmpty(errors: ErrorsType) {
  for (const field in errors) {
    if (errors[field].length != 0) {
      return false;
    }
  }
  return true;
}
