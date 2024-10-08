# This file is autogenerated by running
#  ./dhs/precheckin.sh 
# Please edit droid-src-sony-ganges.spec.tmpl and re-run that command to modify

# Copy this file to your device tree, next to the .spec and dhs submodule
# Replace @...@ accordingly

# device is the codename for the device
%define device kirin

%define ha_device_override sony-ganges

# repo service performed : %%include define-trees
%define dhs_trees build development libcore platform_testing toolchain compatibility device libnativehelper prebuilts tools art cts external vendor bionic dalvik frameworks sdk bootable hardware packages system developers kernel pdk test

%define device_variant -user
%define lunch_device aosp_i4113
%define pre_actions sudo update-java-alternatives -s java-1.8.0-openjdk-amd64

%define post_build_actions mv rpm/patches patches; /bin/sh ./rpm/apply-patches.sh

# Our promotions fail, because rpm v4.9 can't handle conditional macros well, see JB#33275
# Let's work around it for now:
%define dhs_name_hardcoded droid-src-%{ha_device_override}
# If dhs_flavour is set to e.g. syspart, then the hardcoded name should be:
#define dhs_name_hardcoded droid-src-syspart-%{ha_device_override}

%define dhs_sources \
Source52: %{dhs_name_hardcoded}.spec.tmpl\
Source53: source.paths\
Source54: apply-patches.sh\
%{nil}

# repo service performed : %%include dhs/droid-hal-source.inc
# This file should be %%included into a device specific spec file
# where macros are defined:
# device:            should be the CM codename or the AOSP TARGET_PRODUCT
# hadk_make_target:  the target used when running make in the HABUILD_SDK on the
#                      OBS. Defaults to "hybris-hal"
# device_variant:    for AOSP this is used as the TARGET_BUILD_VARIANT for lunch
# lunch_device:      cases where the lunch combo is different from device name.
#                      For example, it's "aosp_f5121" for the "suzu" device
# have_vendor_src_for_obs:
#                    include a separately packaged vendor source for OBS builds
# post_build_actions:
#                    Actions to be executed after the sources have been extracted
#                    for example patches can be applied to the sources which are
#                    then stored in the final rpm droid-src packages.


%define __provides_exclude_from ^%{_libexecdir}/droid-hybris/.*$
%define android_root .

%define __find_provides %{nil}
%define __find_requires %{nil}
%define __strip /bin/true
%define __provides_exclude_from ^/system/.*$
%define __requires_exclude ^.*$
%global debug_package %{nil}

# Support build info extracted from OBS builds too
%if 0%{?_obs_build_project:1}
%define _build_flavour %(echo %{_obs_build_project} | awk -F : '{if ($NF == "testing" || $NF == "release") print $NF; else if ($NF ~ /[0-9]\.[0-9]\.[0-9]/ && NF == 3) print strdevel; else if (NF == 2) print strdevel; else print strunknown}' strdevel=devel strunknown=unknown)
%else
%define _build_flavour unknown
%endif

%define _obs_build_count %(echo %{release} | awk -F . '{if (NF >= 3) print $3; else print $1 }')
%define _obs_commit_count %(echo %{release} | awk -F . '{if (NF >= 2) print $2; else print $1 }')

# We build noarch packages and some sources includes binaries as well
%define _binaries_in_noarch_packages_terminate_build 0

%if "%{_build_flavour}" == "release"
%define _version_appendix (%{_target_cpu})
%else
%define _version_appendix (%{_target_cpu},%{_build_flavour})
%endif

%if 0%{?ha_device_override:1}
%define ha_device %{ha_device_override}
%else
%define ha_device %{device}
%endif

%if 0%{?dhs_flavour:1}
%define dhs_feature droid-src-%{dhs_flavour}
%else
%define dhs_feature droid-src
%endif

%define dhs_name %{dhs_feature}-%{ha_device}

