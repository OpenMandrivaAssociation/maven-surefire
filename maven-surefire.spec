Name:		maven-surefire
Version:	3.6.1
Release:	1
Epoch:		0
Summary:	Maven Surefire and Failsafe test plugins
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/surefire/
Source0:	https://github.com/apache/maven-surefire/archive/refs/tags/surefire-%{version}.tar.gz#/surefire-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	maven-plugin-tools >= 3.16.0
BuildRequires:	mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:	maven-shade-plugin >= 3.6.2-2
BuildRequires:	mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:	java-current-devel
BuildRequires:	junit5 >= 5.14.4
BuildRequires:	mvn(org.junit.platform:junit-platform-engine)
BuildRequires:	mvn(org.junit.platform:junit-platform-launcher)
Requires:	junit5 >= 5.14.4
BuildRequires:	mvn(org.apiguardian:apiguardian-api)
BuildRequires:	apiguardian >= 1.1.2
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	slf4j
Requires:	slf4j
BuildRequires:	mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:	maven-shared-utils >= 3.5.0
Requires:	maven-shared-utils >= 3.5.0
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	apache-commons-io >= 1:2.22.0
Requires:	apache-commons-io >= 1:2.22.0
BuildRequires:	mvn(org.apache.commons:commons-lang3)
BuildRequires:	apache-commons-lang3 >= 3.21.0
Requires:	apache-commons-lang3 >= 3.21.0
BuildRequires:	mvn(org.apache.commons:commons-compress)
BuildRequires:	apache-commons-compress >= 1.28.0
Requires:	apache-commons-compress >= 1.28.0
BuildRequires:	mvn(commons-codec:commons-codec)
BuildRequires:	apache-commons-codec >= 1.23.0
Requires:	apache-commons-codec >= 1.23.0
BuildRequires:	mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:	maven-common-artifact-filters >= 3.4.0-2
Requires:	maven-common-artifact-filters >= 3.4.0-2
BuildRequires:	mvn(org.codehaus.plexus:plexus-java)
BuildRequires:	plexus-java >= 1.7.0
Requires:	plexus-java >= 1.7.0
BuildRequires:	mvn(org.apache.maven.resolver:maven-resolver-util)
BuildRequires:	mvn(com.google.code.findbugs:jsr305)
BuildRequires:	jsr-305 >= 3.0.2-3
BuildRequires:	mvn(javax.inject:javax.inject)
BuildRequires:	javax.inject >= 1-2
BuildRequires:	mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:	mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildSystem:	maven

Obsoletes:	maven-surefire-plugin < %{EVRD}
Provides:	maven-surefire-plugin = %{EVRD}
Obsoletes:	maven-failsafe-plugin < %{EVRD}
Provides:	maven-failsafe-plugin = %{EVRD}
Obsoletes:	maven-surefire-booter < %{EVRD}
Provides:	maven-surefire-booter = %{EVRD}
Obsoletes:	maven-surefire-maven-plugin < %{EVRD}
Provides:	maven-surefire-maven-plugin = %{EVRD}
Obsoletes:	maven2-plugin-surefire < %{EVRD}
Provides:	maven2-plugin-surefire = %{EVRD}
Obsoletes:	maven-surefire-report-parser < %{EVRD}
Provides:	maven-surefire-report-parser = %{EVRD}
Obsoletes:	maven-surefire-provider-junit < %{EVRD}
Obsoletes:	maven-surefire-provider-junit4 < %{EVRD}
Obsoletes:	maven-surefire-provider-testng < %{EVRD}
Obsoletes:	maven-surefire-report-plugin < %{EVRD}
Obsoletes:	maven-surefire-report-maven-plugin < %{EVRD}
Obsoletes:	maven2-plugin-surefire-report < %{EVRD}

%description
Runs unit tests (Surefire) and integration tests (Failsafe). 3.6.1
groups JPMS module-path arguments, fixes a memory leak in large JUnit 4
suites, lets a build opt out of StackWalker stack capture, and corrects
fork timeouts and include/exclude matching. Shared utils, commons-lang3,
commons-compress, commons-codec, and commons-io are shaded into
surefire-shared-utils. The report plugin and the TestNG provider are
not built. Tests are not run.

%prep
%autosetup -n maven-surefire-surefire-%{version}
python - %{version} <<'PY'
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)
VERSION = sys.argv[1]

def tag(name):
    return "{" + NS + "}" + name


def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node


