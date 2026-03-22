from fastapi import APIRouter, Depends, status, Path
from fastapi.responses import RedirectResponse
from app.core.dependencies import (
    get_create_link_use_case,
    get_many_link_use_case,
    get_redirect_link_use_case,
    get_delete_link_use_case
)
from app.use_cases.link import CreateLinkUseCase, DeleteLinkUseCase, GetManyLinkUseCase, RedirectLinkUseCase

from app.core.config import get_settings
from app.schemas import ApiResponse
from app.schemas.link import LinkCreate, LinkResponse


settings = get_settings()
router = APIRouter(prefix="/links")

@router.get("/{slug}")
async def get_url(
    slug: str = Path(..., max_length=settings.REDIRECT_SLUG_MAX_LENGTH),
    use_case: RedirectLinkUseCase = Depends(get_redirect_link_use_case)
) -> RedirectResponse:
    url = await use_case.execute(slug=slug)
    return RedirectResponse(
        url=url,
        status_code=status.HTTP_302_FOUND
    )

@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
    slug: str = Path(..., max_length=settings.REDIRECT_SLUG_MAX_LENGTH),
    use_case: DeleteLinkUseCase = Depends(get_delete_link_use_case)
) -> None:
    await use_case.execute(slug=slug)

@router.get("/", response_model=ApiResponse[list[LinkResponse]])
async def list_all(
    use_case: GetManyLinkUseCase = Depends(get_many_link_use_case)
) -> ApiResponse[list[LinkResponse]]:
    link_schemas = await use_case.execute()
    return ApiResponse(data=link_schemas)

@router.post("/new", response_model=ApiResponse[LinkResponse])
async def create_link(
    data: LinkCreate,
    use_case: CreateLinkUseCase = Depends(get_create_link_use_case)
) -> ApiResponse[LinkResponse]:
    link = await use_case.execute(data)
    return ApiResponse(data=LinkResponse.model_validate(link))


