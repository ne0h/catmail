#include "../include/client.hpp"

Client::Client(std::string hostname, int port)
		: m_hostname(hostname), m_port(port), m_httpClient("http://" + m_hostname + ":" + std::to_string(m_port)),
		 	m_clientHandler(m_httpClient) {

}

int Client::createUser(std::string username, std::string password, std::shared_ptr<KeyPair> userKeyPair,
		std::shared_ptr<KeyPair> exchangeKeyPair) {

	try {
		//Json::Value result = m_clientHandler.createUser(password, username);
		//std::cout << result << std::endl;
	} catch (jsonrpc::JsonRpcException e) {
        std::cerr << e.what() << std::endl;
    }

	return 0;
}
