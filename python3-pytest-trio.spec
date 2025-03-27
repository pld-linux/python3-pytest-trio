#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Pytest plugin for trio
Summary(pl.UTF-8):	Wtyczka pytesta do trio
Name:		python3-pytest-trio
Version:	0.8.0
Release:	1
License:	MIT or Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-trio/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest-trio/pytest-trio-%{version}.tar.gz
# Source0-md5:	2bf10f1c4028c783e2bc0341c911646b
URL:		https://pypi.org/project/pytest-trio/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-async_generator >= 1.9
BuildRequires:	python3-hypothesis >= 3.64
BuildRequires:	python3-outcome
BuildRequires:	python3-pytest >= 6.0.0
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-trio >= 0.15.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a pytest plugin to help you test projects that use Trio, a
friendly library for concurrency and async I/O in Python.

%description -l pl.UTF-8
Ten pakiet zawiera wtyczkę pytesta, pomagającą testować projekty
wykorzystujące Trio - przyjazną bibliotekę Pythona do współbieżności i
asynchronicznego we/wy.

%package apidocs
Summary:	API documentation for Python pytest-trio module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pytest-trio
Group:		Documentation

%description apidocs
API documentation for Python pytest-trio module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pytest-trio.

%prep
%setup -q -n pytest-trio-%{version}

# relies on trio tests sources installed
%{__rm} pytest_trio/_tests/test_hypothesis_interaction.py

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_trio.plugin" \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest pytest_trio/_tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/pytest_trio/_tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.MIT README.rst
%{py3_sitescriptdir}/pytest_trio
%{py3_sitescriptdir}/pytest_trio-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
