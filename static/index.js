var start = 0
var end = 6

window.onload = get_top_videos()


function append_new_videos(data_array) {
    //for each element create a video element
    data_array.forEach(create_video_element)
}

function create_video_element(data) {
    rows_html_collection = document.getElementsByClassName("row row-cols-3 mx-auto")
    rows_array = Array.from(rows_html_collection)
    //create class
    main_div = document.createElement("div")
    main_div.setAttribute("class", "mx-auto videoThumbnailContent");
    //create a href element child
    ahref = document.createElement("a");
    ahref.href = `video/${data.video_link}`;

    thumbnail = document.createElement("img")
    thumbnail.setAttribute("class", "img-fluid videoThumbnail")
    thumbnail.setAttribute("src", `https://d32dcw9m3mntm7.cloudfront.net/thumbnail/${data.video_link}`)
    //create image profile pic as child element
    profile_pic = document.createElement("img")
    profile_pic.setAttribute("class", "profilePicture")
    profile_pic_flag = get_profile_pic_bool(data.video_username)
    if (profile_pic_flag == "true") {
        profile_pic.src = `https://d32dcw9m3mntm7.cloudfront.net/profile_picture/${data.video_username}`
    }
    else {
        profile_pic.src = "./static/assets/default_picture.jpg"
    }
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
    ahref.appendChild(thumbnail)
    main_div.appendChild(ahref)
    main_div.appendChild(profile_pic)
    main_div.appendChild(videoName)
    main_div.appendChild(videoUsername)
    main_div.appendChild(view_count)
    main_div.appendChild(timestamp)



    //append it to rows
    rows_array.slice(-1).pop().appendChild(main_div)
}


async function get_profile_pic_bool(username) {
    let response = await fetch(`/get_profile_picture/${username}`);
    let data = await response.text();
    return data;
}


async function get_top_videos() {
    let response = await fetch(`/get_top_videos/${start}/${end}`)
    let data = await response.json()
    append_new_videos(data)
    start = start + end
    end = end + end
}

// If scrolled to bottom, load the next set of videos
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        get_top_videos()
    }
};


