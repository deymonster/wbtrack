/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
// @ts-nocheck
import type { Body_login_api_v1_auth_login_post } from '../models/Body_login_api_v1_auth_login_post';
import type { Body_reset_forgot_password_api_v1_auth_forgot_password_post } from '../models/Body_reset_forgot_password_api_v1_auth_forgot_password_post';
import type { Body_reset_reset_password_api_v1_auth_reset_password_post } from '../models/Body_reset_reset_password_api_v1_auth_reset_password_post';
import type { Body_verify_request_token_api_v1_auth_request_verify_token_post } from '../models/Body_verify_request_token_api_v1_auth_request_verify_token_post';
import type { Body_verify_verify_api_v1_auth_verify_post } from '../models/Body_verify_verify_api_v1_auth_verify_post';
import type { IUserCreate } from '../models/IUserCreate';
import type { IUserRead } from '../models/IUserRead';
import type { LoginResponse } from '../models/LoginResponse';
import type { RefreshTokenRequest } from '../models/RefreshTokenRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AuthService {
    /**
     * Login
     * Endpoint to login
     * @returns LoginResponse Successful Response
     * @throws ApiError
     */
    public static loginApiV1AuthLoginPost({
        formData,
    }: {
        formData: Body_login_api_v1_auth_login_post,
    }): CancelablePromise<LoginResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/auth/login',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Register:Register
     * @returns IUserRead Successful Response
     * @throws ApiError
     */
    public static registerRegisterApiV1AuthRegisterPost({
        requestBody,
    }: {
        requestBody: IUserCreate,
    }): CancelablePromise<IUserRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/auth/register',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reset:Forgot Password
     * @returns any Successful Response
     * @throws ApiError
     */
    public static resetForgotPasswordApiV1AuthForgotPasswordPost({
        requestBody,
    }: {
        requestBody: Body_reset_forgot_password_api_v1_auth_forgot_password_post,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/auth/forgot-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reset:Reset Password
     * @returns any Successful Response
     * @throws ApiError
     */
    public static resetResetPasswordApiV1AuthResetPasswordPost({
        requestBody,
    }: {
        requestBody: Body_reset_reset_password_api_v1_auth_reset_password_post,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/auth/reset-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Verify:Request-Token
     * @returns any Successful Response
     * @throws ApiError
     */
    public static verifyRequestTokenApiV1AuthRequestVerifyTokenPost({
        requestBody,
    }: {
        requestBody: Body_verify_request_token_api_v1_auth_request_verify_token_post,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/auth/request-verify-token',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Verify:Verify
     * @returns IUserRead Successful Response
     * @throws ApiError
     */
    public static verifyVerifyApiV1AuthVerifyPost({
        requestBody,
    }: {
        requestBody: Body_verify_verify_api_v1_auth_verify_post,
    }): CancelablePromise<IUserRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/auth/verify',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Refresh Token
     * Endpoint to refresh the token
     * @returns any Successful Response
     * @throws ApiError
     */
    public static refreshTokenApiV1AuthRefreshTokenPost({
        requestBody,
    }: {
        requestBody: RefreshTokenRequest,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/auth/refresh-token',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
