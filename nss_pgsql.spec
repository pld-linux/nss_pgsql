# $Revision: 1.2 $Date: 2002-11-05 13:56:32 $
Summary:	PostgreSQL Name Service Switch Module
Summary(pl):	Modu³ NSS PostgreSQL
Name:		nss_pgsql
Version:	1.0.0
Release:	1
License:	GPL
Group:		Base
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/sysauth-pgsql/libnss-pgsql-%{version}.tar.gz
URL:		http://sysauth-pgsql.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
# should be bcond'ed
BuildRequires:	openssl-devel
BuildRequires:	postgresql-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/lib

%description
NSS PgSQL is a NSS library for PostgreSQL.

%description -l pl
NSS PgSQL jest bibliotek± NSS dla PostgreSQL.

%prep
%setup -q -n libnss-pgsql-%{version}
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
%doc AUTHORS ChangeLog NEWS README doc/nss-pgsql.txt
%attr(755,root,root) %{_libdir}/*.so*
#%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/nss*.conf
