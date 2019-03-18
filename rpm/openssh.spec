#specfile originally created for Fedora, modified for Moblin Linux

# OpenSSH privilege separation requires a user & group ID
%define sshd_uid    74
%define sshd_gid    74

# Do we want to disable building of gnome-askpass? (1=yes 0=no)
%define no_gnome_askpass 1

# Do we want to link against a static libcrypto? (1=yes 0=no)
%define static_libcrypto 0

# Do we want smartcard support (1=yes 0=no)
%define scard 0

# Use GTK2 instead of GNOME in gnome-ssh-askpass
%define gtk2 1

# Build position-independent executables (requires toolchain support)?
%define pie 1

# Do we want libedit support
%define libedit 0

# Do we want kerberos5 support 
%define kerberos5 0

# Do we want NSS tokens support
%define nss 1

# Whether or not /sbin/nologin exists.
%define nologin 1

# Reserve options to override askpass settings with:
# rpm -ba|--rebuild --define 'skip_xxx 1'
%{?skip_gnome_askpass:%define no_gnome_askpass 1}

# Add option to build without GTK2 for older platforms with only GTK+.
# Red Hat Linux <= 7.2 and Red Hat Advanced Server 2.1 are examples.
# rpm -ba|--rebuild --define 'no_gtk2 1'
%{?no_gtk2:%define gtk2 0}

# Options for static OpenSSL link:
# rpm -ba|--rebuild --define "static_openssl 1"
%{?static_openssl:%define static_libcrypto 1}

# Options for Smartcard support: (needs libsectok and openssl-engine)
# rpm -ba|--rebuild --define "smartcard 1"
%{?smartcard:%define scard 1}

# Is this a build for the rescue CD (without PAM, with MD5)? (1=yes 0=no)
%define rescue 0
%{?build_rescue:%define rescue 1}
%{?build_rescue:%define rescue_rel rescue}

# Turn off some stuff for resuce builds
%if %{rescue}
%define libedit 0
%define kerberos5 0
%endif

Summary: The OpenSSH implementation of SSH protocol versions 1 and 2
Name: openssh
Version: 7.9p1
Release: 1%{?rescue_rel}
URL: http://www.openssh.com/portable.html
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
#Source1: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz.asc
Source2: sshd.pam
Source4: sshd.service
Source5: sshd@.service 
Source6: sshd.socket
Source7: sshd-keys.service
Source8: sshd-hostkeys
Source9: ssh_config
Source10: sshd_config
Patch0:  0001-CVE-2018-20685-upstream-disallow-empty-incoming-file.patch
Patch1:  0002-CVE-2019-6109-0-For-broken-read-readv-comparisons-po.patch
Patch2:  0003-CVE-2019-6109-1-upstream-Sanitize-scp-filenames-via-.patch
Patch3:  0004-CVE-2019-6109-2-upstream-Have-progressmeter-force-an.patch
Patch4:  0005-CVE-2019-6111-upstream-check-in-scp-client-that-file.patch

License: BSD
Group: Applications/Internet
%if %{nologin}
Requires: /sbin/nologin
Requires: /bin/systemctl
Requires(preun):  /bin/systemctl
Requires(postun): /bin/systemctl
%endif

%if ! %{no_gnome_askpass}
%if %{gtk2}
BuildRequires: gtk2-devel
BuildRequires: libX11-devel
%else
BuildRequires: gnome-libs-devel
%endif
%endif

%if %{scard}
BuildRequires: sharutils
%endif
BuildRequires: autoconf, automake, openssl-devel, perl, zlib-devel
#BuildRequires: audit-libs-devel
BuildRequires: util-linux, groff
BuildRequires: pam-devel
%if %{kerberos5}
BuildRequires: krb5-devel
%endif

%if %{libedit}
BuildRequires: libedit-devel ncurses-devel
%endif

%if %{nss}
BuildRequires: nss-devel
%endif


%package clients
Summary: The OpenSSH client applications
Requires: openssh = %{version}-%{release}
Group: Applications/Internet

%package server
Summary: The OpenSSH server daemon
Group: System/Daemons
Requires: openssh = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
Requires: pam >= 1.0.1-3
Requires: systemd
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd

%package askpass
Summary: A passphrase dialog for OpenSSH and X
Group: Applications/Internet
Requires: openssh = %{version}-%{release}
Obsoletes: openssh-askpass-gnome
Provides: openssh-askpass-gnome

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}

%package clients-doc
Summary: Documentation for %{name}-clients
Group: Documentation
Requires: %{name}-clients = %{version}

%package server-doc
Summary: Documentation for %{name}-server
Group: Documentation
Requires: %{name}-server = %{version}

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features, as well as removing
all patented algorithms to separate libraries.

This package includes the core files necessary for both the OpenSSH
client and server. To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package includes
the clients necessary to make encrypted connections to SSH servers.
You'll also need to install the openssh package on OpenSSH clients.

%description server
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
the secure shell daemon (sshd). The sshd daemon allows SSH clients to
securely connect to your SSH server. You also need to have the openssh
package installed.

