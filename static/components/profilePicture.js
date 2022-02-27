class ProfilePicture extends React.Component {
    constructor(props) {
    super(props);
    const username = document.getElementById("profileUsername").innerHTML;
    this.state = {
        profileBool: "",
        username: username,
        source: ""
    }
}


componentDidMount() {
// Simple GET request using fetch
fetch(`/get_profile_picture/${this.state.username}`)
    .then(response => response.json())
    .then(data => {
        if (data == false) {
            this.setState({
                source :"./static/assets/default_picture.jpg"
            })
        }
        else {
            this.setState({
                source: `https://d32dcw9m3mntm7.cloudfront.net/profile_picture/${this.state.username}`
            })
        }
    })
}




render() {
    return (
        <div>
            <img id="UserProfilePicture" src={this.state.source}></img>
        </div>
        );
    }
}
ReactDOM.render(<ProfilePicture/>, document.querySelector("#profilePictureComponent"));