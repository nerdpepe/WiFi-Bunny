var ws_url = "192.168.4.1";
var current_status = ""; // to store the current connection status

// websocket
var ws = null;
var ws_queue_messages = []; // outgoing msgs
var ws_interval = null;
var ws_interval_timeout = 0 // interval timeout

var send_flag = false; // message queue
var ws_callback = wslog;

// Sets background Color of status 
function setBackground(current_status, color) {
    elem_doc(current_status).style.backgroundColor = color;
}

/*
    Sets Text Color of status according to 'condition'
*/

function setTextColor(condition) {
    if (condition == "connected") {
        elem_doc("current_status").style.color = "#3c5";
    } else if (condition == "disconnected") {
        elem_doc("current_status").style.color = "#ed1556";
    } else if (condition.includes("problem") || condition.includes("error")) {
        elem_doc("current_status").style.color = "#ffb247";
    } else /*if (condition == "connecting..")*/ {
        elem_doc("current_status").style.color = "#0ae";
    }
}

// change status on interface
function update_status(condition) {
    current_status = condition;
    setBackground("current_status", "#c0c0c0");
    setTextColor(condition);
    elem_doc("current_status").innerHTML = condition;
}

function ws_q_msgs_update() {
    if (ws_queue_messages.length >= 1 && send_flag) {
        var item = ws_queue_messages.shift();
        ws.send(item.message);
        ws_callback = item.callback;
        console.debug("# " + item.message);
        send_flag = false;
    }
}

// == WebSocket initialization == //
function ws_init() {
    update_status("..connecting"); // function in same file
    ws = new WebSocket("ws://" + ws_url + "/ws"); // creating ws
    ws.onopen = WS_Open;
    ws.onclose = WS_Close;
    ws.onmessage = WS_Msg;
    ws.onerror = WS_error;
    //clear to send
    send_flag = true;
    // clear the interval if it is set and then use setInterval
    ws_interval = set_ws_interval(ws_q_msgs_update);
    wslog("WS_INIT_END");
}