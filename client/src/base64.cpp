#include "../include/base64.hpp"
#include <iostream>

static const std::string base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

static inline bool is_base64(unsigned char c) {
	return (isalnum(c) || (c == '+') || (c == '/'));
}

std::string base64_encode(std::string input) {

	unsigned char const* input_bytes = (const unsigned char *)input.c_str();
	unsigned int in_len = input.size();

	std::string result;
	unsigned int i = 0;
	unsigned int j = 0;
	unsigned char char_array_3[3];
	unsigned char char_array_4[4];

	while (in_len--) {
		char_array_3[i++] = *(input_bytes++);

		if (i == 3) {
			char_array_4[0] = (char_array_3[0] & 0xfc)  >> 2;
			char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
			char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
			char_array_4[3] = char_array_3[2] & 0x3f;

			for(i = 0; i < 4; i++) {
				result += base64_chars[char_array_4[i]];
			}

			i = 0;
		}
	}

	if (i) {
		for(j = i; j < 3; j++) {
			char_array_3[j] = '\0';
		}

		char_array_4[0] = (char_array_3[0] & 0xfc)  >> 2;
		char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
		char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
		char_array_4[3] = char_array_3[2] & 0x3f;

		for (j = 0; (j < i + 1); j++) {
			result += base64_chars[char_array_4[j]];
		}
	}

	while((i++ < 3)) {
      result += '=';
	}

	return result;
}

std::string base64_decode(std::shared_ptr<std::string> input) {

	size_t inputLength = input->size();
	size_t i = 0;
	size_t j = 0;
	
	int inputCounter = 0;
	unsigned char char_array_4[4], char_array_3[3];
	std::string result;

	while (inputLength-- && (input->at(inputCounter) != '=') && is_base64(input->at(inputCounter))) {
		char_array_4[i++] = input->at(inputCounter); inputCounter++;
		
		if (i == 4) {
			for (i = 0; i <4; i++) {
				char_array_4[i] = static_cast<unsigned char>(base64_chars.find(char_array_4[i]));
			}

			char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
			char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
			char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

			for (i = 0; (i < 3); i++) {
				result += char_array_3[i];
			}
			
			i = 0;
		}
	}

	if (i) {
		for (j = i; j <4; j++) {
			char_array_4[j] = 0;
		}

		for (j = 0; j <4; j++) {
			char_array_4[j] = static_cast<unsigned char>(base64_chars.find(char_array_4[j]));
		}

		char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
		char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
		char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

		for (j = 0; (j < i - 1); j++) {
			result += char_array_3[j];
		}
	}

	return result;
}

void base64_encode(std::shared_ptr<CryptoBox> input) {
	std::string message = base64_encode(input->getMessage());
	std::string nonce   = base64_encode(input->getNonce());

	input->setMessage(message);
	input->setNonce(nonce);
}

void base64_decode(std::shared_ptr<CryptoBox> input) {
	std::string message = base64_decode(std::make_shared<std::string>(input->getMessage()));
	std::string nonce   = base64_decode(std::make_shared<std::string>(input->getNonce()));

	input->setMessage(message);
	input->setNonce(nonce);
}
