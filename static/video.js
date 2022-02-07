function like_unlike() {
    like_button =  document.getElementById("likeButton")
    dislike_button = document.getElementById("dislikeButton")
    video_id = document.getElementById("video_id_hidden").innerHTML
    //check the checked property of dislike button
    if (dislike_button.checked == true) {
        //set it to false
        dislike_button.checked = false
    }

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
    //fetch request to delete comment

    //get the parent element and delete it

}