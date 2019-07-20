  let vid;
  let socket = io();
  
  socket.on('data', function (data) {
	if(data["state"]=="on"){
	  if(!document.querySelector('#videoElement').srcObject){
	    start();
      }
	}else{
	   stop();
	}
   });
   
   socket.on('state',function(data){
	 data["state"].forEach((val,index)=>{
	   if(val==true){
	     $("#s"+(index+1).toString()).html("Active");
	   }else{
	     $("#s"+(index+1).toString()).html("Inactive");
	   }
	 });
   });
   
   socket.on('sensor', function (data) {
     $(".sensors").empty();
	 let f=data["sensors"];
	 f["name"].forEach((val,index)=>{
	   if(f["state"][index]==true){
	     f["state"][index]="Active";
	   }else{
	     f["state"][index]="Inactive";
	   }
	   $(".sensors").append("<tr id=\"m"+(index+1).toString()+"\"><td>"+(index+1).toString()+"</td><td>"+val+"</td><td>"+f["location"][index]+"</td><td>"+f["state"][index]+"</td></tr>");
	 });
   });
   
   setTimeout(()=>{
     socket.emit("sensors");
   },1000);
   
   setInterval(()=>{
      socket.emit("sensors");
   },30000);
	
  
  function start(){
    let video = document.getElementById('videoElement');
    if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
	  localStream=stream;
      video.srcObject = stream;
    })
    .catch(function (error) {
      alert("Something went wrong!");
    });
    }
  }
  
  function stop(){
    let videoEl = document.getElementById('videoElement');
    stream = videoEl.srcObject;
	if(stream){
	 tracks = stream.getTracks();
     tracks.forEach(function(track) {
          track.stop();
      });
	}
	videoEl.srcObject=null;
  }