var start = 1
var end = 2



function append_new_videos(data_array) {
    //for each element create a video element
    data_array.forEach(create_video_element)

}

function create_video_element(data) {
    rows_html_collection = document.getElementsByClassName("row row-cols-5 mx-auto")
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
    ahref.appendChild(thumbnail)
    main_div.appendChild(ahref)
    //create image profile pic as child element
    //create video ame
    //create video username
    // create view count
    // create timestamp

    //append it to rows
    rows_array.slice(-1).pop().appendChild(main_div)
}


function get_top_videos() {
    fetch(`/get_top_videos/${start}/${end}`)
    .then(response => response.json())
    .then(data => append_new_videos(data));
    start = start + end
    end = end + end
}

