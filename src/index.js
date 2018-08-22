import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import registerServiceWorker from "./registerServiceWorker";
import "bootstrap/dist/css/bootstrap.css";
import "./css/style.css";
import "font-awesome/css/font-awesome.min.css";
import "jquery/dist/jquery.min.js";

ReactDOM.render(<App />, document.getElementById("root"));
registerServiceWorker();
