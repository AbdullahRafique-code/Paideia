
#ifndef DATATYPES_HPP
#define DATATYPES_HPP
// we will define the Device, and PortInfo Structs here
#include <string>
#include <vector>
#include <cstdint> // for uint16_t (thanks Chip8 project)




struct PortInfo{
    uint16_t port; //port number is in the range of 0-65535, so we can use uint16t to store it
    std::string service;
    std::string banner;
    std::vector<std::string> cpe;
};

struct Device{
  std::string ip;
  std::string mac;
  std::vector<PortInfo> ports;

  // to be filled by the FSM
  std::string vendor;
  std::string model;
  std::string firmware_version;
};

struct scanResult{
    std::string status;
    std::string error;
    std::vector<Device> discovered_devices;

};

#endif 