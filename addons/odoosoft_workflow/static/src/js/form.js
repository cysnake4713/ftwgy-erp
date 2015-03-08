/**
 * Created by cysnake4713 on 15-3-8.
 */


openerp.odoosoft_workflow = function (instance) {

    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;


    instance.web.form.WidgetButton.include({
        init: function (field_manager, node) {
            this._super(field_manager, node);
            this.is_reject = this.node.attrs.is_reject == '1';
        },
        on_click: function () {
            this.view.is_reject = this.is_reject;
            return this._super();
        }

    });

    instance.web.form.AbstractField.include({
        init: function (field_manager, node) {
            this._super(field_manager, node);
            this.states_required = this.node.attrs.states_required;
        },
        is_valid: function () {
            return this.is_syntax_valid() && !(this.get('required') && this.is_false()) && !(this.is_states_required() && this.is_false());
        },
        is_states_required: function () {
            if (this.states_required != undefined && this.view.is_reject != true) {
                var current_state = this.view.get_field_value('state');
                if ($.inArray(current_state, this.states_required.split(',')) > -1) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        },
        _set_required: function () {
            this.$el.toggleClass('oe_form_required', this.is_states_required() || this.get("required"));
        }
    });


};
