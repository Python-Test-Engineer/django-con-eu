<style>
  body {
    background-color: #060606;
    color: white;
    font-family: 'Fira Code', monospace;
    /* Use Fira Code for code blocks */
    font-size: 22px
  }



  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    font-family: 'Raleway', sans-serif;
    /* Use Raleway for headings */
  }

  p,
  span,
  div {
    font-family: 'Raleway', sans-serif;
    /* Use Raleway for body text */
  }

  code,
  pre {
    font-family: 'Fira Code', monospace;
    /* Use Fira Code for code blocks */
  }

  .messages-box {}

  .messages-list {
    padding-left: 0;
  }

  .message {
    margin-bottom: 15px;
    list-style: none;
  }

  .message-text {
    padding: 10px;
    border-radius: 15px;
    border: 2px solid orange;
    color: white;
    background-color: #060606;
  }

  .sent {
    background-color: #060606;
    align-self: flex-end;
  }

  .received {
    background-color: #060606;
    align-self: flex-start;
  }



  input[type="text"] {
    font-family: inherit;
    font-size: 28px;
    width: 100%;
    /* Large input field width */
    height: 60px;
    /* Large input field height */
    background-color: #1f1f1f;
    /* Dark mode background color */
    color: #fff;
    /* White text color */
    border: white 2px solid;
    border-radius: 20px;
    /* Rounded corners */

    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  }

  input[type="text"]::-webkit-input-placeholder {
    font-size: 22px;
    padding: left 10px;
  }

  input[type="text"]:-moz-placeholder {
    font-size: 22px;
    padding: left 10px;
  }

  input[type="text"]::-moz-placeholder {
    font-size: 22px;
    padding: left 10px;
  }

  input[type="text"]:-ms-input-placeholder {
    font-size: 22px;
    padding: left 10px;
  }

  input[type="text"]:focus {
    outline: none;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }

  button {
    width: 200px;
    /* Large button width */
    height: 50px;
    /* Large button height */
    background-color: #FFA500;
    /* Orange background color */
    color: #fff;
    /* White text color */
    border: none;
    border-radius: 10px;
    /* Rounded corners */
    font-size: 24px;
    cursor: pointer;
    margin-top: 30px;
  }

  button:hover {
    background-color: #e09943;
    /* Darker orange background color on hover */
  }

  button:active {
    background-color: #FFA500;
    /* Lighter orange background color on active */
  }

  .chat-container {
    width: 800px;
    margin: 0 auto;
    background-color: #1f1f1f;
    /* Dark mode background color */
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  }
</style>