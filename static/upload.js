
function checkVideo(){
    //get the element
    input_value = document.getElementById("inputVideoFile")
    //get the first element in files and check its type
    video_file = input_value.files[0]
    file_type = video_file.type
    //if file type is not video
    //then create a message that tells the user invalid file type

    //get file size
    //convert to mb
    const file_size = video_file.size/1000000

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


    if (file_size > 100) {
      input_value.value = ""
      //create element modal
      addModal()
      modal = document.getElementById("mainModal")
      document.getElementById("mainModalTitle").innerHTML = "File Size Limit"
      document.getElementById("mainModalBody").innerHTML = "File exceeds 100 MB"
      $('#mainModal').modal({ show: false})
      $('#mainModal').modal('show');
      //delete element
      $('#mainModal').remove()
    }



    else {
      //check file size
      //read video and play video in frame
      //get the frame element
      //video = document.getElementById("demoVideo")
      //change the frame element source and title
      $("#demoVideo").attr("src", URL.createObjectURL(video_file))
      document.getElementById("demoVideo").play()
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

  function checkImage(){
    //get the element
    input_value = document.getElementById("inputVideoThumbnail")
    //get the first element in files and check its type
    image_file = input_value.files[0]
    file_type = image_file.type
    //if file type is not an image
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
    //get the thumbnail display element
    thumbnailDisplay = document.getElementById("thumbnailImage")
    //create an object url for image and attach as src for display
    thumbnailDisplay.src = URL.createObjectURL(image_file)

  }


  function get_metadata() {
    //autofill video name
    trimmed_name = video_file.name.split('.').slice(0, -1).join('.')
    //durationdocument.getElementById("inputVideoName").value = video_file.name;
    document.getElementById("inputVideoName").value = trimmed_name;
    //autofill length
    video = document.getElementById("demoVideo")
    videoLength = Math.round(video.duration)
    document.getElementById("inputVideoLength").value = videoLength;
    //autofill video quality data
    document.getElementById("inputVideoHeight").value = video.videoHeight;
    document.getElementById("inputVideoWidth").value = video.videoWidth;
  }


  function progressBarMove() {
    var progress = 0;
    if (progress == 0) {
      progress = 1
      progress_bar = document.getElementById("myBar")
      //show progress bar modal
      progress_div = document.getElementById("progressBarDiv");
      progress_div.style.display = "block";
      var width = 10
      var id = setInterval(frame, 50)
      function frame() {
        if (width >= 100) {
          clearInterval(id);
          i = 0;
        } else {
          width++;
          progress_bar.style.width = width + "%";
          progress_bar.innerHTML = width + "%";
        }
      }
    }
  }

  function blockInput() {
    var input_btn = document.getElementById("inputGroupFileAddon04");
    input_btn.disabled = true;
  }


  function submitCheck() {
    //go to start of page
    window.scrollTo(0, 0);
    //block input buttons
    blockInput()
    //add progress bar
    progressModal = new bootstrap.Modal(document.getElementById('progressBarDiv'))
    progressModal.show()
    progressBarMove()
  }





