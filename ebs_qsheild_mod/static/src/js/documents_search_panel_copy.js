/** @odoo-module **/
// comment by mervat: not allow to add event
import { _t } from "@web/core/l10n/translation";
import { SearchPanel } from "@web/search/search_panel/search_panel";



export class DocumentsSearchPanel extends SearchPanel {

events: Object.assign({}, SearchPanel.prototype.events, {
        'dragenter .o_search_panel_category_value, .o_search_panel_filter_value': '_onDragEnter',
        'dragleave .o_search_panel_category_value, .o_search_panel_filter_value': '_onDragLeave',
        'dragover .o_search_panel_category_value, .o_search_panel_filter_value': '_onDragOver',
        'drop .o_search_panel_category_value, .o_search_panel_filter_value': '_onRecordDrop',
    }),


}