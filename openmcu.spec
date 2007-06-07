%define	name	openmcu
%define	version	2.2.1
%define	release	%mkrel 1

%{expand:%%define o_ver %(echo v%{version}| sed "s#\.#_#g")}

Summary:	H.323 conferencing server    
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MPL
Group:		Communications
URL:		http://www.openh323.org/
Source0:	http://prdownloads.sourceforge.net/openh323/%{name}-%{o_ver}-src-tar.bz2
Patch0:		%{name}-1.1.5-mak_files.patch
Patch2:		openmcu_v2_2_1-doc_fixes.diff
# From upstream CVS: fixes build (deque not #include'd)
Patch3:		openmcu-2.2.1-deque.patch
BuildRequires:	openh323-devel pwlib-devel
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
%patch2 -p1
%patch3 -p0

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
