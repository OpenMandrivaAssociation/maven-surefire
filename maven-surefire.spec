# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'
%define _without_maven 1
%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define maven_settings_file %{_builddir}/%{name}/settings.xml

Name:           maven-surefire
Version:        2.3
Release:        %mkrel 1.0.2
Epoch:          0
Summary:        Surefire is a test framework project
License:        Apache Software License
Group:          Development/Java
URL:            http://maven.apache.org/surefire/

Source0:        %{name}-%{version}.tar.gz
# svn export http://svn.apache.org/repos/asf/maven/surefire/tags/surefire-2.3 maven-surefire-2.3
Source1:        %{name}-settings.xml
Source2:        %{name}-jpp-depmap.xml
Source3:        %{name}-build.tar.gz
Source4:        %{name}-plugin.xml
Source5:        %{name}-report-plugin.xml

Patch0:         maven-surefire-2.3-Commandline.patch
Patch1:         maven-surefire-2.3-CommandShell.patch
Patch2:         maven-surefire-2.3-CmdShell.patch
Patch3:         maven-surefire-2.3-junit4-pom.patch
Patch4:         maven-surefire-2.3-testng-TestNGXmlTestSuite.patch
Patch5:         maven-surefire-2.3-testng-TestNGDirectoryTestSuite.patch
Patch6:         maven-surefire-2.3-providers-pom.patch
Patch7:         maven-surefire-2.3-ForkConfiguration.patch
Patch8:         maven-surefire-2.3-SurefireBooter.patch


%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-rpmbuild 
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit
BuildRequires:  ant-nodeps
BuildRequires:  classworlds
BuildRequires:  jmock
BuildRequires:  junit >= 3.8.2
BuildRequires:  junit4
#BuildRequires:  maven-shared-plugin-testing-harness
BuildRequires:  plexus-archiver
BuildRequires:  plexus-utils
BuildRequires:  testng

%if %{with_maven}
BuildRequires:  maven2 
BuildRequires:  maven2-plugin-ant
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-plugin
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-site
BuildRequires:  maven2-plugin-surefire
BuildRequires:  maven2-common-poms >= 0:1.0-3
%endif


Requires:       classworlds
Requires:       plexus-utils
Requires:       junit

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
%endif

%description
Surefire is a test framework project.

%package booter
Summary:         Booter for %{name}
Group:           Development/Java
Requires:        %{name} = %{epoch}:%{version}-%{release}
Requires:        plexus-archiver
Requires:        plexus-container-default
Requires:        plexus-utils

%description booter
%{summary}.

%package junit
Summary:         JUnit3 Runner for %{name}
Group:           Development/Java
Requires:        %{name} = %{epoch}:%{version}-%{release}
Requires:        junit

%description junit
%{summary}.

%package junit4
Summary:         JUnit4 Runner for %{name}
Group:           Development/Java
Requires:        %{name} = %{epoch}:%{version}-%{release}
Requires:        junit4

%description junit4
%{summary}.

%package testng
Summary:         TestNG Runner for %{name}
Group:           Development/Java
Requires:        %{name} = %{epoch}:%{version}-%{release}
Requires:        plexus-utils
Requires:        testng

%description testng
%{summary}.

%if %{with_maven}
%package plugin
Summary:         Maven2 Plugin for %{name}
Group:           Development/Java
Requires:        %{name} = %{epoch}:%{version}-%{release}
Requires:        %{name}-booter = %{epoch}:%{version}-%{release}
Requires:        %{name}-junit = %{epoch}:%{version}-%{release}
Requires:        %{name}-junit4 = %{epoch}:%{version}-%{release}
Requires:        %{name}-testng = %{epoch}:%{version}-%{release}
Requires:        maven2
Requires:        plexus-utils
Obsoletes:       maven2-plugin-surefire < 0:2.0.7
Provides:        maven2-plugin-surefire = %{epoch}:%{version}-%{release}

%description plugin
%{summary}.

