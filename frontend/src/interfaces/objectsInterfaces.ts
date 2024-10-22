export interface BaseModel {
  title: string;
  id?: number;
}

export interface MultiselectOption {
  label: string;
  value: any;
  disabled?: boolean;
}

export interface Difficulty extends BaseModel {}
