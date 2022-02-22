function like_unlike() {
    like_button =  document.getElementById("likeButton")
    dislike_button = document.getElementById("dislikeButton")
    video_id = document.getElementById("video_id_hidden").innerHTML
    //make button liked and unlike dislike if liked
    //new bootstrap button
    var bsButton = new bootstrap.Button(like_button)
    //toggle state
    bsButton.toggle()
    // decheck dislike button
    $('#dislikeButton').removeClass('active')
    $('#dislikeButton').prop('checked',false)

    const data = {
        "video_id": video_id,
        };

    fetch('/like', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json', 'Accept': 'application/json'
    },
    body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
    console.log('Success:', data);
    })
    .catch((error) => {
    console.error('Error:', error);
    });
}


function dislike_undislike() {
    dislike_button =  document.getElementById("dislikeButton")
    like_button = document.getElementById("likeButton")
    video_id = document.getElementById("video_id_hidden").innerHTML
    //make button liked and unlike dislike if liked
    //new bootstrap button
    var disBsButton = new bootstrap.Button(dislike_button)
    //toggle state
    disBsButton.toggle()
    //decheck like button
    $('#likeButton').removeClass('active')
    $('#likeButton').prop('checked',false)

    //check the checked property of like button
    if (like_button.checked == true) {
        //set it to false
        like_button.checked = false
    }

    const data = {
        "video_id": video_id,
        };

    fetch('/dislike', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json', 'Accept': 'application/json'
    },
    body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
    console.log('Success:', data);
    })
    .catch((error) => {
    console.error('Error:', error);
    });
}


function submitComment() {
    //get the comment text
    var comment_data = document.getElementById("commentBox").value
    //get video_id
    var video_id = document.getElementById("video_id_hidden").innerHTML
    //fetch request post
    const data = {
        "comment_data": comment_data,
        "video_id": video_id
        };

    fetch('/comment/add', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json', 'Accept': 'application/json'
    },
    body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
    console.log('Success:', data);
    })
    .catch((error) => {
    console.error('Error:', error);
    });
}


function deleteComment(htmlElementId) {
    comment_id = htmlElementId.slice(16)
    const data = comment_id
    //fetch request to delete comment
    fetch('/comment/delete', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json', 'Accept': 'application/json'
        },
        body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
        console.log('Success:', data);
        })
        .catch((error) => {
        console.error('Error:', error);
        });

    //get the parent element and delete it
    parentElement = document.getElementById(htmlElementId)
    parentElement.parentElement.remove()
}