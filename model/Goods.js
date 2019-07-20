let mongoose=require('mongoose');
let bcrypt=require('bcryptjs');
let mongooseFieldEncryption = require("mongoose-field-encryption").fieldEncryption;
let enc=require('../enc-dec');

let GoodSchema=mongoose.Schema({
	name:String,
	type:{
		type:String,
		unique:true
	},
	price:{
		type:String
	},
	tag:{
		type:String,
		unique:true
	},
    createdDate:{
        type:Date,
        default:Date.now()
    }
});


GoodSchema.plugin(mongooseFieldEncryption, { fields: ["name","type","price","tag","createdDate"], secret: enc.decrypt(process.env.database_key) });

let Good=mongoose.model('Good',GoodSchema)

module.exports = Good;
