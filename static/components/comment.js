class CommentBoxRender extends React.Component {
    constructor(props) {
    super(props);

    this.state = {
            value: "",
            rows: "1",
            disable_text: true,
            class: "",
            classValue: "w-50"
        }
    this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.setState({value: event.target.value});
        this.setState({rows: "3"})
        this.setState({disable_text:false});
        this.setState({class: "btn btn-primary"})
        this.setState({classValue: "w-75"})
    }

    render() {
            return (
            <div>
                <textarea id="commentBox" className={this.state.classValue} placeholder="Add a public comment" value={this.state.value} onChange={this.handleChange} rows={this.state.rows} aria-label="With textarea"></textarea>
                <br />
                <button disabled={this.state.disable_text} className={this.state.class} onClick={submitComment}>comment</button>
            </div>
            );
        }
    }
ReactDOM.render(<CommentBoxRender/>, document.querySelector("#displayCommentBox"));