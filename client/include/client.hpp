#ifndef CLIENT_HPP
#define CLIENT_HPP

#include <string>
#include <memory>
#include <iostream>

#include "../include/keypair.hpp"

#include <jsonrpccpp/client/connectors/httpclient.h>
#include "../api/clienthandler.hpp"

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