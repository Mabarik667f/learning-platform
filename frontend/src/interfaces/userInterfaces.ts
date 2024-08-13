export enum Role {
  Admin = "admin",
  Default = "user",
  Owner = "owner",
}

export interface User {
  username: string;
  email: string;
  role: Role;
}

export interface UserById extends User {
  id: number;
}
