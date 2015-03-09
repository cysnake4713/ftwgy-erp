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
            this.field_manager.on("view_content_has_changed", this, this.check_states_invisible);
        },
        on_click: function () {
            var context = this.build_context().eval();
            if (!_.isUndefined(context.state) && this.is_reject) {
                this.view.reject_state = context.state;
            } else {
                this.view.reject_state = undefined;
            }
            return this._super();
        },
        check_states_invisible: function (attr) {
            attr = 'invisible';
            this.check_states_readonly(attr);
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
            if (!_.isUndefined(this.states_required)) {
                var current_state = this.view.get_field_value('state');
                if (_.contains(this.states_required.split(','), current_state)) {
                    result = true;
                }
                if (!_.isUndefined(this.view.reject_state)) {
                    result = _.contains(this.states_required.split(','), this.view.reject_state);
                }
            }
            return result;
        },
        _set_required: function () {
            this.$el.toggleClass('oe_form_required', this.is_states_required() || this.get("required"));
        }
    });

    instance.web.form.FormWidget.include({
        init: function (field_manager, node) {
            this._super(field_manager, node);
            this.states_editable = this.node.attrs.states_editable;
            this.field_manager.on("view_content_has_changed", this, this.check_states_readonly);
        },
        renderElement: function () {
            this.check_states_readonly();
            this._super();
        },
        check_states_readonly: function (attr) {
            var self = this;
            if (_.isUndefined(attr)) {
                attr = 'readonly';
            }
            if (!_.isUndefined(this.states_editable)) {
                var current_state = this.view.get_field_value('state');
                var states_map = py.eval(this.states_editable, this.field_manager.build_eval_context().eval());
                if (_.has(states_map, current_state)) {
                    var current_state_setting = states_map[current_state];
                    if (current_state_setting == false) {
                        this.set(attr, false);
                    }
                    if (_.has(current_state_setting, 'groups')) {
                        new instance.web.DataSetSearch(this, 'res.users', this.session.user_context, [
                            ['id', '=', this.session.uid], ['groups_id', 'in', current_state_setting.groups]
                        ]).read_slice(['id']).done(function (result) {
                                if (!_.isEmpty(result)) {
                                    self.set(attr, false);
                                } else {
                                    self.set(attr, true);
                                }
                            });
                    }
                    if (_.has(current_state_setting, 'users')) {
                        _.each(current_state_setting.users, function (user) {
                            if (user instanceof Array) {
                                if (_.contains(user[0][2], self.session.uid)) {
                                    self.set(attr, false);
                                } else {
                                    self.set(attr, true);
                                }
                            } else {
                                if (user == self.session.uid) {
                                    self.set(attr, false);
                                } else {
                                    self.set(attr, true);
                                }
                            }
                        });
                    }
                } else {
                    self.set(attr, true);
                }
            }
        }
    });


};
