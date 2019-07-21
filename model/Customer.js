let mongoose=require('mongoose');
let bcrypt=require('bcryptjs');
let mongooseFieldEncryption = require("mongoose-field-encryption").fieldEncryption;
let enc=require('../enc-dec');

let CustomerSchema=mongoose.Schema({
	name:String,
	email:{
		type:String,
		unique:true
	},
	address:{
		type:String
	},
	number:{
		type:String,
		unique:true
	},
	password:{
		type:String
	},
    createdDate:{
        type:Date,
        default:Date.now()
    },
	goods:{
	   type:String,
	   default:""
	}
});

CustomerSchema.pre('save',function(next){  
  if (this.isModified('password')){
    bcrypt.genSalt(10,(err,salt)=>{
      bcrypt.hash(this.password,salt,(err,hash)=>{
        this.password=hash;
		next();
      });
    });
  }else{
    next();
  }
});


CustomerSchema.plugin(mongooseFieldEncryption, { fields: ["name","email","address","number","password","createdDate","goods"], secret: enc.decrypt(process.env.database_key) });

let Customer=mongoose.model('Customer',CustomerSchema)


module.exports = Customer;