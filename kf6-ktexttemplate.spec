#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.21
%define		qtver		5.15.2
%define		kfname		ktexttemplate

Summary:	Text template
Name:		kf6-%{kfname}
Version:	6.21.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	13a14d46983d6d0a51380fba003c61ef
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KTextTemplate.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/libKF6TextTemplate.so.*.*
%ghost %{_libdir}/libKF6TextTemplate.so.6
%dir %{_libdir}/qt6/plugins/kf6/ktexttemplate
%{_libdir}/qt6/plugins/kf6/ktexttemplate/ktexttemplate_defaultfilters.so
%{_libdir}/qt6/plugins/kf6/ktexttemplate/ktexttemplate_defaulttags.so
%{_libdir}/qt6/plugins/kf6/ktexttemplate/ktexttemplate_i18ntags.so
%{_libdir}/qt6/plugins/kf6/ktexttemplate/ktexttemplate_loadertags.so
%{_datadir}/qlogging-categories6/ktexttemplate.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KTextTemplate
%{_libdir}/cmake/KF6TextTemplate
%{_libdir}/libKF6TextTemplate.so
