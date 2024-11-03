from sqlalchemy import select, func, Result
from models.courses import Section, Subsection
from core.crud import BaseCrud


class SectionUtils(BaseCrud):

    async def get_last_pos_for_section(self) -> int:
        q = select(func.max(Section.position))
        res = await self.session.execute(q)
        return self.get_last_pos(res)

    async def get_last_pos_for_subsection(self) -> int:
        q = select(func.max(Subsection.position))
        res = await self.session.execute(q)
        return self.get_last_pos(res)

    @staticmethod
    def get_last_pos(res: Result[tuple[int]]) -> int:
        last_pos = res.fetchone()
        if last_pos is None:
            return 0
        else:
            return last_pos.tuple()[0]
