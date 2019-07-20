let cryptojs = require("crypto-js");

function encrypt(value){
   return cryptojs.AES.encrypt(value,process.env.real_key).toString();
}

function decrypt(value){
  return cryptojs.AES.decrypt(value,process.env.real_key).toString(cryptojs.enc.Utf8);
}


module.exports={
  encrypt:encrypt,
  decrypt:decrypt
}