%description askpass
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH.

%description doc
Man pages for %{name}.

%description clients-doc
Man pages for %{name}-clients.

%description server-doc
Man pages for %{name}-server.

%prep
%setup -q -n %{name}-%{version}/upstream

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

autoreconf

%build
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS
%if %{rescue}
CFLAGS="$CFLAGS -Os"
%endif
%if %{pie}
%ifarch s390 s390x sparc sparcv9 sparc64
CFLAGS="$CFLAGS -fPIE"
%else
CFLAGS="$CFLAGS -fpie"
%endif
export CFLAGS
LDFLAGS="$LDFLAGS -pie"; export LDFLAGS
%endif

%if %{kerberos5}
if test -r /etc/profile.d/krb5-devel.sh ; then
        source /etc/profile.d/krb5-devel.sh
fi
krb5_prefix=`krb5-config --prefix`
if test "$krb5_prefix" != "%{_prefix}" ; then
        CPPFLAGS="$CPPFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"; export CPPFLAGS
        CFLAGS="$CFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"
        LDFLAGS="$LDFLAGS -L${krb5_prefix}/%{_lib}"; export LDFLAGS
else
        krb5_prefix=
        CPPFLAGS="-I%{_includedir}/gssapi"; export CPPFLAGS
        CFLAGS="$CFLAGS -I%{_includedir}/gssapi"
fi
%endif

%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--datadir=%{_datadir}/openssh \
	--with-rsh=%{_bindir}/rsh \
	--with-default-path=/usr/local/bin:/bin:/usr/bin \
	--with-superuser-path=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin \
	--with-privsep-path=%{_var}/empty/sshd \
	--enable-vendor-patchlevel="FC-%{version}-%{release}" \
	--disable-strip \
	--without-zlib-version-check \
%if %{nss}
	--with-nss \
%endif
%if %{scard}
	--with-smartcard \
%endif
%if %{rescue}
	--without-pam \
%else
	--with-pam \
%endif
%if %{kerberos5}
        --with-kerberos5${krb5_prefix:+=${krb5_prefix}} \
%else
        --without-kerberos5 \
%endif
%if %{libedit}
	--with-libedit
%else
	--without-libedit
%endif

%if %{static_libcrypto}
perl -pi -e "s|-lcrypto|%{_libdir}/libcrypto.a|g" Makefile
%endif

make

# Define a variable to toggle gnome1/gtk2 building.  This is necessary
# because RPM doesn't handle nested %if statements.
%if %{gtk2}
	gtk2=yes
%else
	gtk2=no
%endif

%if ! %{no_gnome_askpass}
pushd contrib
if [ $gtk2 = yes ] ; then
	make gnome-ssh-askpass2
	mv gnome-ssh-askpass2 gnome-ssh-askpass
else
	make gnome-ssh-askpass1
	mv gnome-ssh-askpass1 gnome-ssh-askpass
fi
popd
%endif

%install
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd

make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/
install contrib/ssh-copy-id.1 $RPM_BUILD_ROOT%{_mandir}/man1/

# Move doc files to correct place
DOCS=$RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/
mkdir -p $DOCS
install -m 0644 -t $DOCS/ CREDITS INSTALL OVERVIEW README* TODO

# systemd integration
install -D -m 0644 %{SOURCE4} %{buildroot}/%{_lib}/systemd/system/sshd.service
install -D -m 0644 %{SOURCE5} %{buildroot}/%{_lib}/systemd/system/sshd@.service
install -D -m 0644 %{SOURCE6} %{buildroot}/%{_lib}/systemd/system/sshd.socket
install -D -m 0644 %{SOURCE7} %{buildroot}/%{_lib}/systemd/system/sshd-keys.service
mkdir -p %{buildroot}/%{_lib}/systemd/system/multi-user.target.wants
ln -s ../sshd.socket %{buildroot}/%{_lib}/systemd/system/multi-user.target.wants/sshd.socket
install -D -m 0755 %{SOURCE8} %{buildroot}/usr/sbin/sshd-hostkeys
mkdir -p %{buildroot}/%{_lib}/systemd/system/multi-user.target.wants
ln -s ../sshd-keys.service %{buildroot}/%{_lib}/systemd/system/multi-user.target.wants/sshd-keys.service

%if ! %{no_gnome_askpass}
install -s contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/gnome-ssh-askpass
%endif

%if ! %{scard}
	rm -f $RPM_BUILD_ROOT%{_datadir}/openssh/Ssh.bin
%endif

%if ! %{no_gnome_askpass}
ln -s gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/ssh-askpass
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
%endif

%if %{no_gnome_askpass}
rm -f $RPM_BUILD_ROOT/etc/profile.d/gnome-ssh-askpass.*
%endif

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

rm -f README.nss.nss-keys
%if ! %{nss}
rm -f README.nss
%endif

# Use local config files
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/ssh/
install -m 600 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/ssh/

