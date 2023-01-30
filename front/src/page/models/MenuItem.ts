/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Alert } from './Alert';

export type MenuItem = {
    kod: number;
    kod_parent: number;
    name: string;
    typ_menu: string;
    ref?: number;
    sub?: number;
    alert?: Alert;
};
