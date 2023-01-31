/*
 * Generated type guards for "Page.ts".
 * WARNING: Do not manually change this file.
 */
import { Page } from "./Page";

export function isPage(obj: unknown): obj is Page {
    const typedObj = obj as Page
    return (
        (typedObj !== null &&
            typeof typedObj === "object" ||
            typeof typedObj === "function") &&
        (typedObj["design"] !== null &&
            typeof typedObj["design"] === "object" ||
            typeof typedObj["design"] === "function") &&
        typeof typedObj["design"]["font"] === "number" &&
        typeof typedObj["design"]["background"] === "string" &&
        typeof typedObj["design"]["footer"] === "boolean" &&
        typeof typedObj["design"]["caption"] === "boolean" &&
        typeof typedObj["design"]["checkbox"] === "boolean" &&
        typeof typedObj["design"]["sidebar"] === "boolean" &&
        Array.isArray(typedObj["design"]["css"]) &&
        typedObj["design"]["css"].every((e: any) =>
            typeof e === "string"
        ) &&
        (typedObj["verh"] !== null &&
            typeof typedObj["verh"] === "object" ||
            typeof typedObj["verh"] === "function") &&
        typeof typedObj["verh"]["title"] === "string" &&
        typeof typedObj["verh"]["sidebar_icon"] === "string" &&
        Array.isArray(typedObj["verh"]["icons"]) &&
        typedObj["verh"]["icons"].every((e: any) =>
            typeof e === "string"
        ) &&
        (typedObj["head"] !== null &&
            typeof typedObj["head"] === "object" ||
            typeof typedObj["head"] === "function") &&
        (typeof typedObj["head"]["active_menu"] === "undefined" ||
            typeof typedObj["head"]["active_menu"] === "number") &&
        (typedObj["head"]["ins"] !== null &&
            typeof typedObj["head"]["ins"] === "object" ||
            typeof typedObj["head"]["ins"] === "function") &&
        typeof typedObj["head"]["ins"]["orgstr"] === "string" &&
        typeof typedObj["head"]["ins"]["brod"] === "string" &&
        (typeof typedObj["head"]["menu"] === "undefined" ||
            Array.isArray(typedObj["head"]["menu"]) &&
            typedObj["head"]["menu"].every((e: any) =>
                (e !== null &&
                    typeof e === "object" ||
                    typeof e === "function") &&
                typeof e["kod"] === "number" &&
                typeof e["kod_parent"] === "number" &&
                typeof e["name"] === "string" &&
                typeof e["typ_menu"] === "string" &&
                (typeof e["ref"] === "undefined" ||
                    typeof e["ref"] === "number") &&
                (typeof e["sub"] === "undefined" ||
                    typeof e["sub"] === "number") &&
                (typeof e["alert"] === "undefined" ||
                    (e["alert"] !== null &&
                        typeof e["alert"] === "object" ||
                        typeof e["alert"] === "function") &&
                    typeof e["alert"]["title"] === "string" &&
                    typeof e["alert"]["text"] === "string")
            )) &&
        (typedObj["sidebar"] !== null &&
            typeof typedObj["sidebar"] === "object" ||
            typeof typedObj["sidebar"] === "function") &&
        (typedObj["sidebar"]["user"] === null ||
            (typedObj["sidebar"]["user"] !== null &&
                typeof typedObj["sidebar"]["user"] === "object" ||
                typeof typedObj["sidebar"]["user"] === "function") &&
            typeof typedObj["sidebar"]["user"]["username"] === "string" &&
            typeof typedObj["sidebar"]["user"]["status"] === "string" &&
            typeof typedObj["sidebar"]["user"]["datetime"] === "string") &&
        (typedObj["work_zona"] !== null &&
            typeof typedObj["work_zona"] === "object" ||
            typeof typedObj["work_zona"] === "function") &&
        (typeof typedObj["work_zona"]["background"] === "undefined" ||
            typedObj["work_zona"]["background"] === null ||
            typeof typedObj["work_zona"]["background"] === "string") &&
        (typeof typedObj["work_zona"]["icon"] === "undefined" ||
            typedObj["work_zona"]["icon"] === null ||
            Array.isArray(typedObj["work_zona"]["icon"]) &&
            typedObj["work_zona"]["icon"].every((e: any) =>
                typeof e === "string"
            )) &&
        (typeof typedObj["work_zona"]["title"] === "undefined" ||
            typedObj["work_zona"]["title"] === null ||
            typeof typedObj["work_zona"]["title"] === "string") &&
        (typeof typedObj["work_zona"]["end_title"] === "undefined" ||
            typedObj["work_zona"]["end_title"] === null ||
            typeof typedObj["work_zona"]["end_title"] === "string")
    )
}
