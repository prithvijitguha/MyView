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

function TimeAgo(element) {
  var final = moment(element.innerHTML).fromNow();
  element.innerHTML = final;
}


function Timestamp_Ago() {
  //get all timestamp elements
  var timestampCollection = document.getElementsByClassName("timestamp")
  //convert to array
  var timestampArray = Array.from(timestampCollection)
  //pass to timeago function
  timestampArray.forEach(TimeAgo)

}