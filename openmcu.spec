%define	name	openmcu
%define	version	2.1.0
%define	release	5mdk

%{expand:%%define o_ver %(echo v%{version}| sed "s#\.#_#g")}
%define openh323_version 1.15.3
%define pwlib_version 1.8.4

Summary:	H.323 conferencing server    
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MPL
Group:		Communications
URL:		http://www.openh323.org/
Source0:	http://prdownloads.sourceforge.net/openh323/%{name}-%{o_ver}-src-tar.bz2
Patch0:		%{name}-1.1.5-mak_files.patch.bz2
Patch1:		openmcu_v2_1_0-amd64_gcc4.diff.bz2
Patch2:		openmcu_v2_1_0-doc_fixes.diff.bz2
BuildRequires:	openh323-devel >= %openh323_version pwlib-devel >= %pwlib_version
Conflicts:	vpb-devel
Requires:	pwlib1 >= %{pwlib_version} openh323_1 >= %{openh323_version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
A free H.323 conferencing server. Part of OpenH323 project.

Features:
---------
- requires no codec hardware to operate
- currently supports G.711 and GSM audio codecs and H.261 video codecs
- can accept multiple connections simultaneously
- several different conferences can be talking place at the same time
  using the 'rooms' feature
- display statistics on calls in progress
- initiate calls from the MCU to remote endpoints

%prep

%setup -q -n %{name}_%{o_ver}
%patch0 -p1
%patch1 -p0
%patch2 -p0

%build

export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
export CXXFLAGS="%{optflags} -DLDAP_DEPRECATED"

%make \
    OPTCCFLAGS="%{optflags}" \
    PWLIBDIR=%{_datadir}/pwlib \
    OPENH323DIR=%{_prefix} \
    PREFIX=%{_prefix} \
    PWLIB_BUILD=1 \
    optshared

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}

install -m0755 obj_*/%{name} %{buildroot}%{_bindir}
install -m0644 %{name}.1 -D %{buildroot}%{_mandir}/man1/%{name}.1

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc ReadMe.txt
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man1/*