def write(path, builder):
    root = ET.Element(tag("project"))
    builder(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def parent_block(project, relative):
    parent = ET.SubElement(project, tag("parent"))
    add(parent, "groupId", "org.apache.maven.surefire")
    add(parent, "artifactId", "surefire")
    add(parent, "version", VERSION)
    add(parent, "relativePath", relative)


def dep(deps, group, artifact, version, scope=None, optional=False):
    node = ET.SubElement(deps, tag("dependency"))
    add(node, "groupId", group)
    add(node, "artifactId", artifact)
    add(node, "version", version)
    if scope:
        add(node, "scope", scope)
    if optional:
        add(node, "optional", "true")


def jsr305(deps):
    dep(deps, "com.google.code.findbugs", "jsr305", "3.0.2", "provided")


def maven_provided(deps):
    dep(deps, "org.apache.maven", "maven-plugin-api", "3.10.0", "provided")
    dep(deps, "org.apache.maven", "maven-core", "3.10.0", "provided")
    dep(deps, "org.apache.maven", "maven-artifact", "3.10.0", "provided")
    dep(deps, "org.apache.maven", "maven-model", "3.10.0", "provided")
    dep(deps, "org.apache.maven.resolver", "maven-resolver-api", "2.0.24", "provided")
    dep(deps, "org.eclipse.sisu", "org.eclipse.sisu.plexus", "0.9.0.M3", "provided")
    dep(deps, "javax.inject", "javax.inject", "1", "provided")
    dep(deps, "org.apache.maven.plugin-tools", "maven-plugin-annotations", "3.15.2", "provided")


def plugin_descriptor(project):
    build = ET.SubElement(project, tag("build"))
    plugins = ET.SubElement(build, tag("plugins"))
    plugin = ET.SubElement(plugins, tag("plugin"))
    add(plugin, "groupId", "org.apache.maven.plugins")
    add(plugin, "artifactId", "maven-plugin-plugin")
    add(plugin, "version", "3.16.0")
    executions = ET.SubElement(plugin, tag("executions"))
    execution = ET.SubElement(executions, tag("execution"))
    add(execution, "id", "default-descriptor")
    goals = ET.SubElement(execution, tag("goals"))
    add(goals, "goal", "descriptor")


def shade_plugin(project):
    build = ET.SubElement(project, tag("build"))
    plugins = ET.SubElement(build, tag("plugins"))
    plugin = ET.SubElement(plugins, tag("plugin"))
    add(plugin, "groupId", "org.apache.maven.plugins")
    add(plugin, "artifactId", "maven-shade-plugin")
    add(plugin, "version", "3.6.2")
    executions = ET.SubElement(plugin, tag("executions"))
    execution = ET.SubElement(executions, tag("execution"))
    add(execution, "id", "shade-shared")
    add(execution, "phase", "package")
    goals = ET.SubElement(execution, tag("goals"))
    add(goals, "goal", "shade")
    cfg = ET.SubElement(execution, tag("configuration"))
    artifact_set = ET.SubElement(cfg, tag("artifactSet"))
    excludes = ET.SubElement(artifact_set, tag("excludes"))
    add(excludes, "exclude", "org.apache.maven.surefire:surefire-shared-utils")
    add(excludes, "exclude", "org.slf4j:*")
    filters = ET.SubElement(cfg, tag("filters"))
    filt = ET.SubElement(filters, tag("filter"))
    add(filt, "artifact", "*:*")
    ex = ET.SubElement(filt, tag("excludes"))
    add(ex, "exclude", "**/module-info.class")
    add(ex, "exclude", "META-INF/MANIFEST.MF")
    relocations = ET.SubElement(cfg, tag("relocations"))
    moves = (
        ("org.apache.maven.shared.utils", "org.apache.maven.surefire.shared.utils"),
        ("org.apache.commons.codec", "org.apache.maven.surefire.shared.codec"),
        ("org.apache.commons.io", "org.apache.maven.surefire.shared.io"),
        ("org.apache.commons.lang3", "org.apache.maven.surefire.shared.lang3"),
        ("org.apache.commons.compress", "org.apache.maven.surefire.shared.compress"),
    )
    for pattern, shaded in moves:
        relocation = ET.SubElement(relocations, tag("relocation"))
        add(relocation, "pattern", pattern)
        add(relocation, "shadedPattern", shaded)


def setup_parent(project):
    add(project, "modelVersion", "4.0.0")
    add(project, "groupId", "org.apache.maven.surefire")
    add(project, "artifactId", "surefire")
    add(project, "version", VERSION)
    add(project, "packaging", "pom")
    add(project, "name", "Apache Maven Surefire")
    props = ET.SubElement(project, tag("properties"))
    add(props, "maven.compiler.release", "8")
    add(props, "project.build.sourceEncoding", "UTF-8")
    modules = ET.SubElement(project, tag("modules"))
    for name in (
        "surefire-shared-utils",
        "surefire-logger-api",
        "surefire-api",
        "surefire-extensions-api",
        "surefire-extensions-spi",
        "surefire-booter",
        "surefire-providers/common-java5",
        "surefire-providers/surefire-junit-platform",
        "maven-surefire-common",
        "surefire-report-parser",
        "maven-surefire-plugin",
        "maven-failsafe-plugin",
    ):
        add(modules, "module", name)


def setup_shared(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../pom.xml")
    add(project, "artifactId", "surefire-shared-utils")
    add(project, "name", "Surefire Shared Utils")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.apache.maven.shared", "maven-shared-utils", "3.5.0", "runtime")
    dep(deps, "commons-io", "commons-io", "2.22.0", "runtime")
    dep(deps, "org.apache.commons", "commons-lang3", "3.21.0", "runtime")
    dep(deps, "org.apache.commons", "commons-compress", "1.28.0", "runtime")
    dep(deps, "commons-codec", "commons-codec", "1.23.0", "runtime")
    shade_plugin(project)


def setup_logger(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../pom.xml")
    add(project, "artifactId", "surefire-logger-api")
    add(project, "name", "Surefire Logger API")


def setup_api(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../pom.xml")
    add(project, "artifactId", "surefire-api")
    add(project, "name", "Surefire API")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.apache.maven.surefire", "surefire-logger-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-shared-utils", VERSION, optional=True)
    jsr305(deps)


def setup_extensions_api(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../pom.xml")
    add(project, "artifactId", "surefire-extensions-api")
    add(project, "name", "Surefire Extensions API")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.apache.maven.surefire", "surefire-api", VERSION, "provided")
    dep(deps, "org.apache.maven.surefire", "surefire-logger-api", VERSION, "provided")
    dep(deps, "org.apache.maven.surefire", "surefire-shared-utils", VERSION, optional=True)
    jsr305(deps)


def setup_extensions_spi(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../pom.xml")
    add(project, "artifactId", "surefire-extensions-spi")
    add(project, "name", "Surefire Extensions SPI")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.apache.maven.surefire", "surefire-api", VERSION, optional=True)
    jsr305(deps)


def setup_booter(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../pom.xml")
    add(project, "artifactId", "surefire-booter")
    add(project, "name", "Surefire Booter")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.apache.maven.surefire", "surefire-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-extensions-spi", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-shared-utils", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-logger-api", VERSION, optional=True)
    jsr305(deps)


def setup_common_java5(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../../pom.xml")
    add(project, "artifactId", "common-java5")
    add(project, "name", "Surefire Common Java5")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.apache.maven.surefire", "surefire-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-shared-utils", VERSION, optional=True)


def setup_junit_platform(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../../pom.xml")
    add(project, "artifactId", "surefire-junit-platform")
    add(project, "name", "Surefire JUnit Platform Provider")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.apache.maven.surefire", "surefire-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "common-java5", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-shared-utils", VERSION, optional=True)
    dep(deps, "org.junit.platform", "junit-platform-engine", "1.14.4")
    dep(deps, "org.junit.platform", "junit-platform-launcher", "1.14.4")
    dep(deps, "org.junit.jupiter", "junit-jupiter-api", "5.14.4", "provided")
    dep(deps, "org.apiguardian", "apiguardian-api", "1.1.2", "provided")


def setup_common(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../pom.xml")
    add(project, "artifactId", "maven-surefire-common")
    add(project, "name", "Surefire Common")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.slf4j", "slf4j-api", "1.7.36")
    dep(deps, "org.apache.maven.surefire", "surefire-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-logger-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-extensions-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-booter", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-shared-utils", VERSION, optional=True)
    maven_provided(deps)
    dep(deps, "org.apache.maven.resolver", "maven-resolver-util", "2.0.24")
    dep(deps, "org.apache.maven.shared", "maven-common-artifact-filters", "3.4.0")
    dep(deps, "org.codehaus.plexus", "plexus-java", "1.7.0")
    jsr305(deps)


def setup_report_parser(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../pom.xml")
    add(project, "artifactId", "surefire-report-parser")
    add(project, "name", "Surefire Report Parser")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.apache.maven.surefire", "surefire-logger-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.shared", "maven-shared-utils", "3.5.0")


def setup_surefire_plugin(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../pom.xml")
    add(project, "groupId", "org.apache.maven.plugins")
    add(project, "artifactId", "maven-surefire-plugin")
    add(project, "packaging", "maven-plugin")
    add(project, "name", "Maven Surefire Plugin")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.apache.maven.surefire", "surefire-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-extensions-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "maven-surefire-common", VERSION, optional=True)
    maven_provided(deps)
    plugin_descriptor(project)


def setup_failsafe(project):
    add(project, "modelVersion", "4.0.0")
    parent_block(project, "../pom.xml")
    add(project, "groupId", "org.apache.maven.plugins")
    add(project, "artifactId", "maven-failsafe-plugin")
    add(project, "packaging", "maven-plugin")
    add(project, "name", "Maven Failsafe Plugin")
    deps = ET.SubElement(project, tag("dependencies"))
    dep(deps, "org.slf4j", "slf4j-api", "1.7.36")
    dep(deps, "org.apache.maven.surefire", "surefire-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-booter", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-extensions-api", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "surefire-shared-utils", VERSION, optional=True)
    dep(deps, "org.apache.maven.surefire", "maven-surefire-common", VERSION, optional=True)
    maven_provided(deps)
    plugin_descriptor(project)


def named_in(module):
    names = []
    root = Path(module) / "src" / "main" / "java"
    if not root.is_dir():
        return names
    for path in sorted(root.rglob("*.java")):
        text = path.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        text = re.sub(r"//.*?$", "", text, flags=re.M)
        match = re.search(r"\b(?:class|interface|enum)\s+([A-Za-z0-9_]+)", text)
        if not match or "@Named" not in text[: match.start()]:
            continue
        pkg = re.search(r"(?m)^package\s+([A-Za-z0-9_.]+)\s*;", text)
        if pkg:
            names.append(pkg.group(1) + "." + match.group(1))
    return names


def prepare(root: Path):
    for gone in (
        "surefire-its",
        "maven-surefire-report-plugin",
        "surefire-shadefire",
    ):
        path = root / gone
        if path.exists():
            shutil.rmtree(path)
    tests = [path for path in root.rglob("src/test") if path.is_dir()]
    for path in tests:
        shutil.rmtree(path)
    write(root / "pom.xml", setup_parent)
    write(root / "surefire-shared-utils/pom.xml", setup_shared)
    write(root / "surefire-logger-api/pom.xml", setup_logger)
    write(root / "surefire-api/pom.xml", setup_api)
    write(root / "surefire-extensions-api/pom.xml", setup_extensions_api)
    write(root / "surefire-extensions-spi/pom.xml", setup_extensions_spi)
    write(root / "surefire-booter/pom.xml", setup_booter)
    write(root / "surefire-providers/common-java5/pom.xml", setup_common_java5)
    write(root / "surefire-providers/surefire-junit-platform/pom.xml", setup_junit_platform)
    write(root / "maven-surefire-common/pom.xml", setup_common)
    write(root / "surefire-report-parser/pom.xml", setup_report_parser)
    write(root / "maven-surefire-plugin/pom.xml", setup_surefire_plugin)
    write(root / "maven-failsafe-plugin/pom.xml", setup_failsafe)
    names = named_in(root / "maven-surefire-common")
    if len(names) != 3:
        raise SystemExit("expected 3 @Named classes, got " + str(names))
    dest = root / "maven-surefire-common/src/main/resources/META-INF/sisu"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "javax.inject.Named").write_text("\n".join(names) + "\n", encoding="utf-8")
    optional = 0
    for pom in root.rglob("pom.xml"):
        optional += pom.read_text(encoding="utf-8").count("<optional>true</optional>")
    print("named", ", ".join(names))
    print("optional", optional)

prepare(Path("."))
PY

%build -p
python - <<'PY'
from pathlib import Path
count = 0
removed = 0
for path in Path(".").rglob("pom.xml"):
    if ".sysjar" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    found = text.count("<optional>true</optional>")
    count += found
    updated = text.replace("<optional>true</optional>", "")
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        removed += found
if count != 27 or removed != 27:
    raise SystemExit("optional markers " + str(count) + " removed " + str(removed))
PY

%files -f .mfiles
%doc LICENSE README.md
