#include<Datatypes.hpp>
#include<JsonParser.hpp>
#include<cstdint>

int main(){

    std::string path = "/Scanner/Scan_result.json";
    // we need to see the Json file and parse it to the function defined in JsonParser
    std::string file_Content = readfile(path);
    json file_Content_json = file_Content.get<Json>;

    Port_parser(file_Content_json);
    Device_parser(file_Content_json);
    scanResult_parser(file_Content_json);
}