/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
// @ts-nocheck
import type { IEmployeeRead } from './IEmployeeRead';
import type { INextCursor } from './INextCursor';
export type IResponsePaginated_IEmployeeRead_ = {
    items: Array<IEmployeeRead>;
    total: (number | null);
    limit: (number | null);
    offset: (number | null);
    next?: (INextCursor | null);
};