%if ! %{kerberos5}
# If we don't have kerberos, disable mentions of GSSAPI in ssh_config and sshd_config
sed -i -e's/^\([ \t]*GSSAPI\)/#\1/' $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ssh_config $RPM_BUILD_ROOT%{_sysconfdir}/ssh/sshd_config
%endif
%clean

%triggerun server -- ssh-server
if [ "$1" != 0 -a -r /var/run/sshd.pid ] ; then
	touch /var/run/sshd.restart
fi

%pre
# We have nasty problem with old openssh package
# Old package tries to stop sshd.service during uninstallation
# and it fails if sshd.service file is not installed. Because that file
# is installed only when developer mode is enabled (server installed), 
# we will fail during upgrade. To overcome that problem, we create 
# fake service file and remove it when upgrade is over

SSHD_SERVICE="/lib/systemd/system/sshd.service"
if [ ! -f $SSHD_SERVICE -a -d /usr/libexec/openssh ]; then
    echo "[Unit]" > $SSHD_SERVICE || :
    echo "Description=PLU temp fake" >> $SSHD_SERVICE || :
    echo "[Service]"  >> $SSHD_SERVICE || :
    echo "Type=oneshot" >> $SSHD_SERVICE || :
    echo "ExecStart=/bin/true" >> $SSHD_SERVICE || :
    systemctl daemon-reload &> /dev/null || :
fi

%post
# In the past we had sshd-keygen masked to disable it, we changed this
# so that it starts if keys are not present on bootup so one always
# would have keys even if something destroys those.
systemctl unmask sshd-keygen.service &> /dev/null || :

%posttrans
# See comment in pre
SSHD_SERVICE="/lib/systemd/system/sshd.service"
if grep -q "PLU temp fake" $SSHD_SERVICE; then
    systemctl stop sshd.service &> /dev/null || :
    rm -f $SSHD_SERVICE
    systemctl daemon-reload &> /dev/null || :
fi

%pre server
%if %{nologin}
/usr/sbin/useradd -c "Privilege-separated SSH" -u %{sshd_uid} \
	-s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :
%else
/usr/sbin/useradd -c "Privilege-separated SSH" -u %{sshd_uid} \
	-s /dev/null -r -d /var/empty/sshd sshd 2> /dev/null || :
%endif

%post server
systemctl daemon-reload &> /dev/null || :

%postun server
systemctl daemon-reload &> /dev/null || :

%preun server
if [ $1 -eq 0 ] ; then
# only stop when erasing, not on upgrade
systemctl stop sshd.service &> /dev/null || :
fi

%files
%defattr(-,root,root)
%license LICENCE
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli

%if ! %{rescue}
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(0755,root,root) %dir %{_libexecdir}/openssh
%attr(4755,root,root) %{_libexecdir}/openssh/ssh-keysign
%endif
%if %{scard}
%attr(0755,root,root) %dir %{_datadir}/openssh
%attr(0644,root,root) %{_datadir}/openssh/Ssh.bin
%endif

%files doc
%defattr(0644,root,root)
%doc %{_docdir}/%{name}-%{version}
%{_mandir}/man5/moduli.5*
%{_mandir}/man1/ssh-keygen.1*
%{_mandir}/man8/ssh-keysign.8*

%files clients
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/ssh
%attr(0755,root,root) %{_bindir}/scp
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%if ! %{rescue}
%attr(2755,root,nobody) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_bindir}/sftp
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-pkcs11-helper
%endif

%files clients-doc
%defattr(0644,root,root)
%{_mandir}/man1/ssh.1*
%{_mandir}/man1/scp.1*
%{_mandir}/man5/ssh_config.5*
%{_mandir}/man1/ssh-agent.1*
%{_mandir}/man1/ssh-add.1*
%{_mandir}/man1/ssh-keyscan.1*
%{_mandir}/man1/sftp.1*
%{_mandir}/man1/ssh-copy-id.1*
%{_mandir}/man8/ssh-pkcs11-helper.8*

%if ! %{rescue}
%files server
%defattr(-,root,root)
%dir %attr(0711,root,root) %{_var}/empty/sshd
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%attr(0644,root,root) %config(noreplace) /etc/pam.d/sshd
/%{_lib}/systemd/system/sshd.service 
/%{_lib}/systemd/system/sshd.socket
/%{_lib}/systemd/system/sshd@.service
/%{_lib}/systemd/system/sshd-keys.service
/%{_lib}/systemd/system/multi-user.target.wants/sshd.socket
/%{_lib}/systemd/system/multi-user.target.wants/sshd-keys.service
/usr/sbin/sshd-hostkeys

%endif

%files server-doc
%defattr(0644,root,root)
%{_mandir}/man5/sshd_config.5*
%{_mandir}/man8/sshd.8*
%{_mandir}/man8/sftp-server.8*

%if ! %{no_gnome_askpass}
%files askpass
%defattr(-,root,root)
%attr(0644,root,root) %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%attr(0755,root,root) %{_libexecdir}/openssh/gnome-ssh-askpass
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-askpass
%endif
