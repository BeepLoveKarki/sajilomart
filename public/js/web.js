let num=4;

$(document).ready(()=>{
  let d=localStorage.getItem("index");
  if(!d){
    show(1); 
  }else{
    show(d); 
  }
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

function getusers(){
  $.get("/allusers").then ((res,status)=>{
    console.log(res);
  });
}

function logout(){
  window.location.href="/logout";
}

function modal(txt){
  $("#txt").text(txt);
  $(".simplemodal").modal('show');
}