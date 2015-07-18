#ifndef BASE64_HPP
#define BASE64_HPP

#include <string>
#include <memory>

std::string base64_encode(std::string input);
std::string base64_decode(std::shared_ptr<std::string> s);

#endif 