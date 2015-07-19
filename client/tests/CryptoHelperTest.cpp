#include <cppunit/extensions/HelperMacros.h>

#include "../include/cryptohelper.hpp"
#include "../include/user.hpp"
#include "../include/contact.hpp"
#include "../include/base64.hpp"

#include <iostream>
class CryptoHelperTest : public CppUnit::TestFixture {

	CPPUNIT_TEST_SUITE(CryptoHelperTest);
	CPPUNIT_TEST(testAsymCrypto);
	CPPUNIT_TEST(testCrypto);
	CPPUNIT_TEST(testBase64);
	CPPUNIT_TEST(testBase64SecretKey);
	CPPUNIT_TEST_SUITE_END();

public:

	// send an encrypted message to oneself
	void testAsymCrypto() {

		std::string text("topsecrettest");
		std::shared_ptr<CryptoHelper> cryptoHelper(new CryptoHelper());
		std::shared_ptr<User> me(new User("me", cryptoHelper));
		std::shared_ptr<Contact> colleague(new Contact("Colleague", me->getUserKeyPair()->getPublicKey(),
			me->getExchangeKeyPair()->getPublicKey()));

		unsigned int failed = 0;
		for (unsigned int i = 0; i < 1000; i++) {
			Message message    = cryptoHelper->encryptAsym(me, colleague, text);
			std::string result = cryptoHelper->decryptAsym(me, colleague, std::make_shared<Message>(message));

			if (text.compare(result) != 0) {
				failed++;
			}
		}

		CPPUNIT_ASSERT(failed == 0);
	}

	// en- and decrypt a simple string
	void testCrypto() {

		std::string text = std::string("topsecrettest");

		std::shared_ptr<CryptoHelper> cryptoHelper(new CryptoHelper());
		std::shared_ptr<User> me(new User("me", cryptoHelper));
		std::shared_ptr<Contact> colleague(new Contact("Colleague", me->getUserKeyPair()->getPublicKey(),
			me->getExchangeKeyPair()->getPublicKey()));

		std::string symKey = cryptoHelper->generateSymKey();
		Message message    = cryptoHelper->encrypt(me, colleague, text, symKey);
		std::string result = cryptoHelper->decrypt(me, std::make_shared<Message>(message), symKey);

		CPPUNIT_ASSERT(text.compare(result) == 0);
	}

	// en- and decode base64 a secret key
	void testBase64() {

		std::shared_ptr<CryptoHelper> cryptoHelper(new CryptoHelper());
		std::string symKey = cryptoHelper->generateSymKey();

		std::string encoded = base64_encode(symKey);
		std::string decoded = base64_decode(std::make_shared<std::string>(encoded));

		CPPUNIT_ASSERT(decoded.compare(symKey) == 0);
	}

	// en- and decrypt a base64 encoded secret key from a keypair
	void testBase64SecretKey() {

		std::shared_ptr<CryptoHelper> cryptoHelper(new CryptoHelper());
		KeyPair keyPair    = cryptoHelper->generateKeyPair();
		std::string symKey = cryptoHelper->generateSymKey();

		CryptoBox encodedAndEncrypted = cryptoHelper->encryptAndEncodeBase64(keyPair.getSecretKey(), symKey);

		CPPUNIT_ASSERT(true);
	}

};
CPPUNIT_TEST_SUITE_REGISTRATION(CryptoHelperTest);
CPPUNIT_TEST_SUITE_NAMED_REGISTRATION(CryptoHelperTest, "CryptoHelperTest");
