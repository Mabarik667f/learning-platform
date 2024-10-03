from typing import Annotated
from fastapi import Depends
from core.deps import SessionDep
from .crud import SectionCrud, SubSectionCrud


async def get_section_crud(session: SessionDep):
    return SectionCrud(session)

async def get_subsection_crud(session: SessionDep):
    return SubSectionCrud(session)

SectionCrudDep = Annotated[SectionCrud, Depends(get_section_crud)]
SubSectionCrudDep = Annotated[SubSectionCrud, Depends(get_subsection_crud)]
