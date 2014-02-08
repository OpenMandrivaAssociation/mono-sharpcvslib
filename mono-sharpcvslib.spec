Summary:	Client cvs library written in C sharp
Name:		mono-sharpcvslib
Version:	0.35
Release:	5
# Exception: Permission is given to use this library in commercial closed-source applications
# See: README.txt
License:	GPLv2+ with exceptions
Group:		Development/Other
Url:		http://sharpcvslib.sourceforge.net/
# Upstream Source is here: http://downloads.sourceforge.net/sharpcvslib/SharpCvsLib-0.35.3721.507-src.zip
# Unfortunately, they use windows separators. This is the same thing, just rezipped with unix separators.
Source0:	SharpCvsLib-0.35.3721.507-src-unix.zip
Source1:	sharpcvslib.pc
Patch0:		sharpcvslib-cleanups.patch
Patch1:		sharpcvslib-key.patch
BuildArch:	noarch
BuildRequires:	unzip
BuildRequires:	pkgconfig(log4net)
BuildRequires:	pkgconfig(nant)
BuildRequires:	pkgconfig(nunit22)

%description
Gives C sharp projects the ability to communicate with a CVS server.

%package devel
Summary:	Client cvs library written in C sharp
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
Gives C sharp projects the ability to communicate with a CVS server.

%prep
%setup -q -c -n sharpcvslib-%{version}
# We need this to compile.
%apply_patches
# Get rid of the binary dlls
rm -rf src/lib/*
rm -rf src/tools/nant/*
# There is probably a better way to do this, but this works.
# All these guys are built from source.
mkdir -p src/lib/ext/
cp %{_prefix}/lib/mono/log4net/log4net.dll src/lib/ext/
cp %{_prefix}/lib/mono/2.0/ICSharpCode.SharpZipLib.dll src/lib/
cp %{_prefix}/lib/mono/nunit22/nunit.framework.dll src/lib/ext/
sed -i 's/\r//' src/doc/README.txt
sed -i 's/\r//' src/doc/COPYING.txt

%build
# Use the mono system key instead of generating our own here.
%if %mdvver >= 201100
cp -a /etc/pki/mono/mono.snk SharpCvsLib.snk
%else
sn -k SharpCvsLib.snk
%endif
cd src/build
nant -buildfile:SharpCvsLib.build -D:compile.warnaserror=false build.all
# This command works mostly, but fails at the end trying to talk to the Windows registry.
nant -buildfile:SharpCvsLib.build netdoc ||:



%install
mkdir -p %{buildroot}/%{_datadir}/pkgconfig
cp %{SOURCE1} %{buildroot}/%{_datadir}/pkgconfig
mkdir -p %{buildroot}/%{_prefix}/lib/mono/gac/
gacutil -i src/bin/cvs.exe -f -package sharpcvslib -root %{buildroot}/%{_prefix}/lib/
gacutil -i src/bin/ICSharpCode.SharpCvsLib.dll -f -package sharpcvslib -root %{buildroot}/%{_prefix}/lib
gacutil -i src/bin/ICSharpCode.SharpCvsLib.Tests.dll -f -package sharpcvslib -root %{buildroot}/%{_prefix}/lib
gacutil -i src/bin/ICSharpCode.SharpCvsLib.Tests-sample.dll -f -package sharpcvslib -root %{buildroot}/%{_prefix}/lib

# Cleanup docs
sed -i 's/\r//' src/doc/api/msdn/SharpCvsLib.log
sed -i 's/\r//' src/doc/api/msdn/SharpCvsLib.hhp
sed -i 's/\r//' src/doc/api/msdn/tree.css
sed -i 's/\r//' src/doc/api/msdn/MSDN.css
sed -i 's/\r//' src/doc/api/msdn/tree.js
iconv -f iso-8859-1 -t utf-8 -o src/doc/api/msdn/tree.js{.utf8,}
mv src/doc/api/msdn/tree.js{.utf8,}

%files
%doc src/doc/README.txt src/doc/COPYING.txt src/doc/*.html
%doc src/doc/images/
%{_prefix}/lib/mono/gac/cvs/
%{_prefix}/lib/mono/gac/ICSharpCode.SharpCvsLib*/
%{_prefix}/lib/mono/sharpcvslib/

%files devel
%doc src/doc/api/
%{_datadir}/pkgconfig/sharpcvslib.pc

