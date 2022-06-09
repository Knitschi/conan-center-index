from conans import ConanFile
from conans import tools
from conans.errors import ConanInvalidConfiguration

class OpenCppCoverageTestPackage(ConanFile):

    name = "OpenCppCoverageTest"
    description = "Tests the OpenCppCoverage package."
    settings = "os", "compiler", "build_type", "arch"

    def test(self):
        if not tools.cross_building(self):
            openCppCoverageRoot = self.deps_cpp_info["OpenCppCoverage"].rootpath.replace("/","\\")
            # We only run one test case here to prevent problems with failing tests.
            cmd = ("\"{0}\\bin\\OpenCppCoverage.exe\" -- \"{0}\\bin\\ExporterTest.exe\" --gtest_filter=*CreateCurrentRoot*".format(openCppCoverageRoot))
            self.run(cmd, env=None)
