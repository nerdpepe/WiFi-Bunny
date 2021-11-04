function elem_doc(id) {
    return document.getElementById(id);
}

// OnLoad event
window.addEventListener('load', loaded)
function loaded() {
    elem_doc("text_download").onclick = function () {
        console.log("Clicked");
        download_txt("File_Name", get_editor_content());
    };
}

// Get the content of editor
function get_editor_content() {
    var content = elem_doc("textarea").value;

    if (!content.endsWith("\n"))
        content = content + "\n";

    return content;
}

/*  Download the file : 
    https://www.delftstack.com/howto/javascript/javascript-download/
 */

function download_txt(fileName, fileContent) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(fileContent));
    element.setAttribute('download', fileName);

    document.body.appendChild(element);
    // simulate mouse click
    element.click();
    document.body.removeChild(element);
}
