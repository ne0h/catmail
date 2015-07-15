#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/ui/text/TestRunner.h>

int main () {

	CppUnit::TextUi::TestRunner runner;
	CppUnit::TestFactoryRegistry& registry = CppUnit::TestFactoryRegistry::getRegistry();

	CppUnit::Test* test_to_run = registry.makeTest();
	runner.addTest( test_to_run );
	bool failed = runner.run("", false);

	return !failed;
}