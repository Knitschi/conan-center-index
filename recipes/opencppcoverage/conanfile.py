from conans import ConanFile
from conans import tools
from conans.errors import ConanInvalidConfiguration

class OpenCppCoverage(ConanFile):

    """
    Note that OpenCppCoverage uses vcpckg to acquire its own dependencies.
    As I only need the OpenCppCoverage.exe I did not try to convert the
    dependency acquisition also to conan.
    """

    name = "OpenCppCoverage"
    repository = "https://github.com/OpenCppCoverage/OpenCppCoverage.git"
    license = "GNU General Public License v3.0"
    url = "https://github.com/OpenCppCoverage/OpenCppCoverage"
    version = "0.9.9.0"
    description = "OpenCppCoverage is an open source code coverage tool for C++ under Windows."
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*"
    short_paths = True  

    def validate(self):
        if (self.settings.os != "Windows") or (self.settings.arch != "x86_64" ):
            raise ConanInvalidConfiguration("This tool can only be build in a Windows x86_64 configuration.")

        if(self.source_folder != self.build_folder):
            raise ConanInvalidConfiguration("Currently the build folder can not be chosen freely.")

    def source(self):
        self.run("git clone --recursive {0} {1}".format(self.repository, self.source_folder))
        self.run("cd {0} && git checkout release-{1}".format(self.source_folder, self.version))

    def build(self):
        self.run("{0}/BuildThirdPartyDependencies.bat".format(self.source_folder))
        self.run(self._vcvars_command() + "MSBuild.exe {0}/CppCoverage.sln -p:Configuration={1}".format(self.source_folder, self.settings.build_type))

    def package(self):
        # Copy files from the build tree to the package.
        self.copy("*.exe", dst="bin", src="{0}/x64/{1}".format(self.source_folder, self.settings.build_type))
        self.copy("*.dll", dst="bin", src="{0}/x64/{1}".format(self.source_folder, self.settings.build_type))
        self.copy("*", dst="bin/Template", src="{0}/x64/{1}/Template".format(self.source_folder,self.settings.build_type))
        self.copy("*", dst="bin/Plugins", src="{0}/x64/{1}/Plugins".format(self.source_folder, self.settings.build_type))

    def _vcvars_command(self):
        # For visual studio we use the vcvarsall.bat environment because I could not get ninja builds to work without it.
        environment_command = ""
        if self.settings.compiler == "Visual Studio":   # Use varsal environment when using visual studio compiler.
            environment_command = tools.vcvars_command(self) + " && "
        return environment_command
