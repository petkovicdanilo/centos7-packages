%define debug_package %{nil}

Name:           jq
Version:        1.7.1
Release:        1%{?dist}
Summary:        Command-line JSON processor
 
License:        MIT AND ICU AND CC-BY-3.0
URL:            https://jqlang.github.io/jq/
Source0:        https://github.com/jqlang/jq/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
 
BuildRequires:  gcc
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  oniguruma-devel
 
BuildRequires:  valgrind
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
 
# https://github.com/jqlang/jq/pull/3099
# fixes jq --version
Patch:          fix-version-output.patch
 
%description
lightweight and flexible command-line JSON processor
 
 jq is like sed for JSON data – you can use it to slice
 and filter and map and transform structured data with
 the same ease that sed, awk, grep and friends let you
 play with text.
 
 It is written in portable C, and it has zero runtime
 dependencies.
 
 jq can mangle the data format that you have into the
 one that you want with very little effort, and the
 program to do so is often shorter and simpler than
 you'd expect.
 
%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description devel
Development files for %{name}
 
%prep
%autosetup -n %{name}-%{name}-%{version} -p1
 
%build
autoreconf -if
%configure --disable-static
%make_build
# Docs already shipped in jq's tarball.
# In order to build the manual page, it
# is necessary to install rake, rubygem-ronn
# and do the following steps:
#
# # yum install rake rubygem-ronn
# $ cd docs/
# $ curl -L https://get.rvm.io | bash -s stable --ruby=1.9.3
# $ source $HOME/.rvm/scripts/rvm
# $ bundle install
# $ cd ..
# $ ./configure
# $ make real_docs
 
%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
 
# Delete build-time RPATH that is unnecessary on an installed
# system - rhbz#1987608
chrpath -d %{buildroot}%{_bindir}/%{name}
 
%check
make check
 
%files
%license COPYING
%doc AUTHORS COPYING NEWS.md README.md
%{_bindir}/%{name}
%{_libdir}/libjq.so.*
%{_datadir}/man/man1/jq.1.gz
 
%files devel
%{_includedir}/jq.h
%{_includedir}/jv.h
%{_libdir}/libjq.so
%{_libdir}/pkgconfig/libjq.pc
 
%changelog
* Mon Jan 06 2025 Danilo Petkovic <petkovicdanilo97@gmail.com> - 1.7.1-1
- Initial RPM release.
 