%package report-plugin
Summary:         Maven2 Report Plugin for %{name}
Group:           Development/Java
Requires:        %{name} = %{epoch}:%{version}-%{release}
Requires:        %{name}-booter = %{epoch}:%{version}-%{release}
Requires:        maven2
Requires:        maven-doxia
Requires:        plexus-utils
Obsoletes:       maven2-plugin-surefire-report < 0:2.0.7
Provides:        maven2-plugin-surefire-report = %{epoch}:%{version}-%{release}

%description report-plugin
%{summary}.
%endif

%package javadoc
Summary:        Javadoc for %{name} API
Group:          Development/Java

%description javadoc
%{summary}.

%package booter-javadoc
Summary:        Javadoc for %{name} Booter
Group:          Development/Java

%description booter-javadoc
%{summary}.

%package junit-javadoc
Summary:        Javadoc for %{name} JUnit3 Runner
Group:          Development/Java

%description junit-javadoc
%{summary}.

%package junit4-javadoc
Summary:        Javadoc for %{name} JUnit4 Runner
Group:          Development/Java

%description junit4-javadoc
%{summary}.

%package testng-javadoc
Summary:        Javadoc for %{name} TestNG Runner
Group:          Development/Java

%description testng-javadoc
%{summary}.

%prep
%setup -q
cp %{SOURCE1} settings.xml
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

gzip -dc %{SOURCE3} | tar xf -

sed -i -e s:"private static void failSame(":"public static void failSame(":g \
    surefire-api/src/main/java/org/apache/maven/surefire/assertion/SurefireAssert.java
sed -i -e s:"private static void failNotSame(":"public static void failNotSame(":g \
    surefire-api/src/main/java/org/apache/maven/surefire/assertion/SurefireAssert.java
sed -i -e s:"private static void failNotEquals(":"public static void failNotEquals(":g \
    surefire-api/src/main/java/org/apache/maven/surefire/assertion/SurefireAssert.java
%patch0 -b .sav0
%patch1 -b .sav1
%patch2 -b .sav2
%patch3 -b .sav3
%patch4 -b .sav4
%patch5 -b .sav4
%patch6 -b .sav6
%patch7 -b .sav7
%patch8 -b .sav8

for i in \
    maven-surefire-report-plugin/src/main/java/org/apache/maven/plugins/surefire/report/SurefireReportGenerator.java \
    maven-surefire-report-plugin/src/main/java/org/apache/maven/plugins/surefire/report/SurefireReportMojo.java; do

        sed -i -e s:org.codehaus.doxia.sink.Sink:org.apache.maven.doxia.sink.Sink:g $i
        sed -i -e s:org.codehaus.doxia.site.renderer.SiteRenderer:org.apache.maven.doxia.siterenderer.Renderer:g $i
        sed -i -r -e s:\(\\s+\)SiteRenderer\(\\s+\):\\1Renderer\\2:g $i
done


%build
export JAVA_HOME=%{_jvmdir}/java-rpmbuild
%if %{with_maven}
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
rm -rf surefire-api/src/test
rm -rf surefire-booter/src/test
rm -rf maven-surefire-report-plugin/src/test
mvn-jpp \
        -e \
        -s settings.xml \
        -Dmaven.test.failure.ignore=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven2.jpp.depmap.file=%{SOURCE2} \
        ant:ant install javadoc:javadoc
