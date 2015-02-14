/**
 * Created by cysnake4713 on 15-2-9.
 */

openerp.mail_send = function (instance) {
    var _t = instance.web._t;

    instance.web.form.FieldMany2ManyTagsEmail.include({


        _search_create_popup: function (view, ids, context) {
            var self = this;
            var pop = new instance.web.form.SelectCreatePopup(this);
            pop.select_element(
                self.field.relation,
                {
                    title: (view === 'search' ? _t("Search: ") : _t("Create: ")) + this.string,
                    initial_ids: ids ? _.map(ids, function (x) {
                        return x[0]
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
        }
    });
};


