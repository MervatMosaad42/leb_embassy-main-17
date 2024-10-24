//odoo.define('ebs_qsheild_mod.backend',[],  function (require) {
//'use strict';
//
////BY Comment by Mervat: basic fields and AbstractFieldBinary not in odoo 17
//
//	var basic_fields = require('web.basic_fields');
//
//	console.log('aaaaaaaaaaaaaaaaaaaaaaaaa');
//
//	basic_fields.AbstractFieldBinary.include({
//		init: function (parent, name, record) {
//			console.log('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb');
//	        this._super.apply(this, arguments);
//	        this.max_upload_size = 50 * 1024 * 1024; // 25Mo
//	    },
//	})
//
//});