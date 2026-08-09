#include <external/json.hpp>
#include <Datatypes.hpp>
#include <fstream>
#include <sstream>
#include <cstdint>
#include <string>
#include <iostream>

using json = nlohmann::json;

//Reading the Json file functio
std::string readfile(const std::string& path){
    // open file
    std::ifstream inputfile(path);
    
    //verifying it oppened
    if(!inputfile.is_open()){
        std::cerr<<"Error: Couldn't open the json file";
        return "";
    }
                                      
    //reading it into a stringstream buffer directly 
    std::stringstream buffer_streamer;
    buffer_streamer<<inputfile.rdbuf();

    //return the buffer
    return buffer_streamer.str();
}






// defining functions to parse the scan info the the FSM datatype structs
PortInfo Port_parser(const json &j){
    PortInfo PI;
    PI.port = j.at("port").get<uint16_t>();
    PI.service= j.at("service").get<std::string>();
    PI.banner = j.at("banner").get<std::string>();
    PI.cpe= j.at("cpe").get<std::vector<std::string>>();

return PI;
}


Device Device_parser(const json &j){

Device DV;  
    DV.ip = j.at("ip").get<std::string>();
    DV.mac = j.at("mac").get<std::string>();
  //Looping through ports
  if(j.contains("open_ports")){
     const auto & port_json_arr=j.at("open_ports");
     for(int i=0;i<port_json_arr.size();i++)
    { DV.ports.push_back(Port_parser(port_json_arr));}
                                }

  // to be filled by the FSM
    DV.vendor = j.value("vendor","Unknown");
    DV.model = j.value("model","Unknown");
    DV.firmware_version = j.value("frimware_version","Unknown");

    
    
    return DV;
}
    
scanResult scanResult_parser(const json &j){

    scanResult SR;  

        SR.status=j.at("vendor").get<std::string>();
        SR.error=j.at("vendor").get<std::string>();

        if(j.contains("discovered_devices")){
            auto & discovered_arr = j.at("discovered_devices");
            for(int i=0;i<discovered_arr.size();i++){
                SR.discovered_devices.push_back(Device_parser(discovered_arr[i]));
            }
                                              }
  return SR;

    }


    
