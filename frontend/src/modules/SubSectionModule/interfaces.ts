export interface SubSection {
  title: string;
  position: number;
}
export interface SubSectionResponse extends SubSection {
  id: number;
}
export interface SubSectionCreate extends SubSection {}
