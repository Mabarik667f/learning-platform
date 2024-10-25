import { CourseStruct } from "../interfaces";
import { ref } from "vue";

export default class CreateCourseStruct {
  struct = ref<CourseStruct>();

  constructor() {
    this.struct.value = { sections: [] };
  }

  addSection(): void {
    this.struct.value?.sections.push({
      title: "",
      describe: "",
      position: this.getCreateSectionPos(),
      subsections: [],
    });
  }

  delSection(pos: number): void {
    const sects = this.struct.value?.sections;
    if (sects) {
      for (const s of sects.slice(pos)) {
        s.position -= 1;
      }
      sects.splice(pos, 1);
    }
  }

  addSubSection(pos: number): void {
    this.struct.value?.sections[pos].subsections.push({
      title: "",
      position: this.getCreateSubSectionPos(pos),
    });
  }

  delSubSection(secPos: number, subPos: number): void {
    const subs = this.struct.value?.sections[secPos].subsections;
    if (subs) {
      for (const s of subs.slice(subPos)) {
        s.position -= 1;
      }
      subs.splice(subPos, 1);
    }
  }

  getCreateSectionPos(): number {
    const len = this.struct.value?.sections.length;
    return len ? len + 1 : 1;
  }

  getCreateSubSectionPos(pos: number): number {
    const len = this.struct.value?.sections[pos].subsections.length;
    return len ? len + 1 : 1;
  }
}
