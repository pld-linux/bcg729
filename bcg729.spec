#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	ITU G729 Annex A speech codec library
Summary(pl.UTF-8):	Biblioteka kodeka mowy ITU G729 Annex A
Name:		bcg729
Version:	1.1.1
Release:	2
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bcg729/tags
Source0:	https://gitlab.linphone.org/BC/public/bcg729/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	23b0c28422df3251adbc81e596ef9861
Patch0:		%{name}-git.patch
URL:		https://www.linphone.org/technical-corner/bcg729
BuildRequires:	cmake >= 3.22
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.745
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

%prep
%setup -q
%patch0 -p1

%build
%if %{with static_libs}
%cmake -B builddir-static \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DBUILD_SHARED_LIBS=OFF

%{__make} -C builddir-static
%endif

%cmake -B builddir \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make} -C builddir

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C builddir-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md README.md
%attr(755,root,root) %{_libdir}/libbcg729.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbcg729.so
%{_includedir}/bcg729
%{_pkgconfigdir}/libbcg729.pc
%dir %{_datadir}/BCG729
%{_datadir}/BCG729/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbcg729.a
%endif