# if dhs_flavour is not defined, means we're building a generic droid-src, and
# for backwards compatibility we'll need to provide droid-bin and others
%if 0%{?dhs_flavour:1}
%define dhs_legacy 0
%else
%define dhs_legacy 1
%endif

# Don't run strip
%define __strip /bin/true

Summary: 	Droid SRC package for %{ha_device}%{?dhs_flavour:, %{dhs_flavour} flavour}
License: 	BSD
Name: 		%{dhs_name_hardcoded}
Version: 	0.0.0.1
# timestamped releases are used only for HADK (mb2) builds
%if 0%{?_obs_build_project:1}
Release:	1
%else
Release:	%(date +'%%Y%%m%%d%%H%%M')
%endif
Provides:	%{dhs_feature}
%if %{dhs_legacy}
Provides:	droid-bin
%endif
# The repo sync service on OBS prepares a 'source tarball' of the rpm
# dir since we currently have a complex setup with subdirs which OBS
# doesn't like. This is not a problem for local builds.
Source0: 	rpm.tar.bzip2
# Ths actual droid source from the repo service when run on OBS.
# local builds don't mind if this is missing
Source40:       repo.tar.bzip2
# Reserve Source50 onwards
# Allow device specific sources to be defined using dhs_sources
%{?dhs_sources}

Group:		System

# droid-src does not build any binaries, just bundles sources
BuildArch:      noarch

%if 0%{?_obs_build_project:1}
%if 0%{?have_vendor_src_for_obs:1}
BuildRequires:  droid-system-vendor-obsbuild
%endif
%endif

# Ignore the rpmlint-* to avoid long RPMLINT reporting
#!BuildIgnore: rpmlint-mini
#!BuildIgnore: rpmlint-MeeGo
# Don't run any of the MeeGo brp-strip-* or other install_post validation commands
%define __os_install_post %{nil}

%description
%{summary}.

%if 0%{?dhs_trees:1}
# repo service performed : %%include package-section
%package dhs-full
Provides: %{dhs_feature}-full
%if %{dhs_legacy}
Provides: droid-bin-src-full
%endif
Group:  System
AutoReqProv: no
Requires(post): /bin/sh
Requires: %{dhs_feature}-dhs-rootdir %{dhs_feature}-build %{dhs_feature}-development %{dhs_feature}-libcore %{dhs_feature}-platform_testing %{dhs_feature}-toolchain %{dhs_feature}-compatibility %{dhs_feature}-device %{dhs_feature}-libnativehelper %{dhs_feature}-prebuilts %{dhs_feature}-tools %{dhs_feature}-art %{dhs_feature}-cts %{dhs_feature}-external %{dhs_feature}-vendor %{dhs_feature}-bionic %{dhs_feature}-dalvik %{dhs_feature}-frameworks %{dhs_feature}-sdk %{dhs_feature}-bootable %{dhs_feature}-hardware %{dhs_feature}-packages %{dhs_feature}-system %{dhs_feature}-developers %{dhs_feature}-kernel %{dhs_feature}-pdk %{dhs_feature}-test
Summary: Syspart source for all the src trees to be used for droid-side code building
%description dhs-full
This is the full src tree for the %{dhs_name} manifest.
It is only meant for use in the OBS.

%package dhs-utils
Provides: %{dhs_feature}-dhs-utils
Group:  System
AutoReqProv: no
Requires(post): /bin/sh
Summary: Utilities for droid-side code building for %{device}%{?device_variant}
%description dhs-utils
Summary: Utilities for using the syspart source for droid-side code building.
This package is hardcoded for %{device}%{?device_variant}
It is only meant for use in the OBS.

%if 0%{!?dhs_no_makefile:1}
%package dhs-makefile
Provides: %{dhs_feature}-dhs-makefile
Group:  System
AutoReqProv: no
Requires(post): /bin/sh
Summary: Top level makefile to be used for droid-side code building
%description dhs-makefile
Top level makefile to be used for droid-side code building
It is only meant for use in the OBS.
%endif

