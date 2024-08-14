import { RegisterFormInterface } from "../interfaces/RegisterForm";
import { ErrorsType } from "@/interfaces/errorsInterfaces";

export class RegFormValidator implements RegisterFormInterface {
  username: string;
  email: string;
  password: string;
  password2: string;
  errors: ErrorsType;

  constructor(formData: RegisterFormInterface) {
    this.username = formData.username;
    this.email = formData.email;
    this.password = formData.password;
    this.password2 = formData.password2;
    this.errors = { username: [], email: [], password: [] };
  }

  public formValidation(): ErrorsType {
    this._checkPassword();
    this._checkUsername();
    return this.errors;
  }

  protected _checkPassword() {
    if (this.password.length < 8) {
      this.errors["password"].push("Длина пароля меньше 8!");
    }

    if (this.password != this.password2) {
      this.errors["password"].push("Пароли не совпадают!");
    }
  }

  protected _checkUsername() {
    if (this.username.length < 4) {
      this.errors["username"].push("Длина логина должна быть больше 4!");
    }
  }
}
