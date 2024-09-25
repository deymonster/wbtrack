/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
// @ts-nocheck
import type { AuthRequest } from '../models/AuthRequest';
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
}
