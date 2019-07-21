let num=6;

$(document).ready(()=>{
  let d=localStorage.getItem("index");
  if(!d){
    show(1); 
  }else{
    show(d); 
  }
  
 setTimeout(()=>{
  getcustomers()
 },1000);
 
 setInterval(()=>{
  getcustomers()
 },5000);
  
});


function show(a){
  $("#n"+a.toString()).addClass("active");
  $("#a"+a.toString()).show();
  localStorage.setItem("index",a);
  for(let i=1;i<=num;i++){
     if(i!=a){
	   $("#n"+i.toString()).removeClass("active");
	   $("#a"+i.toString()).hide();
	 }
  }
}

function getcustomers(){
  $.get("/getcustomers").then ((res,status)=>{
    $(".udata").empty();
    if(res["data"]){
	  $(".udata").append("<tr><td colspan=\"6\" class=\"text-center\"><h5>No any customers found</h5></td></tr>");
	}else{		
	 res.customer.forEach((val,index)=>{
	  $(".udata").append("<tr>\
	  <td>"+(index+1).toString()+"</td>\
	  <td>"+val["name"]+"</td>\
	  <td>"+val["address"]+"</td>\
	  <td>"+val["number"]+"</td>\
	  <td>"+val["email"]+"</td>\
	  <td><i onclick=\"iedit('"+val["_id"]+"')\" class=\"fa fa-edit fa-2x\"></i><i onclick=\"modal2('"+val["_id"]+"')\" class=\"fa fa-trash fa-2x\"></i></td>\
	  </tr>");
	 });
    }
  });
}

function logout(){
  window.location.href="/logout";
}

function modal(txt){
  $("#txt").text(txt);
  $(".simplemodal").modal('show');
}

let did;
function modal2(id){
 did=id;
 $(".custdmodal").modal('show');
}

function deletecustomer(){
 $.post("/deletecustomer",{id:did}).then((res,status)=>{
    if(res.status=="done"){
	  $(".custdmodal").modal('hide');
	  modal("Customer successfully deleted");
	  getcustomers();
	}
 });
}

function addGood(){
   $(".goodmodal").modal('show');
}
