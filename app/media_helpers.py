import datetime
from fastapi import HTTPException, UploadFile
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from core.crud import BaseCrud
from models.courses import (
    TaskType as TaskTypeModel,
    Answer as AnswerModel,
    Task as TaskModel,
    TaskTest as TaskTestModel,
    Course as CourseModel,
    Section as SectionModel,
    Subsection as SubsectionModel
)

from sqlalchemy.ext.asyncio import AsyncSession
from shutil import rmtree

class UploadMediaFile:

    def __init__(self, course_id: int, session: AsyncSession) -> None:
        self.course_id = course_id
        self.session = session

    @staticmethod
    def get_default_file_name():
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def delete_dir_content(path: Path):
        [f.unlink() for f in path.glob("*") if f.is_file()]

    async def write_video_for_task(self, task_obj: TaskModel, file: UploadFile):
        upload_path = Path(task_obj.get_upload_path_for_video(self.course_id))

        if upload_path.is_dir():
            self.delete_dir_content(upload_path)

        task_obj.video_path = await self.write_media_content(file, upload_path)
        await self.session.commit()
        await self.session.refresh(task_obj)

    async def write_test_for_task(self, test_obj: TaskTestModel, file: UploadFile):
        upload_path = Path(test_obj.get_upload_path_for_test(self.course_id))

        test_obj.test_file = await self.write_media_content(file, upload_path)
        await self.session.commit()
        await self.session.refresh(test_obj)

    async def write_img_for_course(self, course_obj: CourseModel, file: UploadFile):
        upload_path = Path(course_obj.get_upload_path_for_img())
        if upload_path.is_dir():
            self.delete_dir_content(upload_path)

        course_obj.img = await self.write_media_content(file, upload_path)

    async def write_media_content(self, file: UploadFile, upload_path: Path) -> str:
        upload_path.mkdir(parents=True, exist_ok=True)
        if not file.filename:
            file.filename = self.get_default_file_name()
        file_path = f"{str(upload_path)}/{file.filename}"
        with open(file_path, "wb") as buf:
            buf.write(await file.read())
        return file_path


def delete_dir_media(path: str):
    rmtree(path)


def check_content_type(types: list[str], file: UploadFile):
    if file.content_type not in types:
        raise HTTPException(status_code=400, detail=f"invalid type of file!")
