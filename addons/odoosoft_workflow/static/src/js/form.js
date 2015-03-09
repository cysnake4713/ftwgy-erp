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
            this.is_reject = this.node.attrs.is_reject === 'True' || this.node.attrs.is_reject === '1';
        },
        on_click: function () {
            var context = this.build_context().eval();
            if (context.state !== undefined && this.is_reject) {
                this.view.reject_state = context.state;
            } else {
                this.view.reject_state = undefined;
            }
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
            var result = false;
            if (this.states_required != undefined) {
                var current_state = this.view.get_field_value('state');
                if ($.inArray(current_state, this.states_required.split(',')) > -1) {
                    result = true;
                }
                if (this.view.reject_state != undefined) {
                    if ($.inArray(this.view.reject_state, this.states_required.split(',')) < 0) {
                        result = false;
                    } else {
                        result = true;
                    }
                }
            }
            return result;
        },

        _set_required: function () {
            this.$el.toggleClass('oe_form_required', this.is_states_required() || this.get("required"));
        }
    });
    //
    //instance.web.form.FormWidget.include({
    //    init: function (field_manager, node) {
    //        this._super(field_manager, node);
    //        this.states_editable = this.node.attrs.states_editable;
    //        var self = this;
    //        var test_effective_readonly = function () {
    //            self.set({"effective_readonly": self.get("readonly") || self.field_manager.get("actual_mode") === "view" || self.is_states_readonly()});
    //        };
    //        this.on("change:readonly", this, test_effective_readonly);
    //        this.field_manager.on("change:actual_mode", this, test_effective_readonly);
    //        test_effective_readonly.call(this);
    //    },
    //
    //    is_states_readonly: function () {
    //        if (this.states_editable != undefined) {
    //            var current_state = this.view.get_field_value('state');
    //            if ($.inArray(current_state, this.states_editable.split(',')) > -1) {
    //                return false;
    //            } else {
    //                return true;
    //            }
    //        } else {
    //            return false;
    //        }
    //    }
    //})

    instance.web.form.FormWidget.include({


        init: function (field_manager, node) {
            this._super(field_manager, node);
            this.states_required = this.node.attrs.states_required;
            this.states_editable = this.node.attrs.states_editable;
            //this.field_manager.on("view_content_has_changed", this, this.check_states_required);
            this.field_manager.on("view_content_has_changed", this, this.check_states_readonly);
        },
        renderElement: function () {
            //this.check_states_required();
            this.check_states_readonly();
            this._super();
        },

        //check_states_required: function () {
        //    var current_state = this.view.get_field_value('state');
        //    if (this.states_required != undefined) {
        //        if ($.inArray(current_state, this.states_required.split(',')) > -1) {
        //            this.set({required: true});
        //        } else {
        //            this.set({required: false});
        //        }
        //        if (this.view.reject_state != undefined && $.inArray(this.view.reject_state, this.states_required.split(',')) < 0) {
        //            this.set({required: false});
        //        }
        //    }
        //},

        check_states_readonly: function () {
            var self = this;
            if (this.states_editable != undefined) {
                var current_state = this.view.get_field_value('state');
                var states_map = py.eval(this.states_editable);
                if (_.has(states_map, current_state)) {
                    var current_state_setting = states_map[current_state];
                    if (current_state_setting == false) {
                        this.set({readonly: false});
                    } else if (_.has(current_state_setting, 'groups')) {
                        new instance.web.DataSetSearch(this, 'res.users', this.session.user_context, [
                            ['id', '=', this.session.uid], ['groups_id', '=', current_state_setting.groups]
                        ]).read_slice(['id']).done(function (result) {
                                if (_.isEmpty(result)) {
                                        self.set({readonly: true});
                                } else {
                                    self.set({readonly: false});
                                }
                            });

                    } else {
                        console.log('mismatch state_editable type!!');
                        this.set({readonly: true});
                    }
                } else {
                    this.set({readonly: true});
                }
            }
        }
    });


};
