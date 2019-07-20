  let vid;
  
  start();
  
  let WS_URL = 'ws://localhost:8081';
  let FPS = 50;
  let ws = new WebSocket(WS_URL);
  let video = document.getElementById('videoElement');

  let getFrame = (video) => {
      let canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      let data = canvas.toDataURL('image/png');
      return data;
   };
  
  function start(){
    if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
	  localStream=stream;
      video.srcObject = stream;
	  //streamit(video);
    })
    .catch(function (error) {
      alert("Some unknown error");
    });
    }
  }

  
    
   ws.onopen = () => {
      console.log(`Connected to ${WS_URL}`);
      setInterval(() => {
         ws.send(getFrame(video));
      }, 1000 / FPS);
    }
  
  function stop(){
    stream = video.srcObject;
	if(stream){
	 tracks = stream.getTracks();
     tracks.forEach(function(track) {
          track.stop();
      });
	}
	video.srcObject=null;
  }