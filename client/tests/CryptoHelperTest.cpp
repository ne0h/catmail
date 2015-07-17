#include <cppunit/extensions/HelperMacros.h>

#include "../include/cryptohelper.hpp"
#include "../include/user.hpp"
#include "../include/contact.hpp"
#include <iostream>
class CryptoHelperTest : public CppUnit::TestFixture {

	CPPUNIT_TEST_SUITE(CryptoHelperTest);
	CPPUNIT_TEST(testAsymCrypto);
	CPPUNIT_TEST(testCrypto);
	CPPUNIT_TEST_SUITE_END();

public:

	// send an encrypted message to oneself
	void testAsymCrypto() {

		std::string text("topsecrettest");

		unsigned int failed = 0;
		for (unsigned int i = 0; i < 1000; i++) {
			CryptoHelper *cryptoHelper;
			User me("me", cryptoHelper);
			Contact colleague("Colleague", me.getUserKeyPair()->getPublicKey(),
				me.getExchangeKeyPair()->getPublicKey());

			Message message    = cryptoHelper->encryptAsym(&me, &colleague, text);
			std::string result = cryptoHelper->decryptAsym(&me, &colleague, &message);

			if (text.compare(result) != 0) {
				failed++;
			}
		}

		CPPUNIT_ASSERT(failed == 0);
	}

	// en- and decrypt a simple string
	void testCrypto() {

		std::string text = std::string("topsecrettest");

		CryptoHelper *cryptoHelper;
		User me("me", cryptoHelper);
		Contact colleague("Colleague", me.getUserKeyPair()->getPublicKey(),
			me.getExchangeKeyPair()->getPublicKey());

		std::string secretKey = cryptoHelper->generateSecretKey();
		Message message    = cryptoHelper->encrypt(&me, &colleague, text, secretKey);
		std::string result = cryptoHelper->decrypt(&me, &message, secretKey);

		CPPUNIT_ASSERT(text.compare(result) == 0);
	}

};
CPPUNIT_TEST_SUITE_REGISTRATION(CryptoHelperTest);
CPPUNIT_TEST_SUITE_NAMED_REGISTRATION(CryptoHelperTest, "CryptoHelperTest");
