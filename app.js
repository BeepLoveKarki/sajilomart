let fastify = require('fastify');
let app = fastify();
let cors = require('cors');
let helmet = require('fastify-helmet');
let serveStatic = require('serve-static');
let pow = require('point-of-view');
let ejs = require('ejs');
let mongoose = require('mongoose');
let bcrypt = require('bcryptjs');
let bodyParser = require('body-parser');
let awsIot = require('aws-iot-device-sdk');
let io = require('socket.io')(app.server);
let cmd=require('node-cmd');
let enc = require('./enc-dec');
let WebSocket = require('ws');
let AWS = require('aws-sdk');
let fs = require('fs-extra');
let path = require('path');
let asynca = require("async");


require('dotenv').config();

app.use(serveStatic(__dirname+'/public'));
app.register(require('fastify-formbody'))
app.register(helmet);
app.register(pow,{
  engine:{ejs},
  templates:'views'
});

let fastifySession = require('fastify-session');
let fastifyCookie = require('fastify-cookie');
let fileUpload = require('fastify-file-upload');

let User = require('./model/User');
let Customer = require('./model/Customer');
let Good = require('./model/Goods');
 
app.register(fileUpload);
app.register(fastifyCookie);
let MongoDBStore = require('connect-mongodb-session')(fastifySession);


let store = new MongoDBStore({
  uri: 'mongodb://localhost:27017/Ssessions',
  collection: 'Sessions'
});


app.register(fastifySession, {
	secret: enc.decrypt(process.env.session_key),
	store:store,
	cookie:{
		path:"/",
		maxAge:60*60*60*1000,
		saveUninitialized:false,
		httpOnly:true,
		secure:false,
		resave:false
	}
});

//mongoose.connect('mongodb://uname:pwd@157.230.104.253:27017/pir',{useNewUrlParser:true,useCreateIndex:true})
mongoose.connect('mongodb://localhost:27017/sajilomart',{useNewUrlParser:true,useCreateIndex:true})

let device = awsIot.device({
   keyPath: 'credentials/1a2da9790c-private.pem.key',
  certPath: 'credentials/1a2da9790c-certificate.pem.crt',
    caPath: 'credentials/root-CA.crt',
  clientId: 'sajilomart',
      host: 'a1dwqhuuo6ioox-ats.iot.us-east-1.amazonaws.com'
});

device.on('connect', function() {
	device.subscribe("rfid");
});

device.on("error",function(err){
});
 
device.on("message",function(topic,payload){
   let data=JSON.parse(payload.toString());
   console.log(data);
});


/*Web part*/
app.get("/",(req,res)=>{
  
  if(!req.session.user){
      res.view("login.ejs");
  }else{
	 User.find().exec(function (err,user) {
	  let users;
	  for(let i=0;i<user.length;i++){
	   if(user[i].email==req.session.user){
		   users=user[i];
		   break;
		}
       }
	   res.view('web.ejs',{user:users});
	 });
  }
  
});


app.post('/register',(req,res)=>{

  let user=new User({
	 name:req.body.name,
	 email:req.body.email,
	 password:req.body.password
   });
	
  if(req.body.secret==enc.decrypt(process.env.register_key)){
	  
	user.save().then((doc,err)=>{
	  res.send({status:"done"});
	});
	
  }else{
    res.send({status:"error"});
  }
	
});



app.get('/getcustomers',(req,res)=>{
  
  Customer.find().exec(function (err,customer) {
   if(customer.length!=0){
	 res.send({customer});
   }else{
     res.send({data:"none"});
   }
  });
	
});

app.post('/deletecustomer',(req,res)=>{
  
  Customer.findOneAndDelete({'_id':req.body.id}).exec(function (err,status) {
    res.send({status:"done"});
  });
	
});

app.get('/getgoods',(req,res)=>{
  
  Good.find().exec(function (err,good) {
   if(good.length!=0){
	 res.send({good});
   }else{
     res.send({data:"none"});
   }
  });
	
});

app.post('/deletegood',(req,res)=>{
  
  Good.findOneAndDelete({'_id':req.body.id}).exec(function (err,status) {
    res.send({status:"done"});
  });
	
});

