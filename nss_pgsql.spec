# $Revision: 1.5 $Date: 2003-04-08 13:28:38 $
Summary:	PostgreSQL Name Service Switch Module
Summary(pl):	Modu³ NSS PostgreSQL
Name:		nss_pgsql
Version:	1.0.0
Release:	1
License:	GPL
Group:		Base
Source0:	http://dl.sourceforge.net/sysauth-pgsql/libnss-pgsql-%{version}.tar.gz
URL:		http://sysauth-pgsql.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
# should be bcond'ed
BuildRequires:	openssl-devel >= 0.9.7
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
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install conf/nss-pgsql.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS conf/dbschema.sql doc/nss-pgsql.txt
%attr(755,root,root) %{_libdir}/*.so.*.*
%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/nss-pgsql.conf
