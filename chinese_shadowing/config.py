from pathlib import Path


path_project = Path(__file__).parent.parent
path_data = path_project.joinpath('data')
path_csv = path_data.joinpath('notes').with_suffix('.csv')
path_temporary = path_project.joinpath('temporary')
