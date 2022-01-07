// Used to toggle the menu on small screens when clicking on the menu button
function myFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
      x.className += " w3-show";
    } else {
      x.className = x.className.replace(" w3-show", "");
    }
}



function addModal() {
  $("body").append(`
  <div class="modal fade" id="mainModal" tabindex="-1" aria-labelledby="mainModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="mainModalTitle"></h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
      <div id="mainModalBody" class="modal-body">
      </div>
        <div class="modal-footer">
        <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
`);
}


function checkVideo(){
  //get the element
  input_value = document.getElementById("inputGroupFile04")
  //get the first element in files and check its type
  file_type = input_value.files[0].type
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
}
