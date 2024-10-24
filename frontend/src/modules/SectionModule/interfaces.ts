import { SubSectionCreate } from "@/modules/SubSectionModule";

export interface Section {
  title: string;
  describe: string;
  position: number;
}
export interface SectionResponse extends Section {
  id: number;
}
export interface SectionCreate extends Section {
  subsections: SubSectionCreate[];
}
