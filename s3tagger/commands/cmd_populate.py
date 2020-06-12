import click
from s3tagger.cli import pass_context, Context
from s3tagger.utilities import queueing, loader


@click.command()
@click.option('--not-match', '-n', type=str, multiple=True, help="Keys must NOT include one of these match strings to be processed.")
@click.option('--match', '-m', type=str, multiple=True, help="Keys must include one of these match strings to be processed.")
@click.option('--bucket', '-b', default="", type=str, help="S3 bucket.")
@pass_context
def cli(ctx: Context, bucket: str, match: tuple, not_match) -> None:
    """Loads S3 files into disck-backed queue."""
    if queueing.check_queue(bucket):
        raise click.UsageError(f"Queue for {bucket} already exists!  Please run 's3transfer clean'.")

    q = queueing.create_queue(bucket, new=True)
    loader.get_files(bucket, q, match, not_match)

    click.echo(f"🏋️ Queue for {bucket} is loaded and ready to process! 🏋️")
