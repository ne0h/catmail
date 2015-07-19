#ifndef BASE64_HPP
#define BASE64_HPP

#include <string>
#include <memory>

#include "cryptobox.hpp"

std::string base64_encode(std::string input);
void        base64_encode(std::shared_ptr<CryptoBox> input);
std::string base64_decode(std::shared_ptr<std::string> s);
void        base64_decode(std::shared_ptr<CryptoBox> input);

#endif 