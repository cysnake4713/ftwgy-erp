openerp.class_notify = function (instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.web.tree = instance.web.tree || {};

    instance.web.tree.Date = instance.web.DateWidget.extend({
        name: 'a'
    });

    instance.web.class_notify = instance.web.class_notify || {};

    instance.web.views.add('school_plan_quick', 'instance.class_notify.QuickSearchListView');
    instance.class_notify.QuickSearchListView = instance.web.ListView.extend({
        init: function () {
            this._super.apply(this, arguments);
            this.journals = [];
            this.periods = [];
            this.start_date = null;
        },
        start: function () {
            var tmp = this._super.apply(this, arguments);
            var self = this;
            var defs = [];
            this.$el.parent().prepend(QWeb.render("SchoolTimetablePlanQuick", {widget: this}));
            this.date_picker = new instance.web.DateWidget(this);
            this.date_picker.on('datetime_changed', this, _.bind(function () {
                self.start_date = this.value === '' ? null : this.date_picker.get_value();
                self.do_search(self.last_domain, self.last_context, self.last_group_by);
            }, this));
            this.date_picker.appendTo(this.$el.parent().find('div.oe_start_date_picker'));

            return tmp;
        },
        do_search: function (domain, context, group_by) {
            var self = this;
            this.last_domain = domain;
            this.last_context = context;
            this.last_group_by = group_by;
            this.old_search = _.bind(this._super, this);
            return self.search_by_start_date();
        },
        search_by_start_date: function () {
            var self = this;
            var domain = [];
            if (self.start_date !== null) domain.push(["start_date", "=", self.start_date]);
            var compound_domain = new instance.web.CompoundDomain(self.last_domain, domain);
            self.dataset.domain = compound_domain.eval();
            return self.old_search(compound_domain, self.last_context, self.last_group_by);
        }
    });
};
