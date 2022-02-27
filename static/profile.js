var start = 0
var end = 5

window.onload = get_uploaded_videos()

async function get_uploaded_videos() {
    const username = document.getElementById("profileUsername").innerHTML;
    let response = await fetch(`/get_uploaded_videos/${username}/${start}/${end}`);
    let data = await response.json();
    append_new_videos(data);
    start = start + end;
    end = end + end;
}

function append_new_videos(data_array) {
    //for each element create a video element
    data_array.forEach(create_video_element)
}

function create_video_element(data) {
    rows_html_collection = document.getElementsByClassName("row justify-content-md-center")
    rows_array = Array.from(rows_html_collection)
    //create column class
    main_div = document.createElement("div")
    main_div.setAttribute("class", "col-xs-1 col-md-4 mx-auto videoContainer");
    //create a href element child
    ahref = document.createElement("a");
    ahref.href = `video/${data.video_link}`;

    // create thumbnail image
    thumbnail = document.createElement("img")
    thumbnail.setAttribute("class", "img-fluid videoThumbnail")
    thumbnail.setAttribute("src", `https://d32dcw9m3mntm7.cloudfront.net/thumbnail/${data.video_link}`)
    //create video name
    videoName = document.createElement("h6")
    videoName.setAttribute("class", "videoName w-100")
    videoName.innerHTML = data.video_name
    //create video username
    videoUsername = document.createElement("p")
    videoUsername.setAttribute("class", "videoUsername")
    videoUsername.innerHTML = data.video_username
    // create view count
    view_count = document.createElement("strong")
    view_count.setAttribute("class", "viewCount")
    view_count.innerHTML = `${data.views} views`
    // create timestamp
    timestamp = document.createElement("h6")
    timestamp.setAttribute("class", "timestamp timestampVideo")
    timestamp.innerHTML = moment(data.ts_upload).fromNow();
    // create video_length
    video_length = document.createElement("p")
    video_length.setAttribute("class", "videoLength")
    video_length.innerHTML = Math.floor(data.length / 60) + ":" + (data.length % 60 ? data.length % 60 : '00')
    // create deleteVideo button
    delete_div = document.createElement("div")
    delete_div.setAttribute("class", "deleteVideoButtonClass")
    delete_button_input = document.createElement("input")
    delete_button_input.setAttribute("type", "button")
    delete_button_input.setAttribute("name", "btnradio")
    delete_button_input.setAttribute("class", "btn-check")
    delete_button_label = document.createElement("label")
    delete_button_label.setAttribute("class", "btn btn-outline-danger deleteCommentButton")
    delete_button_label.setAttribute("id", `videoID${data.video_id}`)
    delete_button_label.setAttribute("onclick", `delete_video(${data.video_id})`)
    //delete_button_label.onclick = delete_video(this)
    delete_button_label.innerHTML = "delete"

    delete_div.appendChild(delete_button_input)
    delete_div.appendChild(delete_button_label)

    //put all elements together
    ahref.appendChild(thumbnail)
    main_div.appendChild(ahref)
    main_div.appendChild(videoName)
    main_div.appendChild(videoUsername)
    main_div.appendChild(view_count)
    main_div.appendChild(timestamp)
    main_div.appendChild(video_length)
    main_div.appendChild(delete_div)
    //append it to rows
    rows_array.slice(-1).pop().appendChild(main_div)
}


function delete_video(video_id) {
    username = document.getElementById("profileUsername").innerHTML;
    data = {
        "username": username,
        "video_id": video_id
    }
    fetch(`/delete_video/${username}/${video_id}`,{
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
    delete_button = document.getElementById(`videoID${video_id}`)
    parent_video = delete_button.parentElement.parentElement
    parent_video.style.opacity = 0
    parent_video.remove()

}


// If scrolled to bottom, load the next set of videos
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        get_uploaded_videos()
    }
};