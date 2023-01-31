/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Tab } from './Tab';

export type WorkZona = {
    background?: string | null;
    icon?: Array<string> | null;
    title?: string | null;
    end_title?: string | null;
    tabs?: Array<Tab> | null;
};
