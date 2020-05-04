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


%description
Git with a cup of tea, painless self-hosted git service.


%prep
%autosetup -c


%build
TAGS="bindata pam sqlite sqlite_unlock_notify" GITEA_VERSION="%{version}" %make_build


%install
install -m 0755 -Dp %{name} %{buildroot}%{_bindir}/gitea



%files
%license LICENSE
%doc README.md
%{_bindir}/gitea



%changelog
* Mon May  4 2020 ElXreno <elxreno@gmail.com>
- Initial packaging
