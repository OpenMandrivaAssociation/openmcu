%define cvs	20071226
%if %cvs
%define release	%mkrel 0.%cvs.5
%else
%define release	%mkrel 4
%{expand:%%define o_ver %(echo v%{version}| sed "s#\.#_#g")}
%endif

Summary:	H.323 conferencing server    
Name:		openmcu
Version:	2.2.3
Release:	%{release}
License:	MPL
Group:		Communications
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		https://www.h323plus.org/
%if %cvs
Source0:	%{name}-%{cvs}.tar.lzma
%else
Source0:	http://prdownloads.sourceforge.net/openh323/%{name}-%{o_ver}-src-tar.bz2
%endif
Patch0:		openmcu-2.2.1-mak_files.patch
Patch1:		openmcu_v2_2_1-doc_fixes.diff
BuildRequires:	openh323-devel
BuildRequires:	pwlib-devel

%description 
A free H.323 conferencing server. Part of the H323plus project.

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
%if %cvs
%setup -q -n %{name}
%else
%setup -q -n %{name}_%{o_ver}
%endif
%patch0 -p1
%patch1 -p1

%build
export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
export CXXFLAGS="%{optflags} -DLDAP_DEPRECATED"

%make \
    OPTCCFLAGS="%{optflags}" \
    PWLIBDIR=%{_datadir}/pwlib \
    OPENH323DIR=%{_prefix} \
    PREFIX=%{_prefix} \
    PWLIB_BUILD=1 \
    OH323_LIBDIR=%{_libdir} \
    optshared

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}

install -m0755 obj_*/%{name} %{buildroot}%{_bindir}
install -m0644 %{name}.1 -D %{buildroot}%{_mandir}/man1/%{name}.1

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc ReadMe.txt
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man1/*
