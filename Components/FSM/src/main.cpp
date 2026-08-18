#include<Datatypes.hpp>
#include<JsonParser.hpp>
#include<cstdint>

int main(){
    //hardcoded for now, later command line args
    std::string path = "../samplescan/sample_scan_result.json";
    // we need to see the Json file and parse it to the function defined in JsonParser
    std::string file_Content = readfile(path);

    json file_Content_json = json::parse(file_Content);

    //testing
    scanResult result = scanResult_parser(file_Content_json);

    std::cout<<"Status: "<<result.status<<"\n";
    std::cout<<"Device found: "<<result.discovered_devices.size()<<"\n";
    for(const auto &d : result.discovered_devices){
        std::cout<<""<<d.ip<<" ("<<d.mac<<") - "<<d.ports.size()<< " open ports\n";
    }




    return 0;
}