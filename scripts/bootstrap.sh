#!/usr/bin/env bash
set -euo pipefail

# Cuida bootstrap — installs macOS prerequisites
# Usage: bash scripts/bootstrap.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[ok]${NC}   $*"; }
warn() { echo -e "${YELLOW}[warn]${NC} $*"; }
fail() { echo -e "${RED}[fail]${NC} $*"; }

echo ""
echo "Cuida — bootstrapping local dev environment"
echo "--------------------------------------------"
echo ""

# ── Homebrew ──────────────────────────────────────────────────────────────────
if command -v brew &>/dev/null; then
    ok "Homebrew already installed"
else
    warn "Homebrew not found — installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ok "Homebrew installed"
fi

# ── just ──────────────────────────────────────────────────────────────────────
if command -v just &>/dev/null; then
    ok "just $(just --version) already installed"
else
    warn "just not found — installing via Homebrew..."
    brew install just
    ok "just installed"
fi

# ── uv ────────────────────────────────────────────────────────────────────────
if command -v uv &>/dev/null; then
    ok "uv $(uv --version) already installed"
else
    warn "uv not found — installing via Homebrew..."
    brew install uv
    ok "uv installed"
fi

# ── psql (postgresql client) ──────────────────────────────────────────────────
if command -v psql &>/dev/null; then
    ok "psql already installed"
else
    warn "psql not found — installing libpq via Homebrew..."
    brew install libpq
    brew link --force libpq
    ok "psql installed"
fi

# ── Container runtime ─────────────────────────────────────────────────────────
if ! command -v docker &>/dev/null; then
    fail "No container runtime found (docker CLI not in PATH)"
    echo ""
    echo "  Install one of:"
    echo "    OrbStack (recommended):   https://orbstack.dev"
    echo "    Docker Desktop:           https://www.docker.com/products/docker-desktop"
    echo "    Rancher Desktop:          https://rancherdesktop.io"
    echo ""
    echo "  Then re-run this script."
    exit 1
fi

if docker info &>/dev/null; then
    ok "Container runtime is running ($(docker info --format '{{.ServerVersion}}' 2>/dev/null || echo "version unknown"))"
else
    fail "Docker CLI found but no container daemon is running"
    echo ""
    echo "  Start your container runtime (OrbStack, Docker Desktop, etc.) and re-run."
    exit 1
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
ok "All prerequisites satisfied. Run 'just install' to continue setup."
echo ""
