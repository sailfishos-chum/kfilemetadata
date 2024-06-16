%global kf5_version 5.116.0

%global         ffmpeg 1
#global         catdoc 1
#global         ebook 1
#global         poppler 1
%global         taglib 1

Name: opt-kf5-kfilemetadata
Summary:        A Tier 2 KDE Framework for extracting file metadata
Version: 5.116.0
Release:        1%{?dist}

# # KDE e.V. may determine that future LGPL versions are accepted
License:        LGPLv2 or LGPLv3
URL:            https://cgit.kde.org/kfilemetadata
Source0: %{name}-%{version}.tar.bz2

# filter plugin provides
%global __provides_exclude_from ^(%{_opt_qt5_plugindir}/.*\\.so)$
%{?opt_kf5_default_filter}

BuildRequires: opt-extra-cmake-modules >= %{kf5_version}
#BuildRequires: kdegraphics-mobipocket-devel
BuildRequires: opt-kf5-karchive-devel >= %{kf5_version}
BuildRequires: opt-kf5-kcoreaddons-devel >= %{kf5_version}
BuildRequires: opt-kf5-ki18n-devel >= %{kf5_version}
BuildRequires: opt-kf5-rpm-macros
# optional
BuildRequires: opt-kf5-kconfig-devel >= %{kf5_version}

BuildRequires: opt-qt5-qtbase-devel

BuildRequires:  libattr-devel
#BuildRequires:  pkgconfig(exiv2) >= 0.20

## optional deps
%if 0%{?catdoc}
# not strictly required at build-time, satisfying runtime dep check only
BuildRequires:  catdoc
Recommends:     catdoc
%endif
%if 0%{?ebook}
BuildRequires:  ebook-tools-devel
%endif
%if 0%{?ffmpeg}
BuildRequires:  ffmpeg-devel
%endif
%if 0%{?poppler}
BuildRequires:  pkgconfig(poppler-qt5)
%endif
%if 0%{?taglib}
BuildRequires:  pkgconfig(taglib) >= 1.9
%endif

%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
Requires: opt-kf5-karchive >= %{kf5_version}
Requires: opt-kf5-kcoreaddons >= %{kf5_version}
Requires: opt-kf5-ki18n >= %{kf5_version}

%description
%{summary}.

%package devel
Summary:        Developer files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel
%description devel
%{summary}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%_opt_cmake_kf5 ../

%make_build

popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd

%find_lang %{name} --all-name

mkdir -p %{buildroot}%{_opt_qt5_plugindir}/kf5/kfilemetadata/writers/


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSES/*.txt
%{_opt_kf5_datadir}/qlogging-categories5/kfilemetadata*
%{_opt_kf5_libdir}/libKF5FileMetaData.so.*
%{_opt_kf5_datadir}/locale/

# consider putting these into some subpkg ?
%dir %{_opt_qt5_plugindir}/kf5/kfilemetadata/
%{_opt_qt5_plugindir}/kf5/kfilemetadata/kfilemetadata_*.so
%dir %{_opt_qt5_plugindir}/kf5/kfilemetadata/writers/
%if 0%{?taglib}
%{_opt_qt5_plugindir}/kf5/kfilemetadata/writers/kfilemetadata_taglibwriter.so
%endif

%files devel
%{_opt_kf5_libdir}/libKF5FileMetaData.so
%{_opt_kf5_libdir}/cmake/KF5FileMetaData
%{_opt_kf5_includedir}/KF5/KFileMetaData/
%{_opt_kf5_archdatadir}/mkspecs/modules/qt_KFileMetaData.pri
