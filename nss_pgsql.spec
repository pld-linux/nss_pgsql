Summary:	PostgreSQL Name Service Switch Module
Summary(pl):	Modu³ NSS PostgreSQL
Name:		nss_pgsql
Version:	1.0.0
Release:	1
License:	GPL
Group:		Base
Source0:	http://dl.sourceforge.net/sysauth-pgsql/libnss-pgsql-%{version}.tar.gz
# Source0-md5:	73b29c27ad0784baea985f0cf77eec48
URL:		http://sysauth-pgsql.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
# should be bcond'ed
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	postgresql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/lib

%description
NSS PgSQL is a NSS library for PostgreSQL.

%description -l pl
NSS PgSQL jest bibliotek± NSS dla PostgreSQL.

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
	%{?debug:--enable-debug} \
	--with-ssl

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install conf/nss-pgsql.conf $RPM_BUILD_ROOT%{_sysconfdir}

# useless for module
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{la,so}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS conf/dbschema.sql doc/nss-pgsql.txt
%attr(755,root,root) %{_libdir}/*.so.*.*
%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/nss-pgsql.conf
