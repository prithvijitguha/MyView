class LikeDislikeComp extends React.Component {
    constructor(props) {
    super(props);
}
render() {
    return (
        <div className="btn-group" role="group" aria-label="Basic radio toggle button group">
            <input type="radio" className="btn-check" name="btnradio"  autoComplete="off"></input>
            <label className="btn btn-outline-primary" id="likeButton" onClick={like_unlike} htmlFor="btnradio1">👍</label>

            <input type="radio" className="btn-check" name="btnradio" autoComplete="off"></input>
            <label className="btn btn-outline-primary" id="dislikeButton" onClick={dislike_undislike} htmlFor="btnradio2">👎</label>
        </div>
        );
    }
}
ReactDOM.render(<LikeDislikeComp/>, document.querySelector("#likeDislikeDisplay"));