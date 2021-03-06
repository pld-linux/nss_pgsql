#
# Conditional build:
%bcond_without	openssl		# without SSL support
#
Summary:	PostgreSQL Name Service Switch Module
Summary(pl.UTF-8):	Moduł NSS PostgreSQL
Name:		nss_pgsql
Version:	1.4.0
Release:	1
Epoch:		1
License:	GPL
Group:		Base
Source0:	http://dl.sourceforge.net/sysauth-pgsql/libnss-pgsql-%{version}.tgz
# Source0-md5:	a0507f407a9efb564562969af1130d25
URL:		http://sysauth.projects.postgresql.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	postgresql-devel
BuildRequires:	xmlto
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/%{_lib}

%description
NSS PgSQL is a NSS library for PostgreSQL.

%description -l pl.UTF-8
NSS PgSQL jest biblioteką NSS dla PostgreSQL.

%prep
%setup -q -n libnss-pgsql-%{version}

sed -e 's@#include <postgresql/libpq-fe.h>@#include <libpq-fe.h>@' \
	src/backend.c > backend.c.tmp
mv -f backend.c.tmp src/backend.c

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	%{?debug:--enable-debug} \
	%{?with_openssl:--with-ssl}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install conf/nss-pgsql.conf $RPM_BUILD_ROOT%{_sysconfdir}
install conf/nss-pgsql-root.conf $RPM_BUILD_ROOT%{_sysconfdir}

# useless for module
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{la,so}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS conf/dbschema.sql doc/*.html doc/*.png
%attr(755,root,root) %{_libdir}/*.so.*.*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nss-pgsql.conf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nss-pgsql-root.conf
