function wslog(m) {
    // check the console in page source
    console.log(" - WS - console " + m);
}

// elem_doc -> gets the element by id
function elem_doc(id) {
    return document.getElementById(id);
}

function edit_f_name(f_name) {
    return f_name.replace(/ /g, '\-');
}