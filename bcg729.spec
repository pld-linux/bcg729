#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	ITU G729 Annex A speech codec library
Summary(pl.UTF-8):	Biblioteka kodeka mowy ITU G729 Annex A
Name:		bcg729
Version:	1.1.1
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bcg729/tags
Source0:	https://gitlab.linphone.org/BC/public/bcg729/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	23b0c28422df3251adbc81e596ef9861
URL:		http://www.linphone.org/technical-corner/bcg729
BuildRequires:	cmake >= 3.1
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

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{!?with_static_libs:-DENABLE_STATIC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_datadir}/Bcg729/cmake/Bcg729Targets.cmake

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
%dir %{_datadir}/Bcg729
%{_datadir}/Bcg729/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbcg729.a
%endif
