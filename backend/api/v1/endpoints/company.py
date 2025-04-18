from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from api.dependencies.pvz import pvz_service_dependency
from api.dependencies.user import current_active_user
from crud.company import company_crud
from crud.office import office_crud
from models.user import User
from schemas.company import ICompanyRead
from services.pvz_service import PVZService
from enums.user import UserRoleEnum
from api.dependencies.api_key import get_api_key 
from schemas.office import IOfficeUpdate, UpdateOfficesRequest
from typing import List



# import wb_franchise_api_client as wb
# from wb_franchise_api_client.models import RequestCodeResponse, TokenResponse, AccountData
# from wb_franchise_api_client.api_client import ApiAuth


# router = APIRouter(
#     generate_unique_id_function=lambda route: f"company_{route.name}",
# )


# # @router.post(path="/request_code", response_model=RequestCodeResponse)
# # async def request_code(
# #         phone: str,
# #         api_auth: ApiAuth = Depends(get_api_auth),
# #         user: User = Depends(current_active_user),
# #     ):
# #     """Request code to auth in Franchise
# #     :param phone: Phone number
# #     :param api_auth: API auth client
# #     :param user: Current active user
# #     :return Response from WB API
# #     """
# #     code_response = await api_auth.request_code(phone)
# #     return code_response


# # @router.post(path="/verify_code", response_model=TokenResponse)
# # async def verify_code(
# #         phone: str,
# #         code: str,
# #         api_auth: ApiAuth = Depends(get_api_auth),
# #         user: User = Depends(current_active_user)):
# #     """Verify code from WB API and obtain tokens

# #     :param phone: Phone number
# #     :param code: Code from WB API
# #     :param api_auth: API auth client
# #     :param user: Current active user
# #     """
# #     token_response = await api_auth.connect_code(username=phone, password=code)
# #     await redis_client.set(f"{phone}:access_token", token_response.access_token)
# #     await redis_client.set(f"{phone}:refresh_token", token_response.refresh_token)
# #     return token_response


# @router.get(
#     path="",
#     response_model=IResponsePaginated[ICompanyRead],
# )
# async def get_list(
#     order_by: str = "id",
#     order: ListOrderEnum = ListOrderEnum.descendent,
#     params: LimitOffsetParams = Depends(),
#     user: User = Depends(current_active_user),
# ):
#     """Get list of all companies of current user

#     :param order_by: Order by field
#     :param order: Order direction (asc or desc) Default: desc
#     :param params: Pagination parameters
#     :param user: Current active user
#     :return: List of companies paginated
#     """
#     query = select(Company).where(
#         relations(Company.users).any(col(User.id) == user.id),
#     )

#     page = await company_crud.get_multi_paginated_ordered(
#         query=query,
#         params=params,
#         order_by=order_by,
#         order=order,
#     )

#     return page


# @router.get(
#     path="/{id}",
#     response_model=ICompanyRead,
# )
# async def get_by_id(
#     id: int,
# ):
#     """Get company by id

#     :param id: Company id
#     :return: Company
#     """
#     company = await company_crud.get(
#         id=id,
#     )

#     if not company:
#         raise NotFound

#     return company


# @router.post('', response_model=ICompanyRead)
# async def create(
#     payload: ICompanyCreate,
#     user: User = Depends(current_active_user)
# ):
#     """Create company

#     :param payload: Company payload
#     :param user: Current active user
#     :return: Company
#     """
#     api_client = await get_api_client(phone=payload.phone)
#     company_data = await api_client.get_account_data()

#     company = await company_crud.create(
#         obj_in=ICompanyCreate(
#             supplier_id=company_data.supplier_id,
#             name=company_data.name,
#             phone=payload.phone
#         )
#     )
#     company = await company_crud.add_user(
#         company=company,
#         user=user,
#     )

#     # Добавляем офисы в компанию
#     await office_crud.create_or_update_multi(
#         list_in=company_data.offices,
#         index_elements=[col(Office.office_id)],
#         on_conflict_set={"name", "office_shk", "is_site_active"},
#         additionals=dict(company_id=company.id)

#     )

#     #  Добавляем сотрудников в компанию
#     await employee_crud.create_or_update_multi(
#         list_in=company_data.employees,
#         index_elements=[col(Employee.employee_id)],
#         on_conflict_set={
#             "first_name",
#             "is_deleted",
#             "last_name",
#             "middle_name",
#             "phones",
#             "rating",
#             "shortages_sum"
#         },
#         additionals=dict(company_id=company.id)
#     )

#     return company

#     #company = await company_crud.add_user(
#     #    company=company,
#     #    user=user,
#     #)

#     #await CompanyService.sync_cards( TODO : here will be request to get company info from external api
#     #    company=company,
#     #)



# @router.put(
#     path="/{id}",
#     response_model=ICompanyRead,
# )
# async def update(
#     id: int,
#     payload: ICompanyUpdate,
# ):
#     """Update Company

#     :param id: Company id
#     :param payload: Company payload
#     :return: Company
#     """
#     company = await company_crud.get(
#         id=id,
#     )

#     if not company:
#         raise NotFound

#     company_updated = await company_crud.update(
#         obj_current=company,
#         obj_new=payload,
#     )

#     return company_updated


# @router.delete(
#     path="/{id}",
#     response_model=ICompanyRead,
# )
# async def delete(
#     id: int,
# ):
#     """Delete Company

#     :param id: Company id
#     :return: Deleted company
#     """
#     company = await company_crud.get(
#         id=id,
#     )

#     if not company:
#         raise NotFound

#     company_deleted = await company_crud.delete(id=company.id)

#     return company_deleted

router = APIRouter(
    generate_unique_id_function=lambda route: f"company_{route.name}",
)

current_user_dependency = Depends(current_active_user)
api_key_dependency = Depends(get_api_key)

@router.post("/register-company", response_model=ICompanyRead)
async def register_company(
    current_user: Annotated[User, current_user_dependency],
    pvz_service: Annotated[PVZService, pvz_service_dependency]
):
    """
    Регистрация компании.
    Доступно только для пользователей с ролью admin
    """
    
    if current_user.role not in [UserRoleEnum.ADMIN, UserRoleEnum.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required."
        )

    # 1. Get company info from WB
    owner_info = await pvz_service.get_owner_info()

    existing_company = await company_crud.get_company_by_wb_user_id(owner_info.wb_user_id)
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company is already registered"
        )
    
    offices = await pvz_service.get_pickpoint_list()
    
     # Register company with all relations
    company = await company_crud.register_company(
        owner_info=owner_info,
        offices=offices,
        current_user=current_user
    )
    
    return company

@router.post("/update-offices", response_model=ICompanyRead)
async def update_offices(
    request: UpdateOfficesRequest,
    api_key: Annotated[str, api_key_dependency]
):
    """
    Обновление списка офисов компании.
    
    """
    company = await company_crud.get_or_404(id=request.company_id)

    success = await office_crud.update_list_offices_by_external_id(
        offices=request.offices,
        company_id=company.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No matching offices found for company {company.id}"
        )

    updated_company = await company_crud.get_or_404(request.company_id)
    return updated_company
    