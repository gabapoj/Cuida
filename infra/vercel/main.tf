terraform {
  required_providers {
    vercel = {
      source  = "vercel/vercel"
      version = "~> 2.0"
    }
  }
}

# Landing page — cuida.io (Next.js)
resource "vercel_project" "landing" {
  name           = "${var.project_name}-landing"
  framework      = "nextjs"
  root_directory = "landing"

  git_repository = {
    type              = "github"
    repo              = var.github_repo
    production_branch = var.production_branch
  }

  team_id = var.vercel_team_id != "" ? var.vercel_team_id : null
}

resource "vercel_project_domain" "landing_root" {
  project_id = vercel_project.landing.id
  domain     = var.domain
  team_id    = var.vercel_team_id != "" ? var.vercel_team_id : null
}

resource "vercel_project_domain" "landing_www" {
  project_id = vercel_project.landing.id
  domain     = "www.${var.domain}"
  team_id    = var.vercel_team_id != "" ? var.vercel_team_id : null
}

# Web app — app.cuida.io (Vite)
resource "vercel_project" "web" {
  name           = "${var.project_name}-web"
  framework      = "vite"
  root_directory = "web"

  git_repository = {
    type              = "github"
    repo              = var.github_repo
    production_branch = var.production_branch
  }

  team_id = var.vercel_team_id != "" ? var.vercel_team_id : null
}

resource "vercel_project_domain" "web_app" {
  project_id = vercel_project.web.id
  domain     = "app.${var.domain}"
  team_id    = var.vercel_team_id != "" ? var.vercel_team_id : null
}
