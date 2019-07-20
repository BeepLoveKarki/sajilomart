let mongoose=require('mongoose');
let bcrypt=require('bcryptjs');
let mongooseFieldEncryption = require("mongoose-field-encryption").fieldEncryption;
let enc=require('../enc-dec');

let UserSchema=mongoose.Schema({
	name:String,
	email:{
		type:String,
		unique:true,
		required:true
	},
	password:{
		required:true,
		type:String
	},
    createdDate:{
        type:Date,
        default:Date.now()
    },
});


UserSchema.pre('save',function(next){  
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



UserSchema.plugin(mongooseFieldEncryption, { fields: ["name","email","password","createdDate"], secret: enc.decrypt(process.env.database_key) });

let User=mongoose.model('User',UserSchema)


module.exports = User;
