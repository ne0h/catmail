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

	try {
		Json::Value result = m_clientHandler.createUser(exchangeKey, password, userKey, username);
		std::cout << result << std::endl;

		return result["result"].asInt();
	} catch (jsonrpc::JsonRpcException e) {
        std::cerr << e.what() << std::endl;
    }

	return 1;
}
