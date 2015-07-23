#include <cppunit/extensions/HelperMacros.h>

#include "../include/cryptohelper.hpp"
#include "../include/user.hpp"
#include "../include/contact.hpp"
#include "../include/base64.hpp"

std::string longTestString = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.   Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.   Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, At accusam aliquyam diam diam dolore dolores duo eirmod eos erat, et nonumy sed tempor et et invidunt justo labore Stet clita ea et gubergren, kasd magna no rebum. sanctus sea sed takimata ut vero voluptua. est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat.  Consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo";

class CryptoHelperTest : public CppUnit::TestFixture {

	CPPUNIT_TEST_SUITE(CryptoHelperTest);
	CPPUNIT_TEST(testAsymCrypto);
	CPPUNIT_TEST(testCrypto);
	CPPUNIT_TEST(testLongCrypto);
	CPPUNIT_TEST(testBase64);
	CPPUNIT_TEST(testEncryptedBase64SecretKey);
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

		CPPUNIT_ASSERT(result.compare(text) == 0);
	}

	// en- and decrypt a "very long" string
	void testLongCrypto() {

		std::shared_ptr<CryptoHelper> cryptoHelper(new CryptoHelper());
		std::shared_ptr<User> me(new User("me", cryptoHelper));
		std::shared_ptr<Contact> colleague(new Contact("Colleague", me->getUserKeyPair()->getPublicKey(),
			me->getExchangeKeyPair()->getPublicKey()));

		std::string symKey = cryptoHelper->generateSymKey();
		Message message    = cryptoHelper->encrypt(me, colleague, longTestString, symKey);
		std::string result = cryptoHelper->decrypt(me, std::make_shared<Message>(message), symKey);

		CPPUNIT_ASSERT(result.compare(longTestString) == 0);
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
	void testEncryptedBase64SecretKey() {

		std::shared_ptr<CryptoHelper> cryptoHelper(new CryptoHelper());
		KeyPair keyPair    = cryptoHelper->generateKeyPair();
		std::string symKey = cryptoHelper->generateSymKey();

		CryptoBox in = cryptoHelper->encryptAndEncodeBase64(keyPair.getSecretKey(), symKey);
		std::shared_ptr<CryptoBox> out(new CryptoBox(in.getValue(), in.getNonce()));
		std::string result = cryptoHelper->decodeBase64AndDecrypt(out, symKey);

		CPPUNIT_ASSERT(keyPair.getSecretKey().compare(result) == 0);
	}

};
CPPUNIT_TEST_SUITE_REGISTRATION(CryptoHelperTest);
CPPUNIT_TEST_SUITE_NAMED_REGISTRATION(CryptoHelperTest, "CryptoHelperTest");
