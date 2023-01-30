/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Design } from './Design';
import type { Head } from './Head';
import type { Sidebar } from './Sidebar';
import type { Verh } from './Verh';
import type { WorkZona } from './WorkZona';

/** @see {isPage} ts-auto-guard:type-guard */
export type Page = {
    design: Design;
    verh: Verh;
    head: Head;
    sidebar: Sidebar;
    work_zona: WorkZona;
    footer: any;
};

