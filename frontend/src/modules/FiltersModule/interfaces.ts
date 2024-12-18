import { BaseModel } from "@/interfaces/objectsInterfaces";

export interface FilterOption extends BaseModel {}

export interface Prices {
  min_price: number | string;
  max_price: number | string;
}

export interface QueryParams {
  min_price?: string | number;
  max_price?: string | number;
  queryCat?: string;
  difficulties?: string;
  categories?: string;
  [key: string]: any;
}
