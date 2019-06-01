#
# Conditional build:
%bcond_without	mediastreamer	# mediastreamer plugin

Summary:	ITU G729 Annex A speech codec library
Summary(pl.UTF-8):	Biblioteka kodeka mowy ITU G729 Annex A
Name:		bcg729
Version:	1.0.2
Release:	2
License:	GPL v2+, ITU G729 patent license may be required
Group:		Libraries
Source0:	http://download-mirror.savannah.gnu.org/releases/linphone/plugins/sources/%{name}-%{version}.tar.gz
# Source0-md5:	2a3d9b422912024f97a41e56e9e3d357
Patch0:		%{name}-lib.patch
URL:		http://www.linphone.org/eng/documentation/dev/bcg729.html
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	libtool >= 2:2
%{?with_mediastreamer:BuildRequires:	mediastreamer-devel >= 2.9.0}
%{?with_mediastreamer:BuildRequires:	ortp-devel >= 0.21.0}
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
bcg729 is an opensource implementation of both encoder and decoder of
the ITU G729 Annex A speech codec. The library written in C99 is fully
portable and can be executed on many platforms including both ARM
processor and x86. libbcg729 supports concurrent channels
encoding/decoding for multi call application such conferencing. This
project was initially developed as part of Mediastreamer2, the
Linphone's media processing engine. So there is also available the
glue to be integrated in Linphone/Mediastreamer2.

%description -l pl.UTF-8
bcg729 to implementacja o otwartych źródłach kodera oraz dekorera
kodeka mowy ITU G729 Annex A. Biblioteka napisana w dialekcie C99 jest
w pełni przenośna i może być uruchamiana na wielu platformach, w tym
procesorach ARM i x86. libbcg729 obsługuje jednoczesne
kodowanie/dekodowanie wielu kanałów dla zastosowań z wieloma
rozmowami,takich jak konferencje. Ten projekt początkowo był częścią
Mediastreamera2 - silnika przetwarzania multimediów programu Linphone.
Dlatego jest też dostępny kod łączący z Linphonem/Mediastreamerem2.

%package devel
Summary:	Header files for bcg729 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki bcg729
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for bcg729 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki bcg729.

%package static
Summary:	Static bcg729 library
Summary(pl.UTF-8):	Statyczna biblioteka bcg729
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static bcg729 library.

%description static -l pl.UTF-8
Statyczna biblioteka bcg729.

%package -n mediastreamer-plugin-msbcg729
Summary:	ITU G729 Annex A speech codec for mediastreamer
Summary(pl.UTF-8):	Kodek mowy ITU G729 Annex A dla mediastreamera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	mediastreamer >= 2.9.0

%description -n mediastreamer-plugin-msbcg729
This package supplies the mediastreamer plugin for the ITU G729 Annex
A speech codec.

%description -n mediastreamer-plugin-msbcg729 -l pl.UTF-8
Ten pakiet udostępnia wtyczkę mediastreamera do kodeka mowy ITU G729
Annex A.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_mediastreamer:--disable-msplugin} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# dlopened plugin
%{__rm} $RPM_BUILD_ROOT%{_libdir}/mediastreamer/plugins/libmsbcg729.{la,a}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbcg729.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libbcg729.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbcg729.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbcg729.so
%{_includedir}/bcg729
%{_pkgconfigdir}/libbcg729.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libbcg729.a

%if %{with mediastreamer}
%files -n mediastreamer-plugin-msbcg729
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mediastreamer/plugins/libmsbcg729.so*
%endif