%else
export CLASSPATH=$(build-classpath \
commons-lang \
plexus/utils \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
pushd surefire-api
%{ant} -Dbuild.sysclasspath=only jar javadoc
popd
export CLASSPATH=$(build-classpath \
plexus/archiver \
plexus/containers-component-api \
plexus/utils \
)
CLASSPATH=$CLASSPATH:$(pwd)/surefire-api/target/surefire-api-%{version}.jar
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
pushd surefire-booter
%{ant} -Dbuild.sysclasspath=only jar javadoc
popd
export CLASSPATH=$(build-classpath \
junit \
)
CLASSPATH=$CLASSPATH:$(pwd)/surefire-api/target/surefire-api-%{version}.jar
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
pushd surefire-providers/surefire-junit
%{ant} -Dbuild.sysclasspath=only jar javadoc
popd
export CLASSPATH=$(build-classpath \
junit4 \
)
CLASSPATH=$CLASSPATH:$(pwd)/surefire-api/target/surefire-api-%{version}.jar
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
pushd surefire-providers/surefire-junit4
%{ant} -Dbuild.sysclasspath=only jar javadoc
popd
export CLASSPATH=$(build-classpath \
plexus/utils \
testng-jdk15 \
)
CLASSPATH=$CLASSPATH:$(pwd)/surefire-api/target/surefire-api-%{version}.jar
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
pushd surefire-providers/surefire-testng
%{ant} -Dbuild.sysclasspath=only jar javadoc
popd
%if %{with_maven}
export CLASSPATH=$(build-classpath \
maven2/artifact \
maven2/artifact-manager \
maven2/plugin-api \
plexus/utils \
)
CLASSPATH=$CLASSPATH:$(pwd)/surefire-api/target/surefire-api-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/surefire-booter/target/surefire-booter-%{version}.jar
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
pushd maven-surefire-plugin
mkdir -p target/classes/META-INF/maven/org.apache.maven.plugins/maven-surefire-plugin/
cp pom.xml target/classes/META-INF/maven/org.apache.maven.plugins/maven-surefire-plugin/
cp %{SOURCE4} target/classes/META-INF/maven/plugin.xml
cat > target/classes/META-INF/maven/org.apache.maven.plugins/maven-surefire-plugin/pom.properties <<EOT
version=2.3
groupId=org.apache.maven.plugins
artifactId=maven-surefire-plugin
EOT
%{ant} -Dbuild.sysclasspath=only jar
popd
export CLASSPATH=$(build-classpath \
maven2/artifact \
maven2/model \
maven2/plugin-api \
maven2/project \
maven2/reporting-api \
maven2/reporting-impl \
maven-doxia/sink \
maven-doxia/site-renderer \
maven-shared/reporting-impl \
plexus/utils \
)
CLASSPATH=$CLASSPATH:$(pwd)/surefire-api/target/surefire-api-%{version}.jar
CLASSPATH=$CLASSPATH:$(pwd)/surefire-booter/target/surefire-booter-%{version}.jar
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
pushd maven-surefire-report-plugin
mkdir -p target/classes/META-INF/maven/org.apache.maven.plugins/maven-surefire-report-plugin/
cp pom.xml target/classes/META-INF/maven/org.apache.maven.plugins/maven-surefire-report-plugin/
cp %{SOURCE5} target/classes/META-INF/maven/plugin.xml
cat > target/classes/META-INF/maven/org.apache.maven.plugins/maven-surefire-report-plugin/pom.properties <<EOT
version=2.3
groupId=org.apache.maven.plugins
artifactId=maven-surefire-report-plugin
EOT
%{ant} -Dbuild.sysclasspath=only jar
popd
%endif
%endif


%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/maven-surefire
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/plugins
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms

install -m 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-surefire.pom
%add_to_maven_depmap org.apache.maven.surefire surefire %{version} JPP/maven-surefire surefire

install -m 644 surefire-api/target/surefire-api-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/maven-surefire/api-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-api %{version} JPP/maven-surefire api
install -m 644 surefire-api/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-api.pom

install -m 644 surefire-booter/target/surefire-booter-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/maven-surefire/booter-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-booter %{version} JPP/maven-surefire booter
install -m 644 surefire-booter/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-booter.pom

install -m 644 surefire-providers/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-providers.pom
%add_to_maven_depmap org.apache.maven.surefire surefire-providers %{version} JPP/maven-surefire providers

install -m 644 surefire-providers/surefire-junit4/target/surefire-junit4-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/maven-surefire/junit4-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-junit4 %{version} JPP/maven-surefire junit4
install -m 644 surefire-providers/surefire-junit4/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-junit4.pom

install -m 644 surefire-providers/surefire-junit/target/surefire-junit-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/maven-surefire/junit-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-junit %{version} JPP/maven-surefire junit
install -m 644 surefire-providers/surefire-junit/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-junit.pom

install -m 644 surefire-providers/surefire-testng/target/surefire-testng-%{version}.jar \
    $RPM_BUILD_ROOT%{_javadir}/maven-surefire/testng-%{version}.jar
%add_to_maven_depmap org.apache.maven.surefire surefire-testng %{version} JPP/maven-surefire testng
install -m 644 surefire-providers/surefire-testng/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven-surefire-testng.pom

%if %{with_maven}
install -m 644 maven-surefire-plugin/target/maven-surefire-plugin-%{version}.jar \
    $RPM_BUILD_ROOT%{_datadir}/maven2/plugins/surefire-plugin-%{version}.jar
%add_to_maven_depmap org.apache.maven.plugins maven-surefire-plugin %{version} JPP/maven2/plugins surefire-plugin
install -m 644 maven-surefire-plugin/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven2.plugins-surefire-plugin.pom

install -m 644 maven-surefire-report-plugin/target/maven-surefire-report-plugin-%{version}.jar \
    $RPM_BUILD_ROOT%{_datadir}/maven2/plugins/surefire-report-plugin-%{version}.jar
%add_to_maven_depmap org.apache.maven.plugins maven-surefire-report-plugin %{version} JPP/maven2/plugins surefire-report-plugin
install -m 644 maven-surefire-report-plugin/pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.maven2.plugins-surefire-report-plugin.pom
%endif

(cd $RPM_BUILD_ROOT%{_javadir}/maven-surefire && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir}/maven-surefire && ln -sf api.jar surefire.jar)
%if %{with_maven}
(cd $RPM_BUILD_ROOT%{_datadir}/maven2/plugins && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
%endif
# javadoc

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-api-%{version}
cp -pr surefire-api/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-api-%{version}
ln -s %{name}-api-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-api # ghost symlink
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-booter-%{version}
cp -pr surefire-booter/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-booter-%{version}
ln -s %{name}-booter-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-booter # ghost symlink
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-junit4-%{version}
cp -pr surefire-providers/surefire-junit4/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-junit4-%{version}
ln -s %{name}-junit4-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-junit4 # ghost symlink
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-junit-%{version}
cp -pr surefire-providers/surefire-junit/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-junit-%{version}
ln -s %{name}-junit-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-junit # ghost symlink
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testng-%{version}
cp -pr surefire-providers/surefire-testng/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testng-%{version}
ln -s %{name}-testng-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}-testng # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%if %{gcj_support}
%post booter
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun booter
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%dir %{_javadir}/maven-surefire
%{_javadir}/maven-surefire/api*
%{_javadir}/maven-surefire/surefire.jar
%dir %{_datadir}/maven2
%dir %{_datadir}/maven2/poms
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files booter
%defattr(-,root,root,-)
%{_javadir}/maven-surefire/booter*

