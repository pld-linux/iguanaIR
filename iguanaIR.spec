# TODO: PLDize init script, use /etc/sysconfig instead of /etc/default
Summary:	Driver for Iguanaworks USB IR transceiver
Summary(pl.UTF-8):	Sterownik do nadajnika-odbiornika podczerwieni na USB firmy Iguanaworks
Name:		iguanaIR
Version:	1.0.1
Release:	2
License:	GPL v2
Group:		Applications/Communications
Source0:	http://iguanaworks.net/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	cf9e6e7939ff9d76aa985fab8c6f5af7
Patch0:		%{name}-opt.patch
URL:		http://iguanaworks.net/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	libusb-compat-devel >= 0.1.0
BuildRequires:	popt-devel
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python >= 1.3.31
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	udev-iguanaIR
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Driver for Iguanaworks USB IR transceiver.

%description -l pl.UTF-8
Sterownik do nadajnika-odbiornika podczerwieni na USB firmy
Iguanaworks.

%package libs
Summary:	iguanaIR shared library
Summary(pl.UTF-8):	Biblioteka współdzielona iguanaIR
License:	LGPL v2.1
Group:		Libraries

%description libs
iguanaIR shared library for Iguanaforks USB IR transceiver.

%description libs -l pl.UTF-8
Biblioteka współdzielona iguanaIR do nadajnika-odbiornika podczerwieni
na USB firmy Iguanaworks.

%package devel
Summary:	Header files for iguanaIR library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki iguanaIR
License:	LGPL v2.1
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for iguanaIR library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki iguanaIR.

%package -n python-%{name}
Summary:	Python binding for iguanaIR library
Summary(pl.UTF-8):	Interfejs Pythona do biblioteki iguanaIR
License:	GPL v2
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-%{name}
Python binding for iguanaIR library.

%description -n python-%{name} -l pl.UTF-8
Interfejs Pythona do biblioteki iguanaIR.

%prep
%setup -q
%patch0 -p1

%build
cd autoconf
%{__aclocal}
%{__autoconf} --output=../configure
%{__autoheader}
cd ..
%configure \
	PYTHON_SITE_PKG=%{py_sitedir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d
mv -f $RPM_BUILD_ROOT/etc/init.d $RPM_BUILD_ROOT/etc/rc.d

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%{__rm} docs/Makefile

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.txt WHY docs
%attr(755,root,root) %{_bindir}/igclient
%attr(755,root,root) %{_bindir}/igdaemon
%attr(755,root,root) %{_bindir}/iguanaIR-reflasher
%dir %{_libdir}/iguanaIR
%attr(755,root,root) %{_libdir}/iguanaIR/*.so
%dir %{_libdir}/iguanaIR-reflasher
%attr(755,root,root) %{_libdir}/iguanaIR-reflasher/iguanaIR-reflasher
%{_libdir}/iguanaIR-reflasher/hex
/lib/udev/rules.d/80-iguanaIR.rules
%attr(754,root,root) /etc/rc.d/init.d/iguanaIR

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libiguanaIR.so.0

%files devel
%defattr(644,root,root,755)
%doc protocols.txt
%attr(755,root,root) %{_libdir}/libiguanaIR.so
%{_includedir}/iguanaIR.h

%files -n python-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_iguanaIR.so
%{py_sitedir}/iguanaIR.py[co]
