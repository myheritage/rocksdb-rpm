#%{?scl:%scl_package rocksdb}
%{!?scl:%global pkg_name %{name}}
# Disable dependency auto detecting


Name: rocksdb		
Version: 4.8	
Release:	%{?release}%{!?release:1}%{?dist}
Summary: RocksDB	

Group: Application/Databases		
License: BSD
URL: http://rocksdb.org/	
%if 0%{?gh_commit:1}
Source0: https://github.com/facebook/rocksdb/archive/%{gh_commit}.tar.gz#/%{name}-%{version}.tar.gz	
%else
Source0: https://github.com/facebook/rocksdb/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

BuildRequires: %{?scl_prefix}gcc >= 4.8.2, %{?scl_prefix}binutils, %{?scl_prefix}gcc-c++ >= 4.8.2, zlib-devel, bzip2-devel, snappy-devel, lz4-devel 	
Requires: zlib, bzip2, snappy, lz4

%description

%package devel
Group: Development/Libraries
Summary: Files needed for building projects with RocksDB 
Requires: %{name}, zlib-devel, bzip2-devel, snappy-devel, lz4-devel

%description devel

%prep
%if 0%{?gh_commit:1}
%setup -n %{pkg_name}-%{gh_commit} -q
%else
%setup -n %{pkg_name}-%{version} -q
%endif

%build
%{?scl:scl enable %{scl} - << \EOF}
PORTABLE=1 make %{?_smp_mflags} shared_lib
%{?scl:EOF}

%install
INSTALL_PATH=%{buildroot}/%{_usr} make install-shared
# RocksDB hard coded "lib" as the lib directory, without taking account 64 bit systems, or other systems
# where the lib directory might be different.
if [[ "%{_lib}" != "lib" ]]; then
	mv %{buildroot}/%{_usr}/lib %{buildroot}/%{_usr}/%{_lib}
fi

%files
%doc
%{_usr}/%{_lib}/librocksdb.so* 

%files devel
%{_usr}/include/rocksdb

%changelog
