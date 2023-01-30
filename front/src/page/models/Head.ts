/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ins } from './Ins';
import type { MenuItem } from './MenuItem';

export type Head = {
    active_menu: number;
    ins: Ins;
    menu?: Array<MenuItem>;
};
