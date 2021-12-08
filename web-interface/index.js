// ========== Global Variables ========== //

// ! List of files returned by "ls" command
var file_list = "";

// ! Variable to save interval for updating status continously
var status_interval = undefined;

// ! Unsaved content in the editor
var unsaved_changed = false;

// ! Flag if editor has loaded a file yet
var file_opened = false;


// ===== Value Getters ===== //
function get_editor_filename() {
    return elem_doc("editorFile").value;
}

// not required here
function set_editor_filename(filename) {
    return elem_doc("editorFile").value = filename;
}

function get_editor_content() {
    var content = elem_doc("textarea").value;

    if (!content.endsWith("\n"))
        content = content + "\n";

    return content;
}
// ! Stop interval that checks and updates the status continously
function stop_status_interval() {
    if (!status_interval) return; // !< Only continue if status_interval was set

    // ! Stop interval and unset variable
    clearInterval(status_interval);
    status_interval = undefined;
}

// ! Update status until it's no longer "running"
function check_status() {
    if (current_status.includes("running") || current_status.includes("saving"))
        ws_send_current_status();
    else
        stop_status_interval();
}

// ! Start interval that checks and updates the status continously
function start_status_interval() {
    if (status_interval) return; // !< Only continue if status_interval not set

    ws_send_current_status(); // !< Get current status
    status_interval = setInterval(check_status, 500); // !< Start interval
}


/*
 *
 */

function update_file_list() {
    ws_send("mem", function (msg) {
        var lines = msg.split(/\n/);

        if (lines.length == 1) {
            console.error("Check for error : " + msg);
            return;
        }

        var byte = lines[0].split(" ")[0];
        var used = lines[1].split(" ")[0];
        var free = lines[2].split(" ")[0];

        var percent = Math.floor(byte / 100);
        var freepercent = Math.floor(free / percent);

        /* calculating the leftover storage and updating inner HTML */

        elem_doc("current_free_storage").innerHTML = used + " byte used (" + freepercent + "% free)";
        file_list = "";
        ws_send("ls", function (csv) {
            file_list += csv;

            var lines = file_list.split(/\n/);
            var tableHTML = "<thead>\n";

            tableHTML += "<tr>\n";
            tableHTML += "<th>File</th>\n";
            tableHTML += "<th>Size (in bytes)</th>\n";
            tableHTML += "<th>Actions</th>\n";
            tableHTML += "</tr>\n";
            tableHTML += "</thead>\n";
            tableHTML += "<tbody>\n";

            for (var i = 0; i < lines.length; i++) {
                var data = lines[i].split(" ");
                var fileName = data[0];
                var fileSize = data[1];

                if (fileName.length > 0) {
                    if (i == 0 && !file_opened) {
                        read(fileName);
                    }
                    tableHTML += "<tr>\n";
                    tableHTML += "<td>" + fileName + "</td>\n";
                    tableHTML += "<td>" + fileSize + "</td>\n";
                    tableHTML += "<td>\n";
                    tableHTML += "<button onclick=\"read('" + fileName + "')\">edit</button>\n";
                    tableHTML += "<button onclick=\"run('" + fileName + "')\">run</button>\n";
                    tableHTML += "</tr>\n";
                }
            }
            tableHTML += "</tbody>\n";

            elem_doc("table_scripts").innerHTML = tableHTML;
        });
    });
}

// ! Recursive read from stream
function read_stream() {
    ws_send("read", function (content) {
        if (content != "> END") {
            elem_doc("textarea").value += content;
            read_stream();
            update_status("reading...");
        } else {
            ws_send("close", wslog);
            ws_send_current_status();
        }
    });
}

// Function that is called once the websocket connection was established
// Called by ws_init() in script.js
function ws_connected() {
    update_file_list();
    wslog('WS_CONNECTED_CALLED')
}
// ! Open stream to a file
function read(fileName) {
    stop(fileName);
    // fix file name
    fileName = edit_f_name(fileName);
    // set contents 
    elem_doc("editorFile").value = fileName;
    elem_doc("textarea").value = "";

    ws_send("stream \"" + fileName + "\"", wslog);

    read_stream(); // !< Read file contents (recursively)

    file_opened = true;
}

// ! Run script
function run(fileName) {
    ws_send("run \"" + edit_f_name(fileName) + "\"", wslog);
    start_status_interval();
}

// ! Stop running specific script
function stop(fileName) {
    ws_send("stop \"" + edit_f_name(fileName) + "\"", wslog, true);
}

// ! Stop running all scripts
function stopConnecting() {
    ws_send("stop", wslog, true);
}

// write editor content
// ! Write content to file
function write(fileName, content) {
    stop(fileName); // ws_send to stop that script from running

    fileName = edit_f_name(fileName);

    ws_send("remove \"/temporary_script\"", wslog);
    ws_send("create \"/temporary_script\"", wslog);

    ws_send("stream \"/temporary_script\"", wslog);

    var ws_send_log = function (msg) {
        update_status("saving...");
        wslog(msg);
    };

    var pktsize = 1024;

    for (var i = 0; i < Math.ceil(content.length / pktsize); i++) {
        var begin = i * pktsize;
        var end = begin + pktsize;
        if (end > content.length) end = content.length;

        ws_send_raw(content.substring(begin, end), ws_send_log);
    }

    ws_send("close", wslog);

    ws_send("remove \"" + fileName + "\"", wslog);
    ws_send("rename \"/temporary_script\" \"" + fileName + "\"", wslog);

    ws_send_current_status();
}

// ! Save file that is currently open in the editor
function save_editor() {
    write(get_editor_filename(), get_editor_content());
    unsaved_changed = false;
    // elem_doc("editorinfo").innerHTML = "saved";
    update_file_list();
}

// ========== Startup ========== //

window.addEventListener("load", function () {
    wslog('WS_INIT_called')

    // == EDITOR DOWNLOAD == //
    elem_doc("text_download").onclick = function () {
        console.log("Clicked");
        download_txt("File_Name", get_editor_content());
    };

    // == EDITOR SAVE == //
    elem_doc("editorSave").onclick = save_editor;

    // == EDITOR DELETE == //
    elem_doc("editorDelete").onclick = function () {
        f_name = get_editor_filename();
        stop(f_name);
        ws_send("remove \"" + edit_f_name(fileName) + "\"", wslog);
        update_file_list();
        unsaved_changed = true;
    }

    // == EDITOR RUN == //
    elem_doc("editorRun").onclick = function () {
        /*
        if (unsaved_changed) {
          save();
        }
        */
        run(get_editor_filename());
    };

    elem_doc("editorStop").onclick = function () {
        stop(get_editor_filename());
    }

    // == STATUS RECONNECT == //
    elem_doc("reconnect_status").onclick = ws_init;
    elem_doc("stop_status").onclick = stopConnecting;
    elem_doc("load_scripts").onclick = update_file_list;

    ws_init();
}, false);