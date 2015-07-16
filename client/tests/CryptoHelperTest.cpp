#include <cppunit/extensions/HelperMacros.h>

#include "../cryptohelper.hpp"
#include "../user.hpp"
#include "../contact.hpp"

class CryptoHelperTest : public CppUnit::TestFixture {

	CPPUNIT_TEST_SUITE(CryptoHelperTest);
	CPPUNIT_TEST(testAsymCrypto);
	CPPUNIT_TEST_SUITE_END();

public:
	// send an encrypted message to oneself
	void testAsymCrypto() {

		std::string text("topsecrettest");

		CryptoHelper *cryptoHelper;
		User me("me", cryptoHelper);
		Contact colleague("Colleague", me.getUserKeyPair()->getPublicKey(), me.getExchangeKeyPair()->getPublicKey());

		Message message    = cryptoHelper->encryptAsym(&me, &colleague, text);
		std::string result = cryptoHelper->decryptAsym(&me, &colleague, &message);
		
		CPPUNIT_ASSERT(text.compare(result) == 0);
	}

};
CPPUNIT_TEST_SUITE_REGISTRATION(CryptoHelperTest);
CPPUNIT_TEST_SUITE_NAMED_REGISTRATION(CryptoHelperTest, "CryptoHelperTest");