%package dhs-rootdir
Provides: %{dhs_feature}-dhs-rootdir
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Top level source files for the device src tree to be used for droid-side code building
%description dhs-rootdir
This is the src tree for the files in the root directory from the %device manifest.
It is only meant for use in the OBS.

%package build
Provides: %{dhs_feature}-build
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the build src tree to be used for droid-side code building
%description build
This is the src tree for the build subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package development
Provides: %{dhs_feature}-development
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the development src tree to be used for droid-side code building
%description development
This is the src tree for the development subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package libcore
Provides: %{dhs_feature}-libcore
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the libcore src tree to be used for droid-side code building
%description libcore
This is the src tree for the libcore subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package platform_testing
Provides: %{dhs_feature}-platform_testing
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the platform_testing src tree to be used for droid-side code building
%description platform_testing
This is the src tree for the platform_testing subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package toolchain
Provides: %{dhs_feature}-toolchain
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the toolchain src tree to be used for droid-side code building
%description toolchain
This is the src tree for the toolchain subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package compatibility
Provides: %{dhs_feature}-compatibility
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the compatibility src tree to be used for droid-side code building
%description compatibility
This is the src tree for the compatibility subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package device
Provides: %{dhs_feature}-device
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the device src tree to be used for droid-side code building
%description device
This is the src tree for the device subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package libnativehelper
Provides: %{dhs_feature}-libnativehelper
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the libnativehelper src tree to be used for droid-side code building
%description libnativehelper
This is the src tree for the libnativehelper subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package prebuilts
Provides: %{dhs_feature}-prebuilts
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the prebuilts src tree to be used for droid-side code building
%description prebuilts
This is the src tree for the prebuilts subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package tools
Provides: %{dhs_feature}-tools
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the tools src tree to be used for droid-side code building
%description tools
This is the src tree for the tools subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package art
Provides: %{dhs_feature}-art
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the art src tree to be used for droid-side code building
%description art
This is the src tree for the art subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package cts
Provides: %{dhs_feature}-cts
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the cts src tree to be used for droid-side code building
%description cts
This is the src tree for the cts subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package external
Provides: %{dhs_feature}-external
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the external src tree to be used for droid-side code building
%description external
This is the src tree for the external subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package vendor
Provides: %{dhs_feature}-vendor
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the vendor src tree to be used for droid-side code building
%description vendor
This is the src tree for the vendor subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package bionic
Provides: %{dhs_feature}-bionic
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the bionic src tree to be used for droid-side code building
%description bionic
This is the src tree for the bionic subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package dalvik
Provides: %{dhs_feature}-dalvik
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the dalvik src tree to be used for droid-side code building
%description dalvik
This is the src tree for the dalvik subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package frameworks
Provides: %{dhs_feature}-frameworks
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the frameworks src tree to be used for droid-side code building
%description frameworks
This is the src tree for the frameworks subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package sdk
Provides: %{dhs_feature}-sdk
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the sdk src tree to be used for droid-side code building
%description sdk
This is the src tree for the sdk subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package bootable
Provides: %{dhs_feature}-bootable
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the bootable src tree to be used for droid-side code building
%description bootable
This is the src tree for the bootable subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package hardware
Provides: %{dhs_feature}-hardware
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the hardware src tree to be used for droid-side code building
%description hardware
This is the src tree for the hardware subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package packages
Provides: %{dhs_feature}-packages
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the packages src tree to be used for droid-side code building
%description packages
This is the src tree for the packages subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package system
Provides: %{dhs_feature}-system
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the system src tree to be used for droid-side code building
%description system
This is the src tree for the system subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package developers
Provides: %{dhs_feature}-developers
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the developers src tree to be used for droid-side code building
%description developers
This is the src tree for the developers subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package kernel
Provides: %{dhs_feature}-kernel
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the kernel src tree to be used for droid-side code building
%description kernel
This is the src tree for the kernel subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package pdk
Provides: %{dhs_feature}-pdk
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the pdk src tree to be used for droid-side code building
%description pdk
This is the src tree for the pdk subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%package test
Provides: %{dhs_feature}-test
Group:  System
AutoReqProv: no
Requires: %{dhs_feature}-dhs-utils %{dhs_feature}-dhs-makefile
Requires(post): /bin/sh
Summary: Source for the test src tree to be used for droid-side code building
%description test
This is the src tree for the test subdirectory from the %{device} manifest.
It is only meant for use in the OBS.

