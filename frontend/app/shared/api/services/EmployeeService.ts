/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
// @ts-nocheck
import type { AuthRequest } from '../models/AuthRequest';
import type { IResponsePaginated_IEmployeeRead_ } from '../models/IResponsePaginated_IEmployeeRead_';
import type { ListOrderEnum } from '../models/ListOrderEnum';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class EmployeeService {
    /**
     * Login
     * @returns any Successful Response
     * @throws ApiError
     */
    public static employeeLogin({
        requestBody,
    }: {
        requestBody: AuthRequest,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/employee/login',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Confirm Code
     * @returns any Successful Response
     * @throws ApiError
     */
    public static employeeConfirmCode({
        requestBody,
    }: {
        requestBody: AuthRequest,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/employee/confirm',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Info Employee
     * @returns any Successful Response
     * @throws ApiError
     */
    public static employeeGetInfoEmployee(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/employee/me',
        });
    }
    /**
     * Get List
     * Get list of all employees
     *
     * :param order_by: Order by field
     * :param order: Order direction (asc or desc) Default: desc
     * :param params: Pagination parameters
     * :param user: Current active user
     * :return: List of employees paginated
     * @returns IResponsePaginated_IEmployeeRead_ Successful Response
     * @throws ApiError
     */
    public static employeeGetList({
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
    }): CancelablePromise<IResponsePaginated_IEmployeeRead_> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/employee',
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
}
