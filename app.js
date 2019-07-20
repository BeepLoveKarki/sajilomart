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

/*let device = awsIot.device({
   keyPath: 'credentials/1a2da9790c-certificate.pem.key',
  certPath: 'credentials/1a2da9790c-certificate.pem.crt',
    caPath: 'credentials/root-CA.crt',
  clientId: 'sajilomart',
      host: 'a1dwqhuuo6ioox-ats.iot.us-east-1.amazonaws.com'
});*/


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

app.post('/customerregister',(req,res)=>{
  
  
  Customer.find().exec(function (err,customer) {

   let a=0;
   if(customer.length!=0){
    for(let i=0;i<customer.length;i++){
     if(customer[i].email==req.body.email){
      a=1;
	  break;
     }
	 if(customer[i].number==req.body.number){
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
	
});

function savecustomer(req,res){
 
  let customer=new Customer({
    name:req.body.name,
	email:req.body.email,
	address:req.body.address,
	number:req.body.number,
	password:req.body.password
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