app.post("/addgood",(req,res)=>{

 let files = req.raw.files;
 let buffer=new Buffer.from(files["image"]["data"],'base64');
 let filepath="./public/uploads/"+req.raw.body.type+"/"+req.raw.body.name+".png";
 let path="./public/uploads/"+req.raw.body.type;
 
 fs.mkdir(path,{recursive:true},(err1)=>{
	
	fs.writeFile(filepath, buffer, (err2)=>{
	   cmd.get('aws s3 mv '+filepath+'  s3://sajilomart-goods/'+req.raw.body.type+'/', function(err3, data, stderr){
			fs.remove(path, (err4)=>{
			   goods(req,res);
			});
       });
	});
 });
 
});

function goods(req,res){
  
  let good=new Good({
    name:req.raw.body.name,
	type:req.raw.body.type,
	price:req.raw.body.price,
	tag:req.raw.body.tag
 });
	
 good.save().then((doc,err)=>{
	  res.send({status:"done"});
 });
 
}

app.post('/customerregister',(req,res)=>{
  
  let files = req.raw.files;
  let buffers=new Array(),paths=new Array(),result=new Array();
  files["image"].forEach((val,index)=>{
     buffers.push(new Buffer.from(val.data,'base64'));
	 paths.push('./public/uploads/'+req.raw.body.email+'/'+(index+1).toString()+'.png');
	 result.push(function(callback){
        fs.writeFile(paths[index], buffers[index], callback);
     });
  });
  
  let dir='./public/uploads/'+req.raw.body.email;
  fs.mkdir('./public/uploads/'+req.raw.body.email,{recursive:true},(err)=>{
    asynca.parallel(result,function(err, results){
		  cmd.get('aws s3 mv '+dir+'/ s3://sajilomart/'+req.raw.body.email+'/ --recursive', function(err, data, stderr){
			fs.remove(dir, (err)=>{
			   customerbridge(req,res);
			});
          });
    });
  });
});

function customerbridge(req,res){
  Customer.find().exec(function (err,customer) {

   let a=0;
   if(customer.length!=0){
    for(let i=0;i<customer.length;i++){
     if(customer[i].email==req.raw.body.email){
      a=1;
	  break;
     }
	 if(customer[i].number==req.raw.body.number){
	  a=2;
	  break;
	 }
    }
  }
  
  if(a==1){
    res.send({status:"emailalready"});
   }else if(a==2){
    res.send({status:"phonealready"});
  }else{
    savecustomer(req,res);
  }
  
 });
}

app.post("/customerlogin",(req,res)=>{
   
   Customer.find().exec(function (err,customer) {
   
   let cust, a=0;
   for(let i=0;i<customer.length;i++){
	   if(customer[i].email==req.body.email){
		   cust=customer[i];
		   a=1;
		   break;
		}
    }
	
	if(a==1){
	  bcrypt.compare(req.body.password,cust["password"],function(err,result){  
       if(result==true){
		 res.send({status:"done",data:cust});
	   }else{
		 res.send({status:"nopassword"});
	   }
	  });
	}else{
	  res.send({status:"nousername"});
	}
     
   });
   
});

function savecustomer(req,res){

  let customer=new Customer({
    name:req.raw.body.name,
	email:req.raw.body.email,
	address:req.raw.body.address,
	number:req.raw.body.number,
	password:req.raw.body.password
   });
	
   customer.save().then((doc,err)=>{
	  res.send({status:"done"});
   });

}

app.post("/login",(req,res)=>{
 User.find().exec(function (err,user) {
   
   let pwd;
   for(let i=0;i<user.length;i++){
	   if(user[i].email==req.body.email){
		   pwd=user[i].password;
		   break;
		}
    }
    
    bcrypt.compare(req.body.password,pwd,function(err,result){  
	  if(result==true){
        req.session.user = req.body.email;
       }
       res.redirect("/");
	 });
     
   
  });
  
});

app.get('/logout', (req, res) => {
   if(req.session.user){
     req.session.user=null;
   }
   res.redirect("/");
});



app.listen(8080,'0.0.0.0');