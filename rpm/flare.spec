#
# spec file for package flare
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           info.you_ra.flare
Version:        1.14
Release:        0
Summary:        Free Libre Action Roleplaying Engine
License:        (CC-BY-SA-3.0 OR CC-BY-SA-4.0) AND GPL-3.0-or-later
Group:          Amusements/Games/RPG
URL:            https://flarerpg.org
Source0:        https://github.com/flareteam/flare-game/releases/download/v%{version}/%{name}-engine-v%{version}.tar.gz
Source1:        https://github.com/flareteam/flare-game/releases/download/v%{version}/%{name}-game-v%{version}.tar.gz
Patch0:         flare-engine-1.14-settings.patch
Patch1:         flare-engine-1.14-desktop.patch
Patch2:         flare-engine-1.14-cmake.patch
Patch3:         flare-engine-1.14-platformlinux.patch
BuildRequires:  cmake
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  vim
BuildRequires:  pkgconfig(SDL2_image)
BuildRequires:  pkgconfig(SDL2_mixer)
BuildRequires:  pkgconfig(SDL2_ttf)
BuildRequires:  librsvg-tools

%define _unpackaged_files_terminate_build 0

%description
Flare (Free Libre Action Roleplaying Engine) is a game engine built
to handle a very specific kind of game: single-player 2D action RPGs.
Flare is not a reimplementation of an existing game or engine. It is a
tribute to and exploration of the action RPG genre.

The usecase of this project is to build several real games and
reuse code. The first game, in progress, is a fantasy dungeon crawl.

Flare uses .ini-style config files for most of the
game data to modify game contents. The game code is C++.

%prep
if [ ! -d flare-engine-v%{version} ]; then
  curl -O -L https://github.com/flareteam/flare-game/releases/download/v%{version}/flare-engine-v%{version}.tar.gz
  tar xzf flare-engine-v%{version}.tar.gz
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
fi
if [ ! -d flare-game-v%{version} ]; then
  curl -O -L https://github.com/flareteam/flare-game/releases/download/v%{version}/flare-game-v%{version}.tar.gz
  tar xzf flare-game-v%{version}.tar.gz
fi

%build
%cmake \
    -DBINDIR="bin" \
    -DDATADIR="share/%{name}" \
    -DMANDIR="share/%{name}/man" \
    -DCMAKE_BUILD_TYPE="Release" \
    -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
    flare-engine-v%{version}
%make_build
if test -f %{name} ; then strip %{name}; fi
for sz in 86 108 128 172; do \
    rsvg-convert \
    --width=${sz} \
    --height=${sz} \
    --output "${sz}x${sz}.png" \
    flare-engine-v%{version}/distribution/flare_logo_icon.svg; \
    done
cd flare-game-v%{version} && /usr/bin/cmake \
    -DDATADIR="share/%{name}" \
    -DCMAKE_BUILD_TYPE="Release" \
    -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
    .
%install
%make_install
mkdir -p "/home/deploy/installroot/usr/share/icons/hicolor/86x86/apps"
install -m 644 -p "86x86.png" "/home/deploy/installroot/usr/share/icons/hicolor/86x86/apps/%{name}.png"
mkdir -p "/home/deploy/installroot/usr/share/icons/hicolor/108x108/apps"
install -m 644 -p "108x108.png" "/home/deploy/installroot/usr/share/icons/hicolor/108x108/apps/%{name}.png"
mkdir -p "/home/deploy/installroot/usr/share/icons/hicolor/128x128/apps"
install -m 644 -p "128x128.png" "/home/deploy/installroot/usr/share/icons/hicolor/128x128/apps/%{name}.png"
mkdir -p "/home/deploy/installroot/usr/share/icons/hicolor/172x172/apps"
install -m 644 -p "172x172.png" "/home/deploy/installroot/usr/share/icons/hicolor/172x172/apps/%{name}.png"
cd flare-game-v%{version} && /usr/bin/make DATADIR="/usr/share/%{name}" DESTDIR=/home/deploy/installroot INSTALL_ROOT=/home/deploy/installroot install

%files
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
