/*  Download the file : 
    https://www.delftstack.com/howto/javascript/javascript-download/
 */
function download_txt(f_name, fileContent) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(fileContent));
    element.setAttribute('download', f_name);

    document.body.appendChild(element);
    // simulate mouse click
    element.click();
    document.body.removeChild(element);
}