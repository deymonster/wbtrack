from fastapi import APIRouter, Depends
from fastapi_pagination import LimitOffsetParams
from sqlmodel import col, select

from core.exceptions import NotFound, ValidationError
from config import settings
from core.utils.sqlmodel import relations
from api.dependencies.user import current_active_user
from enums.common import ListOrderEnum
from models.company import Company
from crud.company import company_crud
from models.company_user import CompanyUser
from models.user import User
from schemas.company import ICompanyCreate, ICompanyRead, ICompanyUpdate
from schemas.response import IResponsePaginated

import wb_franchise_api_client as wb
from wb_franchise_api_client.models import RequestCodeResponse, TokenResponse


router = APIRouter(
    generate_unique_id_function=lambda route: f"company_{route.name}",
)

api_config = wb.APIConfig(
    base_path=settings.WILDBERRIES_BASE_PATH,
    auth_base_path=settings.AUTH_BASE_PATH,
    basic_token=settings.WB_BASIC_TOKEN,
)
api_auth = wb.ApiAuth(api_config=api_config)


@router.post(path="/request_code", response_model=RequestCodeResponse)
async def request_code(phone: str, user: User = Depends(current_active_user)):
    """Request code to auth in Franchise
    :param phone: Phone number
    :param user: Current active user
    :return Response from WB API
    """
    code_response = await api_auth.request_code(phone)
    return code_response


@router.post(path="/verify_code", response_model=TokenResponse)
async def verify_code(phone: str, code: str, user: User = Depends(current_active_user)):
    """Verify code from WB API and obtain tokens

    :param phone: Phone number
    :param code: Code from WB API
    :param user: Current active user
    """
    token_response = await api_auth.connect_code(username=phone, password=code)
    return token_response


@router.get(
    path="",
    response_model=IResponsePaginated[ICompanyRead],
)
async def get_list(
    order_by: str = "id",
    order: ListOrderEnum = ListOrderEnum.descendent,
    params: LimitOffsetParams = Depends(),
    user: User = Depends(current_active_user),
):
    """Get list of all companies of current user

    :param order_by: Order by field
    :param order: Order direction (asc or desc) Default: desc
    :param params: Pagination parameters
    :param user: Current active user
    :return: List of companies paginated
    """
    query = select(Company).where(
        relations(Company.users).any(col(User.id) == user.id),
    )

    page = await company_crud.get_multi_paginated_ordered(
        query=query,
        params=params,
        order_by=order_by,
        order=order,
    )

    return page


@router.get(
    path="/{id}",
    response_model=ICompanyRead,
)
async def get_by_id(
    id: int,
):
    """Get company by id

    :param id: Company id
    :return: Company
    """
    company = await company_crud.get(
        id=id,
    )

    if not company:
        raise NotFound

    return company


async def create(
    payload: ICompanyCreate,
    user: User = Depends(current_active_user),
):
    """Create company

    :param payload: Company payload
    :param user: Current active user
    :return: Company
    """
    company = await company_crud.create(
        obj_in=payload,
    )

    company = await company_crud.add_user(
        company=company,
        user=user,
    )

    #await CompanyService.sync_cards( TODO : here will be request to get company info from external api
    #    company=company,
    #)

    return company

@router.put(
    path="/{id}",
    response_model=ICompanyRead,
)
async def update(
    id: int,
    payload: ICompanyUpdate,
):
    """Update Company

    :param id: Company id
    :param payload: Company payload
    :return: Company
    """
    company = await company_crud.get(
        id=id,
    )

    if not company:
        raise NotFound

    company_updated = await company_crud.update(
        obj_current=company,
        obj_new=payload,
    )

    return company_updated


@router.delete(
    path="/{id}",
    response_model=ICompanyRead,
)
async def delete(
    id: int,
):
    """Delete Company

    :param id: Company id
    :return: Deleted company
    """
    company = await company_crud.get(
        id=id,
    )

    if not company:
        raise NotFound

    company_deleted = await company_crud.delete(id=company.id)

    return company_deleted
