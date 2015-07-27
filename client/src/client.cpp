#include "../include/client.hpp"

Client::Client(std::string hostname, int port)
		: m_hostname(hostname), m_port(port), m_httpClient("http://" + m_hostname + ":" + std::to_string(m_port)),
		 	m_clientHandler(m_httpClient) {

}

int Client::createUser(std::string username, std::string password, std::shared_ptr<KeyPairBox> userKeyPair,
		std::shared_ptr<KeyPairBox> exchangeKeyPair) {

	Json::Value userKey;
	userKey["secretKey"] = userKeyPair->getValue();
	userKey["nonce"]     = userKeyPair->getNonce();
	userKey["publicKey"] = userKeyPair->getPublicKey();

	Json::Value exchangeKey;
	exchangeKey["secretKey"] = exchangeKeyPair->getValue();
	exchangeKey["nonce"]     = exchangeKeyPair->getNonce();
	exchangeKey["publicKey"] = exchangeKeyPair->getPublicKey();

	Json::Value response;

	try {
		response = m_clientHandler.createUser(exchangeKey, password, userKey, username);
		std::cout << response << std::endl;
	} catch (jsonrpc::JsonRpcException e) {
        std::cerr << e.what() << std::endl;
    }

	return response["result"].asInt();
}

KeyPairBox Client::login(std::string username, std::string password) {
	
	Json::Value response;

	try {
		response = m_clientHandler.login(password, username);
		std::cout << response << std::endl;
	} catch (jsonrpc::JsonRpcException e) {
		std::cerr << e.what() << std::endl;
	}
	
	return KeyPairBox(response["secretKey"].asString(), response["nonce"].asString(), response["publicKey"].asString());
}
