/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
// @ts-nocheck
import type { UserRoleEnum } from './UserRoleEnum';
export type IUserRead = {
    id: any;
    email: string;
    is_active?: boolean;
    is_superuser?: boolean;
    is_verified?: boolean;
    first_name: (string | null);
    last_name: (string | null);
    middle_name: (string | null);
    phone: (string | null);
    role: UserRoleEnum;
};

