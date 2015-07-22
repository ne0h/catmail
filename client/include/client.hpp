#ifndef CLIENT_HPP
#define CLIENT_HPP

#include <string>
#include <iostream>

#include "../include/keypair.hpp"

#include <jsonrpccpp/client/connectors/httpclient.h>
#include "../api/clienthandler.hpp"

class KeyPairValue : public Json::Value {

public:
	KeyPairValue(std::string secretKey, std::string publicKey) : m_secretKey(secretKey), m_publicKey(publicKey) {}
	std::string getSecretKey() {return m_secretKey;}
	std::string getPublicKey() {return m_publicKey;}

private:
	std::string m_secretKey;
	std::string m_publicKey;

};

class Client {

public:
	Client(std::string hostname, int port);
	int createUser(std::string username, std::string password, std::shared_ptr<KeyPair> userKeyPair,
		std::shared_ptr<KeyPair> exchangeKeyPair);

private:
	std::string m_hostname;
	int m_port;
	jsonrpc::HttpClient m_httpClient;
	ClientHandler m_clientHandler;

};

#endif