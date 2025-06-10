import click
from github_api import get_repos, delete_repo, star_repo, create_repo, init_repo, clone_repo

@click.group()
def cli():
    """GitHub CLI Tool — manage your repositories with ease"""
    pass

@cli.command()
def list():
    """List all repositories"""
    repos = get_repos()
    for repo in repos:
        click.echo(f"📁 {repo['name']} - 🌐 {repo['html_url']}")

@cli.command()
@click.argument('repo')
def delete(repo):
    """Delete a repository"""
    if click.confirm(f"⚠️ Are you sure you want to delete '{repo}'?"):
        if delete_repo(repo):
            click.echo(f"✅ Deleted '{repo}'")
        else:
            click.echo(f"❌ Failed to delete '{repo}' — check if it exists or if you own it.")

@cli.command()
@click.argument('repo')
def star(repo):
    """Star a repository"""
    if star_repo(repo):
        click.echo(f"⭐ Starred '{repo}'")
    else:
        click.echo(f"❌ Failed to star '{repo}' — check if it exists or if you own it.")

@cli.command()
@click.argument('repo')
def create(repo):
    """Create a new repository"""
    if create_repo(repo):
        click.echo(f"✅ Created repository: {repo}")
    else:
        click.echo(f"❌ Failed to create repository: {repo}")

@cli.command()
@click.argument('repo')
def init(repo):
    """Initialize a local repository"""
    if init_repo(repo):
        click.echo(f"✅ Initialized repository: {repo}")
    else:
        click.echo(f"❌ Failed to initialize repository: {repo}")

@cli.command()
@click.argument("repo")
def clone(repo):
    """Clone a repository"""
    if clone_repo(repo):
        click.echo(f"✅ Cloned repository: {repo}")
    else:
        click.echo(f"❌ Failed to clone repository: {repo}")

if __name__ == '__main__':
    cli()
