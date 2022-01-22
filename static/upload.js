
function checkVideo(){
    //get the element
    input_value = document.getElementById("inputVideoFile")
    //get the first element in files and check its type
    video_file = input_value.files[0]
    file_type = video_file.type
    //if file type is not video
    //then create a message that tells the user invalid file type
    if (!file_type.includes('video')) {
      input_value.value = ""
      //create element modal
      addModal()
      modal = document.getElementById("mainModal")
      document.getElementById("mainModalTitle").innerHTML = "Invalid File Type"
      document.getElementById("mainModalBody").innerHTML = "Only video files accepted"
      $('#mainModal').modal({ show: false})
      $('#mainModal').modal('show');
      //delete element
      $('#mainModal').remove()
      //display alert

      console.log("invalid file type, input reset")
    }

    else {
      //read video and play video in frame
      //get the frame element
      //video = document.getElementById("demoVideo")
      //change the frame element source and title
      $("#demoVideo").attr("src", URL.createObjectURL(video_file))
      document.getElementById("demoVideo").play()

      //enable the capture thumbnail button
      document.getElementById("thumbnailCapturebtn").disabled = false;
      //get video frame
      video = document.getElementById("demoVideo");

      video.addEventListener('loadedmetadata',
        function() {
        // Video is loaded and can be played
        get_metadata()
        },
      );




    }
  }

  function capture(){
    //function to capture thumbnail
    canvas = document.getElementById('thumbnailDisplay');
    video = document.getElementById("demoVideo");
    //get original video dimensions
    canvas.getContext('2d').drawImage(video, 0, 0, video.width, video.height)
    canvas_image = canvas.toDataURL('image/jpeg', 1.0)
    //add video as source for display
    document.getElementById("thumbnailImage").setAttribute("src", canvas_image)
  }

  function checkImage(){
    //get the element
    input_value = document.getElementById("inputVideoThumbnail")
    //get the first element in files and check its type
    image_file = input_value.files[0]
    file_type = image_file.type
    //if file type is not video
    //then create a message that tells the user invalid file type
    if (!file_type.includes('image')) {
      input_value.value = ""
      //create element modal
      addModal()
      modal = document.getElementById("mainModal")
      document.getElementById("mainModalTitle").innerHTML = "Invalid File Type"
      document.getElementById("mainModalBody").innerHTML = "Only Images Accepted"
      $('#mainModal').modal({ show: false})
      $('#mainModal').modal('show');
      //delete element
      $('#mainModal').remove()
      //display alert
      console.log("invalid file type, input reset")
    }
  }




  function get_metadata() {
    //capture first image as thumbnail
    capture()
    //autofill video name
    document.getElementById("inputVideoName").value = video_file.name;
    //autofill length
    video = document.getElementById("demoVideo")
    videoLength = Math.round(video.duration)
    document.getElementById("inputVideoLength").value = videoLength;
    //autofill video quality data
    document.getElementById("inputVideoHeight").value = video.videoHeight;
    document.getElementById("inputVideoWidth").value = video.videoWidth;
  }