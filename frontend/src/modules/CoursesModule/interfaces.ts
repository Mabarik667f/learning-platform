import { Category } from "../CategoriesModule";

export interface Course {
  title: string;
  describe: string;
  img: File | null;
  price: number;
  difficulty: string;
}

export interface CourseCreate extends Course {
  categories?: number[];
}

export interface CourseResponse extends Course {
  id: number;
  categories: Category[];
}
