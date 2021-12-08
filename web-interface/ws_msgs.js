
function set_ws_interval(ws_q_msgs) {
    if (ws_interval)
        clearInterval(ws_interval);
    ws_interval_timeout = 1
    return setInterval(ws_q_msgs, ws_interval_timeout);
}
// sending and adding WS messages to queue

function ws_send(msg, cbk, force = false) {
    if (!msg.endsWith('\n')) msg += '\n';
    ws_send_raw(msg, cbk, force);
}

function ws_send_raw(message, callback, force = false) {
    var obj = {
        "message": message,
        "callback": callback
    };

    if (force) {
        ws_queue_messages.unshift(obj);
    } else {
        ws_queue_messages.push(obj);
    }
}

function ws_send_current_status() {
    ws_send("status", update_status);
}