%global debug_package %{nil}

Name:           gitea
Version:        1.11.4
Release:        1%{?dist}
Summary:        Git with a cup of tea, painless self-hosted git service

License:        MIT
URL:            https://gitea.io
Source0:        https://github.com/go-gitea/gitea/releases/download/v%{version}/%{name}-src-%{version}.tar.gz

BuildRequires:  golang
BuildRequires:  npm

BuildRequires:  pam-devel

Requires:       git

Requires(pre):  shadow-utils


%description
Git with a cup of tea, painless self-hosted git service.


%prep
%autosetup -c

# Change default user in sample config
sed -i "s|RUN_USER = git|RUN_USER = gitea|" custom/conf/app.ini.sample


%build
TAGS="bindata pam sqlite sqlite_unlock_notify" %make_build


%install
install -m 0755 -Dp %{name}                     %{buildroot}%{_bindir}/%{name}
install -m 0755 -dp                             %{buildroot}%{_sharedstatedir}/%{name}

install -m 0644 -Dp /dev/zero                   %{buildroot}%{_sysconfdir}/%{name}/app.ini
install -m 0644 -Dp custom/conf/app.ini.sample  %{buildroot}%{_sysconfdir}/%{name}/app.ini.sample


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name} service account" %{name}
exit 0



%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%config(noreplace) %attr(664, root, %{name}) %{_sysconfdir}/gitea/app.ini
%config %attr(664, root, %{name}) %{_sysconfdir}/gitea/app.ini.sample
%dir %attr(755, %{name}, %{name}) %{_sharedstatedir}/%{name}



%changelog
* Mon May  4 2020 ElXreno <elxreno@gmail.com>
- Initial packaging
