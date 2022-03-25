# TODO: PLDize SysV init script further
#
# Conditional build:
%bcond_without	lirc	# LIRC driver

Summary:	Driver for Iguanaworks USB IR transceiver
Summary(pl.UTF-8):	Sterownik do nadajnika-odbiornika podczerwieni na USB firmy Iguanaworks
Name:		iguanaIR
Version:	1.2.0
%define	snap	20171020
%define	gitref	9336f121b4127f4ac494e5b26b82ce9c6b86a0ac
%define	rel	6
Release:	1.%{snap}.%{rel}
License:	GPL v2
Group:		Applications/Communications
# formerly (up to 1.1.0): http://www.iguanaworks.net/files/
# now https://github.com/iguanaworks/iguanair/releases /usb_ir- (but 1.2.0 is not tagged)
Source0:	https://github.com/iguanaworks/iguanair/archive/%{gitref}/iguanair-%{snap}.tar.gz
# Source0-md5:	a20ba738cbdf654526190d2b86e70992
Patch0:		%{name}-opt.patch
Patch1:		%{name}-pld.patch
Patch2:		%{name}-lirc.patch
URL:		http://iguanaworks.net/
BuildRequires:	cmake >= 2.6
BuildRequires:	libusb-devel >= 1.0
%{?with_lirc:BuildRequires:	lirc-devel >= 0.9.4}
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	python-devel >= 2
BuildRequires:	python-modules >= 2
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
BuildRequires:	udev-devel
BuildRequires:	systemd-devel >= 1:209
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
Summary:	Python 2 binding for iguanaIR library
Summary(pl.UTF-8):	Interfejs Pythona 2 do biblioteki iguanaIR
License:	GPL v2
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-%{name}
Python 2 binding for iguanaIR library.

%description -n python-%{name} -l pl.UTF-8
Interfejs Pythona 2 do biblioteki iguanaIR.

%package -n python3-%{name}
Summary:	Python 3 binding for iguanaIR library
Summary(pl.UTF-8):	Interfejs Pythona 3 do biblioteki iguanaIR
License:	GPL v2
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python3-%{name}
Python 3 binding for iguanaIR library.

%description -n python3-%{name} -l pl.UTF-8
Interfejs Pythona 3 do biblioteki iguanaIR.

%package -n lirc-plugin-iguanaIR
Summary:	iguanaIR driver for LIRC
Summary(pl.UTF-8):	Sterownik iguanaIR dla LIRC-a
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n lirc-plugin-iguanaIR
iguanaIR driver for LIRC.

%description -n lirc-plugin-iguanaIR -l pl.UTF-8
Sterownik iguanaIR dla LIRC-a.

%prep
%setup -q -n iguanair-%{gitref}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python3}\1,' \
      software/usb_ir/files/python/usr/share/iguanaIR-reflasher/iguanaIR-reflasher

%build
install -d build
cd build
%cmake ../software/usb_ir \
	-DLIBDIR:PATH=%{_libdir}

# j1: version.h vs compile race
%{__make} -j1
cd ..

%if %{with lirc}
CFLAGS="%{rpmcflags}" \
%{__make} -C software/lirc-drv-iguanair \
	CC="%{__cc}" \
	CPPFLAGS="%{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with lirc}
%{__make} -C software/lirc-drv-iguanair install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

install -d $RPM_BUILD_ROOT/etc/rc.d
%{__mv} $RPM_BUILD_ROOT/etc/init.d $RPM_BUILD_ROOT/etc/rc.d
%{__mv} $RPM_BUILD_ROOT/etc/default $RPM_BUILD_ROOT/etc/sysconfig

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%{__rm} software/usb_ir/docs/Makefile

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%triggerpostun libs -- iguanaIR-libs < 1.2.0
rm -f %{_libdir}/libiguanaIR.so.0
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog software/usb_ir/{AUTHORS,README.txt,WHY,docs}
%attr(755,root,root) %{_bindir}/igclient
%attr(755,root,root) %{_bindir}/igdaemon
%attr(755,root,root) %{_bindir}/iguanaIR-reflasher
%attr(755,root,root) %{_bindir}/iguanaIR-rescan
%dir %{_libdir}/iguanaIR
%attr(755,root,root) %{_libdir}/iguanaIR/libusbdrv.so
%dir %{_datadir}/iguanaIR-reflasher
%attr(755,root,root) %{_datadir}/iguanaIR-reflasher/iguanaIR-reflasher
%{_datadir}/iguanaIR-reflasher/hex
/lib/udev/rules.d/80-iguanaIR.rules
%attr(754,root,root) /etc/rc.d/init.d/iguanaIR
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/iguanaIR
%{systemdunitdir}/iguanaIR.service
%{systemdtmpfilesdir}/iguanair.conf
%{_mandir}/man1/igclient.1*
%{_mandir}/man1/iguanaIR-reflasher.1*
%{_mandir}/man1/iguanaIR-rescan.1*
%{_mandir}/man8/igdaemon.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdirectIguanaIR.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdirectIguanaIR.so.0
%attr(755,root,root) %{_libdir}/libiguanaIR.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libiguanaIR.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdirectIguanaIR.so
%attr(755,root,root) %{_libdir}/libiguanaIR.so
%{_includedir}/iguanaIR.h

%files -n python-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_iguanaIR.so
%{py_sitedir}/iguanaIR.py[co]

%files -n python3-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_iguanaIR.so
%{py3_sitedir}/iguanaIR.py
%{py3_sitedir}/__pycache__/iguanaIR.cpython-*.py[co]

%if %{with lirc}
%files -n lirc-plugin-iguanaIR
%doc software/lirc-drv-iguanair/iguanair.txt
%attr(755,root,root) %{_libdir}/lirc/plugins/iguanair.so
%{_datadir}/lirc/configs/iguanair.conf
%{_docdir}/lirc/plugindocs/iguanair.html
/etc/modprobe.d/60-blacklist-kernel-iguanair.conf
%endif
