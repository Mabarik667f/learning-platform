from fastapi import Depends
from typing import Annotated
from crud.sections import SectionCrud, SubSectionCrud
from core.deps import SessionDep


async def get_section_crud(session: SessionDep):
    return SectionCrud(session)


async def get_subsection_crud(session: SessionDep):
    return SubSectionCrud(session)


SectionCrudDep = Annotated[SectionCrud, Depends(get_section_crud)]
SubSectionCrudDep = Annotated[SubSectionCrud, Depends(get_subsection_crud)]
