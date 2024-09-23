/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ICompanyRead } from './ICompanyRead';
import type { INextCursor } from './INextCursor';
export type IResponsePaginated_ICompanyRead_ = {
    items: Array<ICompanyRead>;
    total: (number | null);
    limit: (number | null);
    offset: (number | null);
    next?: (INextCursor | null);
};

