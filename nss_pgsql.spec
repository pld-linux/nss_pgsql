# $Revision: 1.1 $Date: 2002-11-04 16:50:15 $
Summary:	Postgresql Name Service Switch Module
Name:		nss_pgsql
Version:	1.0.0
Release:	1
License:	GPL
Group:		Base
Source0:	libnss-pgsql-%{version}.tar.gz
URL:		http://www.freesoftware.fsf.org/nss-mysql/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	zlib-devel
BuildRequires:	postgresql-devel
# should be bcond'ed
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/lib

%description
NSS PgSQL is a NSS library for Postgresql.

%description -l pl
NSS PgSQL jest bibliotek± NSS dla Postgresql.

%prep
%setup -q -n libnss-pgsql-%{version}
#%patch0 -p1
#%patch1 -p1
perl -pi -e 's/\#include\ \<postgresql\/libpq-fe.h\>/\#include\ \<libpq-fe.h>/' src/backend.c

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{?debug:--enable-debug} \
	--with-ssl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_libdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
#%doc AUTHORS ChangeLog NEWS README SHADOW THANKS TODO UPGRADE *.sql
%attr(755,root,root) %{_libdir}/*.so*
#%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/nss*.conf
