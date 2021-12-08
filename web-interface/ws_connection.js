// WS - Open, Close, On-Msg, Error
function WS_Open(e) {
    wslog("connected");
    update_status("connected");
    ws_send("close", wslog, true);
    ws_connected();
}

function WS_Close(e) {
    wslog("disconnected");
    update_status("disconnected");
}

function WS_Msg(e) {
    var msg = e.data;
    wslog(msg);
    if (ws_callback && msg.length > 0) {
        ws_callback(msg);
    }
    send_flag = true;
}

function WS_error(e) {
    wslog("error");
    update_status("error");
    wslog("BT");
    console.error(e);
}