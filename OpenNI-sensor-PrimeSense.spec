Summary:	PrimeSense Sensor Module for OpenNI framework
Summary(pl.UTF-8):	Moduł czujnika PrimeSense dla szkieletu OpenNI
Name:		OpenNI-sensor-PrimeSense
Version:	5.1.6.6
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/PrimeSense/Sensor/tarball/Stable-%{version}/PrimeSense-%{version}.tar.gz
# Source0-md5:	8d4e082acf75964f109039a87feccc78
Patch0:		%{name}-system-libs.patch
URL:		http://www.primesense.com/
BuildRequires:	OpenNI-devel >= 1.5
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel >= 6:4.0
Requires(post,preun):	OpenNI >= 1.5
# NOTE: other platforms need adding support in OpenNI
ExclusiveArch:	%{ix86} %{x8664} arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86}
%define		openni_platform	x86
%endif
%ifarch %{x8664}
%define		openni_platform	x64
%endif
%ifarch arm
%define		openni_platform	Arm
%endif

%description
PrimeSense Sensor Module for OpenNI framework.

%description -l pl.UTF-8
Moduł czujnika PrimeSense dla szkieletu OpenNI.

%package -n udev-OpenNI-sensor-PrimeSense
Summary:	Udev rules for PrimeSense sensors
Summary(pl.UTF-8):	Reguły udev dla czujników PrimeSense
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	udev-core

%description -n udev-OpenNI-sensor-PrimeSense
Udev rules for PrimeSense sensors.

%description -n udev-OpenNI-sensor-PrimeSense -l pl.UTF-8
Reguły udev dla czujników PrimeSense.

%prep
%setup -q -n PrimeSense-Sensor-9108048
%patch -P0 -p1

%build
%{__make} -C Platform/Linux/Build clean
export CFLAGS="%{rpmcflags}"
%{__make} -C Platform/Linux/Build \
	CFG=PLD \
	CXX="%{__cxx}" \
	HOSTPLATFORM=%{openni_platform}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},/etc/udev/rules.d} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/primesense,/var/log/primesense/XnSensorServer}

BDIR=Platform/Linux/Bin/%{openni_platform}-PLD
install ${BDIR}/XnSensorServer $RPM_BUILD_ROOT%{_bindir}
install ${BDIR}/libXn{Core,DDK,DeviceFile,DeviceSensorV2,Formats}.so $RPM_BUILD_ROOT%{_libdir}
install Data/GlobalDefaults.ini $RPM_BUILD_ROOT%{_sysconfdir}/primesense
install Platform/Linux/Install/55-primesense-usb.rules $RPM_BUILD_ROOT/etc/udev/rules.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
for mod in libXnDeviceSensorV2.so libXnDeviceFile.so ; do
	%{_bindir}/niReg -r %{_libdir}/$mod
done

%preun
if [ "$1" = "0" ]; then
	for mod in libXnDeviceSensorV2.so libXnDeviceFile.so ; do
		%{_bindir}/niReg -u %{_libdir}/$mod
	done
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES NOTICE README
%attr(755,root,root) %{_bindir}/XnSensorServer
%attr(755,root,root) %{_libdir}/libXnCore.so
%attr(755,root,root) %{_libdir}/libXnDDK.so
%attr(755,root,root) %{_libdir}/libXnDeviceFile.so
%attr(755,root,root) %{_libdir}/libXnDeviceSensorV2.so
%attr(755,root,root) %{_libdir}/libXnFormats.so
%dir %{_sysconfdir}/primesense
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/primesense/GlobalDefaults.ini

%files -n udev-OpenNI-sensor-PrimeSense
%defattr(644,root,root,755)
/etc/udev/rules.d/55-primesense-usb.rules
