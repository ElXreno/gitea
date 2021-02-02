%global debug_package %{nil}

%global gitea_user gitea

Name:           gitea
Version:        1.13.2
Release:        1%{?dist}
Summary:        Git with a cup of tea, painless self-hosted git service

License:        MIT
URL:            https://gitea.io
Source0:        https://github.com/go-gitea/gitea/releases/download/v%{version}/%{name}-src-%{version}.tar.gz

Source10:       %{name}.service
Source11:       %{name}-sysusers.conf

BuildRequires:  systemd
BuildRequires:  golang
BuildRequires:  npm

BuildRequires:  pam-devel

Requires(pre):  shadow-utils
Requires:       git

Recommends:     git-lfs


%description
Git with a cup of tea, painless self-hosted git service.


%prep
%autosetup -c

# Change default user in sample config
sed -i "s|RUN_USER = git|RUN_USER = %{gitea_user}|" custom/conf/app.example.ini


%build
TAGS="bindata pam sqlite sqlite_unlock_notify" \
LDFLAGS="-X \"code.gitea.io/gitea/modules/setting.CustomPath=%{_sharedstatedir}/%{name}\" \
         -X \"code.gitea.io/gitea/modules/setting.CustomConf=%{_sysconfdir}/%{name}/app.ini\" \
         -X \"code.gitea.io/gitea/modules/setting.AppWorkPath=%{_sharedstatedir}/%{name}\"" \
%make_build


%install
install -m 0755 -Dp %{name}                     %{buildroot}%{_bindir}/%{name}
install -m 0755 -dp                             %{buildroot}%{_sharedstatedir}/%{name}

install -m 0644 -Dp custom/conf/app.example.ini %{buildroot}%{_sysconfdir}/%{name}/app.example.ini
touch                                           %{buildroot}%{_sysconfdir}/%{name}/app.ini

install -m 0644 -Dp %{SOURCE10}                 %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 -Dp %{SOURCE11}                 %{buildroot}%{_sysusersdir}/%{name}.conf


%pre
%sysusers_create_package %{name} %{SOURCE11}


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service



%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf
%config %attr(664, root, %{gitea_user}) %{_sysconfdir}/%{name}/app.example.ini
%config(noreplace) %attr(664, root, %{gitea_user}) %{_sysconfdir}/%{name}/app.ini
%dir %attr(755, %{gitea_user}, %{gitea_user}) %{_sharedstatedir}/%{name}



%changelog
* Tue Feb 02 2021 ElXreno <elxreno@gmail.com> - 1.13.2-1
- Update to version 1.13.2

* Thu Jan 14 13:26:51 MSK 2021 George Nikandrov <george.nikandrov@feuerplatz.ru> - 1.13.1-2
- Changed builtin paths

* Wed Dec 30 06:56:50 +03 2020 ElXreno <elxreno@gmail.com> - 1.13.1-1
- Update to version 1.13.1

* Wed Dec  2 10:34:09 +03 2020 ElXreno <elxreno@gmail.com> - 1.13.0-2
- Fix example config installation

* Wed Dec  2 10:19:02 +03 2020 ElXreno <elxreno@gmail.com> - 1.13.0-1
- Update to version 1.13.0

* Mon Nov 16 21:58:00 +03 2020 ElXreno <elxreno@gmail.com> - 1.12.6-1
- Update to version 1.12.6

* Sat Oct 03 2020 ElXreno <elxreno@gmail.com> - 1.12.5-1
- Updated to version 1.12.5

* Sun Sep 06 2020 ElXreno <elxreno@gmail.com> - 1.12.4-1
- Updated to version 1.12.4

* Wed Jul 29 2020 ElXreno <elxreno@gmail.com> - 1.12.3-1
- Updated to version 1.12.3

* Sun Jul 12 2020 ElXreno <elxreno@gmail.com> - 1.12.2-1
- Updated to version 1.12.2

* Mon Jun 22 2020 ElXreno <elxreno@gmail.com> - 1.12.1-1
- Updated to version 1.12.1

* Fri Jun 19 2020 ElXreno <elxreno@gmail.com> - 1.12.0-1
- Updated to version 1.12.0.
  Built with repacked original archive with fixed vendor.

* Sun May 31 2020 ElXreno <elxreno@gmail.com> - 1.11.6-1
- Updated to version 1.11.6

* Sun May 10 2020 ElXreno <elxreno@gmail.com> - 1.11.5-1
- Updated to version 1.11.5

* Mon May 04 2020 ElXreno <elxreno@gmail.com>
- Initial packaging