%endif

%prep
# No %%setup macro !!

%if 0%{?_obs_build_project:1}
# The OBS does not have access to 'repo' so a service does the repo init/sync
# and provides a (huge) tarball with the checked-out tree in it.
# So now drop to android_root and pretend to do a repo sync
tar xf %{SOURCE40} -C %android_root
# Clean up the repo tarball to save space
rm -f %{SOURCE40}
# Make a dummy tarball for rpm checks
mkdir dummy;(cd dummy; touch dummy; tar cvf - . | bzip2 > %{SOURCE40}); rm -rf dummy
# unpack the directories to SOURCES ... this needs to change
tar xf %{SOURCE0} -C ../SOURCES
# Clean up the rpm tarball too
rm -f %{SOURCE0}
cp %{SOURCE40} %{SOURCE0}

%if 0%{?have_vendor_src_for_obs:1}
# Copy SW binaries to the build dir (provided by droid-system-vendor-obsbuild)
cp -ar /vendor .
%endif

# In OBS the repo service leaves the rpm/* files for OBS and they just ^^
# got unpacked to ../SOURCES ... but we're used to having an rpm/ dir
# So if rpm/ is missing then we use ../SOURCES :
[ -d rpm ] || ln -s ../SOURCES rpm
%endif

%build

# We'll hardcode the device/variant information into the droid-make
# script This isn't trivially installable into the ubu-chroot so
# include the ubu-chroot command within it
cat <<"EOF" > droid-make
#!/bin/bash

# This command runs a hardware-specific 'make' command inside the
# ubu-chroot with the correct lunch setup
# It is only intended to run in the OBS builders

# We can check if we have new or old ubu-chroot by checking if it has the -V  option
# added with this version.
if ubu-chroot -V ; then
   bash="bash -c"
fi

exec ubu-chroot -r /srv/mer/sdks/ubu ${bash} "set -o errexit; %{?pre_actions}; source build/envsetup.sh; lunch %{?lunch_device}%{!?lunch_device:%{device}}%{?device_variant}; make $*"
EOF

%{?post_build_actions}

################
%install
rm -rf $RPM_BUILD_ROOT

# Support the building of src-* rpms and srcutils if they're wanted
%if 0%{?dhs_trees:1}
# To create a set of rpms that hold the *source* we move the subset of
# src to the buildroot for packaging
# These will be used to create buildroots for packages like droidmedia
mkdir -p $RPM_BUILD_ROOT/home/abuild/src/droid
for tree in %dhs_trees ; do
   d=$(dirname $tree)
   mkdir -p $RPM_BUILD_ROOT/home/abuild/src/droid/$d
   mv %android_root/$tree $RPM_BUILD_ROOT/home/abuild/src/droid/$d
done

# Top level makefile
if [ -f %android_root/Makefile ]; then
mv %android_root/Makefile $RPM_BUILD_ROOT/home/abuild/src/droid/
fi

# Install the droid-make helper
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp droid-make $RPM_BUILD_ROOT/usr/bin

rm -rf tmp/
mkdir tmp/

find %android_root -maxdepth 1 \( -type f -or -type l \) -print -exec mv {} $RPM_BUILD_ROOT/home/abuild/src/droid/ \; | sed 's ^%android_root /home/abuild/src/droid ' >> tmp/rootdir.files

%endif

################################################################
# Begin files section

#files
#defattr(-,root,root,-)

