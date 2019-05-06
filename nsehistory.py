import click
from nsepy import get_history
from datetime import datetime
@click.command()
@click.option('--symbol', '-S',  help='Index code')
@click.option('--start', '-s', help='Start date in yyyy-mm-dd format')
@click.option('--end', '-e', help='End date in yyyy-mm-dd format')
@click.option('--format', '-f', default='csv',  type=click.Choice(['csv', 'pkl']),
                help='Output format, pkl - to save as Pickel and csv - to save as csv')
@click.option('--file', '-o', 'file_name',  help='Output file name')
def pehistory(symbol, start, end, format, file_name):
    try:
        sd = datetime.strptime(start, "%Y-%m-%d").date()
        ed = datetime.strptime(end, "%Y-%m-%d").date()
    except:
        click.secho("\nPlease provide start and end date in format yyyy-mm-dd\n", fg='red')
        print_help_msg(pehistory)
        return
    if not symbol:
        click.secho("\nPlease provide security/index code\n", fg='red')
        print_help_msg(pehistory)
        return
    df = get_history(symbol, sd, ed)
    click.echo(df.head())
    
    if not file_name:
        file_name = symbol + '.' + format

    if format == 'csv':
        df.to_csv(file_name)
    else:
        df.to_pickle(file_name)
    click.secho('Saved to: {}'.format(file_name) , fg='green', nl=True)

if __name__ == '__main__':
    pehistory()
