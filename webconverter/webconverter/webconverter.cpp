#define _CRT_SECURE_NO_WARNINGS

#include <iostream>
#include <string>
#include <filesystem>  //c++17
#include <vector>
#include <fstream>
#include <algorithm>
#include <sstream>
#include "zlib.h"
#include "zconf.h"
#pragma comment(lib,"zdll.lib")
namespace fs = std::filesystem;
using namespace std;

/* data : Original data
   ndata : Original data length 
   zdata : Compressed data 
   nzdata : Length after compression */
int gzcompress(Bytef* data, uLong ndata, Bytef* zdata, uLong* nzdata)
{
    z_stream c_stream;
    int err = 0;

    if (data && ndata > 0) {
        c_stream.zalloc = NULL;
        c_stream.zfree = NULL;
        c_stream.opaque = NULL;
        if (deflateInit2(&c_stream, Z_DEFAULT_COMPRESSION, Z_DEFLATED,
            MAX_WBITS + 16, 8, Z_DEFAULT_STRATEGY) != Z_OK) return -1;
        c_stream.next_in = data;
        c_stream.avail_in = ndata;
        c_stream.next_out = zdata;
        c_stream.avail_out = *nzdata;
        while (c_stream.avail_in != 0 && c_stream.total_out < *nzdata) {
            if (deflate(&c_stream, Z_NO_FLUSH) != Z_OK) return -1;
        }
        if (c_stream.avail_in != 0) return c_stream.avail_in;
        for (;;) {
            if ((err = deflate(&c_stream, Z_FINISH)) == Z_STREAM_END) break;
            if (err != Z_OK) return -1;
        }
        if (deflateEnd(&c_stream) != Z_OK) return -1;
        *nzdata = c_stream.total_out;
        return 0;
    }
    return -1;
}


vector<string> split(const string& str, const string& delims = " ")
{
    vector<string> output;
    auto first = cbegin(str);
    while (first != cend(str))
    {
        const auto second = find_first_of(first, cend(str),cbegin(delims), cend(delims));
        if (first != second)
            output.emplace_back(first, second);
        if (second == cend(str))
            break;
        first = next(second);
    }
    return output;
}


auto get_varname(string filename)
{
    replace(filename.begin(),filename.end(), '.', '_');
    return filename;
}

auto get_file_type(string filename)
{
    auto file_ending = split(filename, ".")[1];
    if (file_ending == "js")
        return "application/javascript";
    else if (file_ending == "css")
        return "text/css";
    else if (file_ending == "html")
        return "text/html";
    else
        return "text/plain";
}

auto get_response_code(string filename)
{
    if (filename == "error404.html")
        return "404";
    else
        return "200";
}

void write_server_callback(string filename, ofstream& output)
{
    auto varname = get_varname(filename);
    auto filetype = get_file_type(filename);
    auto response_code = get_response_code(filename);

    output << "\\\nserver.on(\"/";
    output << filename;
    output << "\", HTTP_GET, [](AsyncWebServerRequest* request) {";
    output << "\\\n\treply(request, ";
    output << response_code;
    output << ", \"";
    output << filetype;
    output << "\", ";
    output << varname;
    output << ", sizeof(";
    output << varname;
    output << "));";
    output << "\\\n});";
}

auto get_file_content(string path, uLong& comprlen)
{
    int err;
    ifstream file;
    file.open(path);
    stringstream buffer;
    buffer << file.rdbuf();
    string content(buffer.str());
    //content = file.read().encode("utf-8")
    file.close();
    const char* tmp = content.c_str();
    Byte compr[3000], uncompr[3000];
    uLong uncomprLen;
    uLong len = strlen(tmp) + 1;
    comprlen = sizeof(compr) / sizeof(compr[0]);
    err = gzcompress((Bytef*)tmp, len, compr, &comprlen);
    if (err != Z_OK) 
    {
        cerr << "compress error: " << err << endl;
        exit(1);
    }
    cout << len << " byte " << "-> " << comprlen << "byte" << "... ";
    strcpy((char*)uncompr, "garbage");
    return compr;
}

auto build_hex_string(string varname, Byte* content, uLong comprlen)
{
    stringstream ss;
    string s2;
    string hexstr = "const uint8_t " + varname + "[] PROGMEM = { ";
    for (auto i = 0; i < comprlen; i++)
    {
        ss << "0x" << hex << int(content[i]) << ",";
    }
    s2 = ss.str();
    hexstr += s2;
    hexstr = hexstr.substr(0, hexstr.length() - 1);
    hexstr += " };\n\n";
    return hexstr;
}

void write_hex_array(string filename, ofstream& output)
{
    uLong comprlen = 0;
    cout << "Converting " << filename << "... ";
    string path = "web/" + filename;
    auto content = get_file_content(path, comprlen);
    auto varname = get_varname(filename);
    auto hex_array = build_hex_string(varname, content, comprlen);
    output << hex_array;
    cout << "OK" << endl;
}



void write_callbacks(vector<string> files, ofstream& output)
{
    for (auto filename : files)
        write_server_callback(filename, output);
}

void write_arrays(vector<string> files, ofstream& output)
{
    for (auto filename : files)
        write_hex_array(filename, output);
}

string WstringToString(const wstring str)
{
    unsigned len = str.size() * 4;
    setlocale(LC_CTYPE, "");
    char* p = new char[len];
    wcstombs(p, str.c_str(), len);
    string str1(p);
    delete[] p;
    return str1;
}


int main()
{
    vector<string> web_files = {};
    for (const auto& entry : fs::directory_iterator("web/"))
        web_files.push_back(split(WstringToString(entry.path()),"/")[1]);

    ofstream outputfile;
    outputfile.open("esp_duck/webfiles.h");
    outputfile << "#pragma once\n\n";

    outputfile << "#define WEBSERVER_CALLBACK ";

    write_callbacks(web_files, outputfile);

    outputfile << "\n\n";

    write_arrays(web_files, outputfile);

    outputfile.close();

    return 0;
}
