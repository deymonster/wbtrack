/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ICompanyCreate } from '../models/ICompanyCreate';
import type { ICompanyRead } from '../models/ICompanyRead';
import type { ICompanyUpdate } from '../models/ICompanyUpdate';
import type { IResponsePaginated_ICompanyRead_ } from '../models/IResponsePaginated_ICompanyRead_';
import type { ListOrderEnum } from '../models/ListOrderEnum';
import type { RequestCodeResponse } from '../models/RequestCodeResponse';
import type { TokenResponse } from '../models/TokenResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CompanyService {
    /**
     * Request Code
     * Request code to auth in Franchise
     * :param phone: Phone number
     * :param api_auth: API auth client
     * :param user: Current active user
     * :return Response from WB API
     * @returns RequestCodeResponse Successful Response
     * @throws ApiError
     */
    public static companyRequestCode({
        phone,
    }: {
        phone: string,
    }): CancelablePromise<RequestCodeResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/company/request_code',
            query: {
                'phone': phone,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Verify Code
     * Verify code from WB API and obtain tokens
     *
     * :param phone: Phone number
     * :param code: Code from WB API
     * :param api_auth: API auth client
     * :param user: Current active user
     * @returns TokenResponse Successful Response
     * @throws ApiError
     */
    public static companyVerifyCode({
        phone,
        code,
    }: {
        phone: string,
        code: string,
    }): CancelablePromise<TokenResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/company/verify_code',
            query: {
                'phone': phone,
                'code': code,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get List
     * Get list of all companies of current user
     *
     * :param order_by: Order by field
     * :param order: Order direction (asc or desc) Default: desc
     * :param params: Pagination parameters
     * :param user: Current active user
     * :return: List of companies paginated
     * @returns IResponsePaginated_ICompanyRead_ Successful Response
     * @throws ApiError
     */
    public static companyGetList({
        orderBy = 'id',
        order,
        limit = 50,
        offset,
    }: {
        orderBy?: string,
        order?: ListOrderEnum,
        /**
         * Page size limit
         */
        limit?: number,
        /**
         * Page offset
         */
        offset?: number,
    }): CancelablePromise<IResponsePaginated_ICompanyRead_> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/company',
            query: {
                'order_by': orderBy,
                'order': order,
                'limit': limit,
                'offset': offset,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create
     * Create company
     *
     * :param payload: Company payload
     * :param user: Current active user
     * :return: Company
     * @returns ICompanyRead Successful Response
     * @throws ApiError
     */
    public static companyCreate({
        requestBody,
    }: {
        requestBody: ICompanyCreate,
    }): CancelablePromise<ICompanyRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/company',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get By Id
     * Get company by id
     *
     * :param id: Company id
     * :return: Company
     * @returns ICompanyRead Successful Response
     * @throws ApiError
     */
    public static companyGetById({
        id,
    }: {
        id: number,
    }): CancelablePromise<ICompanyRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/company/{id}',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update
     * Update Company
     *
     * :param id: Company id
     * :param payload: Company payload
     * :return: Company
     * @returns ICompanyRead Successful Response
     * @throws ApiError
     */
    public static companyUpdate({
        id,
        requestBody,
    }: {
        id: number,
        requestBody: ICompanyUpdate,
    }): CancelablePromise<ICompanyRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/company/{id}',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete
     * Delete Company
     *
     * :param id: Company id
     * :return: Deleted company
     * @returns ICompanyRead Successful Response
     * @throws ApiError
     */
    public static companyDelete({
        id,
    }: {
        id: number,
    }): CancelablePromise<ICompanyRead> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/company/{id}',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
