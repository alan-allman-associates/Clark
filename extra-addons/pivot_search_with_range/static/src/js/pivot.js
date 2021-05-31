odoo.define('pivot_search_with_range.pivot', function (require) {
"use strict";

var time        = require('web.time');
var core        = require('web.core');
var data        = require('web.data');
var session     = require('web.session');
var utils       = require('web.utils');
var PivotView   = require('web.PivotView');
var datepicker  = require('web.datepicker');
var SearchView  = require('web.SearchView');
var rpc = require('web.rpc');


var _t = core._t;
var _lt = core._lt;
var QWeb = core.qweb;

SearchView.include({
    build_search_data: function (noDomainEvaluation) {
        var res = this._super(noDomainEvaluation);
        // console.log(this.tm723_domain);
        if (this.search_domain){
            res.domains = res.domains.concat(this.search_domain || [[]]);
        }
        return res;
    },
});

PivotView.include({

    init: function() {
        this._super.apply(this, arguments);
        this.ts_fields = [];
    },

    tgl_on_button_click: function (event) {
        var self = this;
        var $target = $(event.target),
            field, key, first_item;

        field   = $target.parent().data('field');
        key     = $target.parent().data('key');

        if (field == -1) {
            first_item = $target.parent().parent().children('.tgl_first_item.selected');
            if (!first_item.length) {
                $target.parent().parent().children('li').removeClass('selected')
            }
        } else {
            first_item = $target.parent().parent().children('.tgl_first_item').removeClass('selected');
        }

        $target.parent().toggleClass('selected');
        this.search_by_range();
        event.stopPropagation();

    },

});


var PivotController      = require('web.PivotController');

PivotController.include({

    do_search: function(domain, context, group_by) {
        var self = this;
        this.last_domain = domain;
        this.last_context = context;
        this.last_group_by = group_by;
        this.last_search = _.bind(this._super, this);
        return self.search_by_range();
    },

    js_date: function (now) {
        //format: yyyyMMddhhmmss
	    var year = "" + now.getFullYear();
	    var month = "" + (now.getMonth() + 1); if (month.length == 1) { month = "0" + month; }
	    var day = "" + now.getDate(); if (day.length == 1) { day = "0" + day; }
	    var hour = "" + now.getHours(); if (hour.length == 1) { hour = "0" + hour; }
	    var minute = "" + now.getMinutes(); if (minute.length == 1) { minute = "0" + minute; }
	    var second = "" + now.getSeconds(); if (second.length == 1) { second = "0" + second; }
	    return year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second;
    },

    search_by_range: function() {
        var self = this;
        var searchview = self.searchView
        searchview.search_domain = []
        var domain = [], value, value_tmp;

        if (self.$search_date) {
            var start_date  = self.$search_date.find('.field_start_date').val(),
                end_date    = self.$search_date.find('.field_end_date').val();

            var l10n = _t.database.parameters;
            var time_string = time.strftime_to_moment_format(l10n.date_format + " " + l10n.time_format);
            if (start_date) {
                var d = moment(start_date, time_string).toDate();
                var nowUtc = new Date( d.getTime() + (d.getTimezoneOffset() * 60000));
                start_date = self.js_date(nowUtc);
                searchview.search_domain.push([['date_closed', '>=', start_date]]);
            }
            if (end_date) {
                var d = moment(end_date, time_string).toDate();
                var nowUtc = new Date( d.getTime() + ((d.getTimezoneOffset() + (24 * 60)) * 60000));
                end_date = self.js_date(nowUtc);
                searchview.search_domain.push([['date_closed', '<=', end_date]]);
            }

        }

        if (self.$search_int_axe1) {
            var start_int  = self.$search_int_axe1.find('.input_field_axe1').val();
            if (start_int) {
                searchview.search_domain.push([['axe1', '=', parseInt(start_int)]]);
            }
        }
        if (self.$search_int_axe2) {
            var start_int  = self.$search_int_axe2.find('.input_field_axe2').val();
            if (start_int) {
                searchview.search_domain.push([['axe2', '=', parseInt(start_int)]]);
            }
        }
        if (self.$search_int_axe3) {
            var start_int  = self.$search_int_axe3.find('.input_field_axe3').val();
            if (start_int) {
                searchview.search_domain.push([['axe3', '=', parseInt(start_int)]]);
            }
        }
        if (self.$search_int_axe4) {
            var start_int  = self.$search_int_axe4.find('.input_field_axe4').val();
            if (start_int) {
                searchview.search_domain.push([['axe4', '=', parseInt(start_int)]]);
            }
        }
         if (self.$search_int_company) {
            var start_int  = self.$search_int_company.find('.input_field_company').val();
            if (start_int) {
                searchview.search_domain.push([['company_id', '=', parseInt(start_int)]]);
            }
        }
        if (self.$search_int_partner) {
            var start_int  = self.$search_int_partner.find('.input_field_partner').val();
            if (start_int) {
                searchview.search_domain.push(['|',['parent_id', '=', parseInt(start_int)],['partner_id', '=', parseInt(start_int)]]);
            }
        }
        self.searchView.query.trigger('reset');
        return true;
    },



    get_data: function() {
        var l10n = _t.database.parameters;
        var datepickers_options = {
                minDate: moment({ y: 1900 }),
                maxDate: moment({ y: 9999, M: 11, d: 31 }),
                calendarWeeks: true,
                icons : {
                    time: 'fa fa-clock-o',
                    date: 'fa fa-calendar',
                    next: 'fa fa-chevron-right',
                    previous: 'fa fa-chevron-left',
                    up: 'fa fa-chevron-up',
                    down: 'fa fa-chevron-down',
                   },
                locale : moment.locale(),
                format : time.getLangDatetimeFormat(),
            };
        return datepickers_options;
    },


        do_clear: function () {
        var self = this;
        if ($(document)){
            self.$search_date.find('.field_start_date').val('');
            self.$search_date.find('.field_end_date').val('');
            self.$search_int_axe1.find('#id_input_field_axe1').val('');
            self.$search_int_axe2.find('#id_input_field_axe2').val('');
            self.$search_int_axe3.find('#id_input_field_axe3').val('');
            self.$search_int_axe4.find('#id_input_field_axe4').val('');
            if (self.$search_int_company) {
             self.$search_int_company.find('#id_input_field_company').val('');
            }
            if (self.$search_int_partner){
             self.$search_int_partner.find('#id_input_field_partner').val('');
            }
        }
        return self.search_by_range();
    },


    renderButtons: function ($node) {
     var self = this;
        var state = self.model.get(self.handle, {raw: true});
        var context = state.context || false;
        this._super.apply(this, arguments);
         var l10n = _t.database.parameters;
         self.values_field = []
        var datepickers_options = {
            pickTime: false,
            startDate: moment({ y: 1900 }),
            endDate: moment().add(200, "y"),
            calendarWeeks: true,
            icons : {
                time: 'fa fa-clock-o',
                date: 'fa fa-calendar',
                up: 'fa fa-chevron-up',
                down: 'fa fa-chevron-down'
               },
            language : moment.locale(),
            format : time.strftime_to_moment_format(l10n.date_format),
        }
        if ((context && context.add_company) || (context && context.add_partner)){
         self.$formule_calcul = $(QWeb.render('formule_calcul', {}))
         self.$formule_calcul.appendTo($node);
         }
        // company
        if (context && context.add_company){
           var res = rpc.query({
            model: 'res.company',
            method: 'search_company_read',
            args: ['', []],
            /* args: args */
        }).then(function (result) {
         var values_field = [];
        _.each(result, function(elment, id, list){
            if (elment.name && elment.id) {
                values_field.push([elment.id, elment.name]);
            }
             });
             if (values_field.length > 0) {

           $('select#id_input_field_company').html($(QWeb.render('new_options', {'values_field': values_field})));
         }
            });
         var values_field = [];
         self.$search_int_company = $(QWeb.render('button_for_company', {'values_field': values_field}))
         self.$search_int_company .appendTo($node);
         }

         // partner
        if (context && context.add_partner){
           var res = rpc.query({
            model: 'res.partner',
            method: 'search_read',
            args: [[['parent_id','=',false],['is_company','=',true],['name', 'like','%[%']], ['id', 'name']],
            /* args: args */
        }).then(function (result) {
         var values_field = [];
        _.each(result, function(elment, id, list){
            if (elment.name && elment.id) {
                values_field.push([elment.id, elment.name]);
            }
             });
             if (values_field.length > 0) {

           $('select#id_input_field_partner').html($(QWeb.render('new_options', {'values_field': values_field})));
         }
            });
         var values_field = [];
         self.$search_int_partner = $(QWeb.render('button_for_partner', {'values_field': values_field}))
         self.$search_int_partner.appendTo($node);
         }
        // Date field
         if (context.add_company || context.add_partner){
        self.$search_date = $(QWeb.render('buttons_for_date'))
        self.$search_date.find('.field_start_date').datetimepicker(datepickers_options);
        self.$search_date.find('.field_end_date').datetimepicker(datepickers_options);
        self.$search_date.appendTo($node);

         var res = rpc.query({
            model: 'crm.axes',
            method: 'search_read',
            args: [[['axe_type','=','axe1']], ['id', 'name']],
            /* args: args */
        }).then(function (result) {
         var values_field = [];
        _.each(result, function(elment, id, list){
            if (elment.name && elment.id) {
                values_field.push([elment.id, elment.name]);
            }
             });
             if (values_field.length > 0) {

           $('select#id_input_field_axe1').html($(QWeb.render('new_options', {'values_field': values_field})));
         }
            });
         var values_field = [];
         self.$search_int_axe1 = $(QWeb.render('button_for_axe1', {'values_field': values_field}))
         self.$search_int_axe1.appendTo($node);
            var res = rpc.query({
            model: 'crm.axes',
            method: 'search_read',
            args: [[['axe_type','=','axe2']], ['id', 'name']],
            /* args: args */
        }).then(function (result) {
         var values_field = [];
        _.each(result, function(elment, id, list){
            if (elment.name && elment.id) {
                values_field.push([elment.id, elment.name]);
            }
             });
             if (values_field.length > 0) {

           $('select#id_input_field_axe2').html($(QWeb.render('new_options', {'values_field': values_field})));
         }
            });
         var values_field = [];
         self.$search_int_axe2 = $(QWeb.render('button_for_axe2', {'values_field': values_field}))
         self.$search_int_axe2.appendTo($node);

          var res = rpc.query({
            model: 'crm.axes',
            method: 'search_read',
            args: [[['axe_type','=','axe3']], ['id', 'name']],
            /* args: args */
        }).then(function (result) {
         var values_field = [];
        _.each(result, function(elment, id, list){
            if (elment.name && elment.id) {
                values_field.push([elment.id, elment.name]);
            }
             });
             if (values_field.length > 0) {

           $('select#id_input_field_axe3').html($(QWeb.render('new_options', {'values_field': values_field})));
         }
            });
         var values_field = [];
         self.$search_int_axe3 = $(QWeb.render('button_for_axe3', {'values_field': values_field}))
         self.$search_int_axe3.appendTo($node);

        var res = rpc.query({
            model: 'crm.axes',
            method: 'search_read',
            args: [[['axe_type','=','axe4']], ['id', 'name']],
            /* args: args */
        }).then(function (result) {
         var values_field = [];
        _.each(result, function(elment, id, list){
            if (elment.name && elment.id) {
                values_field.push([elment.id, elment.name]);
            }
             });
             if (values_field.length > 0) {

           $('select#id_input_field_axe4').html($(QWeb.render('new_options', {'values_field': values_field})));
         }
            });
         var values_field = [];
         self.$search_int_axe4 = $(QWeb.render('button_for_axe4', {'values_field': values_field}))
         self.$search_int_axe4.appendTo($node);
         self.$search_int_axe4.find('.search_button').on('click', function() {
            self.search_by_range();
        });
        self.$search_int_axe4.find('.clear_button').on('click', function() {
            self.do_clear();
        });
        }
    },

});
});
