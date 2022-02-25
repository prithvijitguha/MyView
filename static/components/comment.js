class CommentBoxRender extends React.Component {
    constructor(props) {
    super(props);

    this.state = {
            value: "",
            rows: "1",
            disable_text: true,
            class: ""
        }
    this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState({value: event.target.value});
        this.setState({rows: "3"})
        this.setState({disable_text:false});
        this.setState({classValue: "btn btn-primary"})
    }

    render() {
            return (
            <div>
                <textarea id="commentBox" placeholder="Add a public comment" value={this.state.value} onChange={this.handleChange} rows={this.state.rows} aria-label="With textarea"></textarea>
                <br />
                <button disabled={this.state.disable_text} className={this.state.classValue} onClick={submitComment}>comment</button>
            </div>
            );
        }
    }
ReactDOM.render(<CommentBoxRender/>, document.querySelector("#displayCommentBox"));