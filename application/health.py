import click

@click.command()
@click.option('--name', default="Dr. Anonymous", help='Your first name')
def health(name):
    """
    Simple command that says hello
    """
    click.echo(f'Hello {name}')


if __name__ == '__main__':
    health()