%files junit
%defattr(-,root,root,-)
%{_javadir}/maven-surefire/junit-%{version}.jar
%{_javadir}/maven-surefire/junit.jar

%files junit4
%defattr(-,root,root,-)
%{_javadir}/maven-surefire/junit4-%{version}.jar
%{_javadir}/maven-surefire/junit4.jar

%files testng
%defattr(-,root,root,-)
%{_javadir}/maven-surefire/testng*

%if %{with_maven}
%files plugin
%defattr(-,root,root,-)
%dir %{_datadir}/maven2/plugins
%{_datadir}/maven2/plugins/surefire-plugin*

%files report-plugin
%defattr(-,root,root,-)
%dir %{_datadir}/maven2/plugins
%{_datadir}/maven2/plugins/surefire-report-plugin*
%endif

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/maven-surefire-api-%{version}
%doc %{_javadocdir}/maven-surefire-api

%files booter-javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/maven-surefire-booter-%{version}
%doc %{_javadocdir}/maven-surefire-booter

%files junit-javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/maven-surefire-junit-%{version}
%doc %{_javadocdir}/maven-surefire-junit

%files junit4-javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/maven-surefire-junit4-%{version}
%doc %{_javadocdir}/maven-surefire-junit4

%files testng-javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/maven-surefire-testng-%{version}
%doc %{_javadocdir}/maven-surefire-testng
