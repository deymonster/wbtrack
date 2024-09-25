/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
// @ts-nocheck
import type { IUserRead } from '../models/IUserRead';
import type { IUserUpdate } from '../models/IUserUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UserService {
    /**
     * Users:Current User
     * @returns IUserRead Successful Response
     * @throws ApiError
     */
    public static usersCurrentUserApiV1UserMeGet(): CancelablePromise<IUserRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/user/me',
            errors: {
                401: `Missing token or inactive user.`,
            },
        });
    }
    /**
     * Users:Patch Current User
     * @returns IUserRead Successful Response
     * @throws ApiError
     */
    public static usersPatchCurrentUserApiV1UserMePatch({
        requestBody,
    }: {
        requestBody: IUserUpdate,
    }): CancelablePromise<IUserRead> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/user/me',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                401: `Missing token or inactive user.`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Users:User
     * @returns IUserRead Successful Response
     * @throws ApiError
     */
    public static usersUserApiV1UserIdGet({
        id,
    }: {
        id: string,
    }): CancelablePromise<IUserRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/user/{id}',
            path: {
                'id': id,
            },
            errors: {
                401: `Missing token or inactive user.`,
                403: `Not a superuser.`,
                404: `The user does not exist.`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Users:Patch User
     * @returns IUserRead Successful Response
     * @throws ApiError
     */
    public static usersPatchUserApiV1UserIdPatch({
        id,
        requestBody,
    }: {
        id: string,
        requestBody: IUserUpdate,
    }): CancelablePromise<IUserRead> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/user/{id}',
            path: {
                'id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                401: `Missing token or inactive user.`,
                403: `Not a superuser.`,
                404: `The user does not exist.`,
                422: `Validation Error`,
            },
        });
    }
    /**
     * Users:Delete User
     * @returns void
     * @throws ApiError
     */
    public static usersDeleteUserApiV1UserIdDelete({
        id,
    }: {
        id: string,
    }): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/user/{id}',
            path: {
                'id': id,
            },
            errors: {
                401: `Missing token or inactive user.`,
                403: `Not a superuser.`,
                404: `The user does not exist.`,
                422: `Validation Error`,
            },
        });
    }
}