%if 0%{?dhs_trees:1}
# repo service performed : %%include files-section
%files dhs-full
# Deliberately empty

%files dhs-utils
%defattr(755,root,root,-)
/usr/bin/droid-make

%if 0%{!?dhs_no_makefile:1}
%post dhs-makefile
# The abuild user is not setup at post time so we use the numeric id
chown 399:399 /home/abuild/src
chown 399:399 /home/abuild/src/droid
chown 399:399 /home/abuild/src/droid/Makefile

%files dhs-makefile
%defattr(-,root,root,-)
/home/abuild/src/droid/Makefile
%endif

%post dhs-rootdir
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/

%files dhs-rootdir -f tmp/rootdir.files
%defattr(-,root,root,-)

%post build
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/build
%files build
%defattr(-,root,root,-)
/home/abuild/src/droid/build

%post development
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/development
%files development
%defattr(-,root,root,-)
/home/abuild/src/droid/development

%post libcore
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/libcore
%files libcore
%defattr(-,root,root,-)
/home/abuild/src/droid/libcore

%post platform_testing
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/platform_testing
%files platform_testing
%defattr(-,root,root,-)
/home/abuild/src/droid/platform_testing

%post toolchain
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/toolchain
%files toolchain
%defattr(-,root,root,-)
/home/abuild/src/droid/toolchain

%post compatibility
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/compatibility
%files compatibility
%defattr(-,root,root,-)
/home/abuild/src/droid/compatibility

%post device
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/device
%files device
%defattr(-,root,root,-)
/home/abuild/src/droid/device

%post libnativehelper
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/libnativehelper
%files libnativehelper
%defattr(-,root,root,-)
/home/abuild/src/droid/libnativehelper

%post prebuilts
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/prebuilts
%files prebuilts
%defattr(-,root,root,-)
/home/abuild/src/droid/prebuilts

%post tools
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/tools
%files tools
%defattr(-,root,root,-)
/home/abuild/src/droid/tools

%post art
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/art
%files art
%defattr(-,root,root,-)
/home/abuild/src/droid/art

%post cts
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/cts
%files cts
%defattr(-,root,root,-)
/home/abuild/src/droid/cts

%post external
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/external
%files external
%defattr(-,root,root,-)
/home/abuild/src/droid/external

%post vendor
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/vendor
%files vendor
%defattr(-,root,root,-)
/home/abuild/src/droid/vendor

%post bionic
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/bionic
%files bionic
%defattr(-,root,root,-)
/home/abuild/src/droid/bionic

%post dalvik
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/dalvik
%files dalvik
%defattr(-,root,root,-)
/home/abuild/src/droid/dalvik

%post frameworks
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/frameworks
%files frameworks
%defattr(-,root,root,-)
/home/abuild/src/droid/frameworks

%post sdk
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/sdk
%files sdk
%defattr(-,root,root,-)
/home/abuild/src/droid/sdk

%post bootable
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/bootable
%files bootable
%defattr(-,root,root,-)
/home/abuild/src/droid/bootable

%post hardware
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/hardware
%files hardware
%defattr(-,root,root,-)
/home/abuild/src/droid/hardware

%post packages
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/packages
%files packages
%defattr(-,root,root,-)
/home/abuild/src/droid/packages

%post system
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/system
%files system
%defattr(-,root,root,-)
/home/abuild/src/droid/system

%post developers
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/developers
%files developers
%defattr(-,root,root,-)
/home/abuild/src/droid/developers

%post kernel
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/kernel
%files kernel
%defattr(-,root,root,-)
/home/abuild/src/droid/kernel

%post pdk
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/pdk
%files pdk
%defattr(-,root,root,-)
/home/abuild/src/droid/pdk

%post test
# The abuild user is not setup at post time so we use the numeric id
chown -R 399:399 /home/abuild/src/droid/test
%files test
%defattr(-,root,root,-)
/home/abuild/src/droid/test

%endif
