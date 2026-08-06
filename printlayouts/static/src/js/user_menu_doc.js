/** @odoo-module **/
import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";

const DOC_URL = "/printlayouts/static/src/manual/b_so_manual.html";

registry.category("user_menuitems").add(
    "documentation",
    () => ({
        type: "item",
        id: "documentation",
        description: _t("Documentation"),
        href: DOC_URL,
        callback: () => { browser.open(DOC_URL, "_blank"); },
        sequence: 10,
    }),
    { force: true }
);
