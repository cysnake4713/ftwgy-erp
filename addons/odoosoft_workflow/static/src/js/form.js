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

    instance.web.form.FieldMany2ManyMulti = instance.web.form.FieldMany2ManyTags.extend(instance.web.form.CompletionFieldMixinNoLimit, {

        _search_create_popup: function (view, ids, context) {
            var self = this;
            var pop = new instance.web.form.SelectCreatePopup(this);
            pop.select_element(
                self.field.relation,
                {
                    title: (view === 'search' ? _t("Search: ") : _t("Create: ")) + this.string,
                    initial_ids: ids ? _.map(ids, function (x) {
                        return x[0];
                    }) : undefined,
                    initial_view: view,
                    disable_multiple_selection: false
                },
                self.build_domain(),
                new instance.web.CompoundContext(self.build_context(), context || {})
            );
            pop.on("elements_selected", self, function (element_ids) {
                _.each(element_ids, function (element_id) {
                    self.add_id(element_id);
                });
                self.focus();
            });
        },

        get_search_result: function (search_val) {
            var self = this;

            var dataset = new instance.web.DataSet(this, this.field.relation, self.build_context());
            this.last_query = search_val;
            var exclusion_domain = [], ids_blacklist = this.get_search_blacklist();
            if (!_(ids_blacklist).isEmpty()) {
                exclusion_domain.push(['id', 'not in', ids_blacklist]);
            }

            return this.orderer.add(dataset.name_search(
                search_val, new instance.web.CompoundDomain(self.build_domain(), exclusion_domain),
                'ilike', this.limit + 1, self.build_context())).then(function (data) {
                self.last_search = data;
                // possible selections for the m2o
                var values = _.map(data, function (x) {
                    x[1] = x[1].split("\n")[0];
                    return {
                        label: _.str.escapeHTML(x[1]),
                        value: x[1],
                        name: x[1],
                        id: x[0]
                    };
                });

                // search more... if more results that max
                if (values.length > self.limit) {
                    values = values.slice(0, self.limit);
                    values.push({
                        label: _t("Search More..."),
                        action: function () {
                            dataset.name_search(search_val, self.build_domain(), 'ilike').done(function (data) {
                                self._search_create_popup("search", data);
                            });
                        },
                        classname: 'oe_m2o_dropdown_option'
                    });
                }
                // quick create
                var raw_result = _(data.result).map(function (x) {
                    return x[1];
                });
                if (search_val.length > 0 && !_.include(raw_result, search_val) && !(self.options && (self.options.no_create || self.options.no_quick_create))) {
                    values.push({
                        label: _.str.sprintf(_t('Create "<strong>%s</strong>"'),
                            $('<span />').text(search_val).html()),
                        action: function () {
                            self._quick_create(search_val);
                        },
                        classname: 'oe_m2o_dropdown_option'
                    });
                }
                // create...
                if (!(self.options && (self.options.no_create || self.options.no_create_edit))) {
                    values.push({
                        label: _t("Create and Edit..."),
                        action: function () {
                            self._search_create_popup("form", undefined, self._create_context(search_val));
                        },
                        classname: 'oe_m2o_dropdown_option'
                    });
                }
                else if (values.length == 0)
                    values.push({
                        label: _t("No results to show..."),
                        action: function () {
                        },
                        classname: 'oe_m2o_dropdown_option'
                    });

                return values;
            });
        }
    });

    instance.web.form.widgets = instance.web.form.widgets.extend({
        'many2many_tags_multi': 'instance.web.form.FieldMany2ManyMulti'
    });


    //instance.web.form.WidgetApplyButton = instance.web.form.WidgetButton.extend({
    //    init: function (field_manager, node) {
    //        if (!node.attrs.name) {
    //            node.attrs.name = 'common_apply';
    //        }
    //        if (!node.attrs.type) {
    //            node.attrs.type = 'object';
    //        }
    //
    //        this._super(field_manager, node);
    //    }
    //});
    //instance.web.form.tags.add('apply_button', 'instance.web.form.WidgetApplyButton');


};
