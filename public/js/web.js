let num=4;

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
  
});


function show(a){
  $("#n"+a.toString()).addClass("active");
  $("#a"+a.toString()).show();
  localStorage.setItem("index",a);
  for(let i=1;i<=4;i++){
     if(i!=a){
	   $("#n"+i.toString()).removeClass("active");
	   $("#a"+i.toString()).hide();
	 }
  }
}

function getcustomers(){
  $.get("/getcustomers").then ((res,status)=>{
    $(".udata").empty();
	res.customer.forEach((val,index)=>{
	  $(".udata").append("<tr>\
	  <td>"+(index+1).toString()+"</td>\
	  <td>"+val["name"]+"</td>\
	  <td>"+val["address"]+"</td>\
	  <td>"+val["number"]+"</td>\
	  <td>"+val["email"]+"</td>\
	  <td><i onclick=\"iedit('"+val["id"]+"')\" class=\"fa fa-edit fa-2x\"></i><i onclick=\"modal2('"+val["id"]+"')\" class=\"fa fa-trash fa-2x\"></i></td>\
	  </tr>");
	});
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
	  modal("Customer successfully deleted");
	  getcustomers();
	}
 });
}