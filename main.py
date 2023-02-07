import os

import jira.resources
from jira import JIRA

import datetime


def keep_version(version: jira.resources.Version, start: datetime.datetime, end: datetime.datetime) -> bool:
    if not version.released:
        return True
    release_date = datetime.datetime.strptime(version.releaseDate, '%Y-%m-%d')
    return start <= release_date <= end


def get_version_url(version: jira.resources.Version, jira_server: str, project_key: str) -> str:
    return f'{jira_server}/projects/{project_key}/versions/{version.id}'


def main():
    jira_server = os.environ.get("JIRA_SERVER")
    jira_mail = os.environ.get("JIRA_MAIL")
    jira_token = os.environ.get("JIRA_TOKEN")
    jira_project_key = os.environ.get("JIRA_PROJECT_KEY")
    jira_board_id = int(os.environ.get("JIRA_BOARD_ID"))

    jira_api = JIRA(jira_server, basic_auth=(jira_mail, jira_token))

    sprint = jira_api.sprints(board_id=jira_board_id, state='active')[0]
    sprint_start = datetime.datetime.combine(datetime.datetime.strptime(sprint.startDate, '%Y-%m-%dT%H:%M:%S.%fZ'), datetime.time.min)
    sprint_end = datetime.datetime.combine(datetime.datetime.strptime(sprint.endDate, '%Y-%m-%dT%H:%M:%S.%fZ'), datetime.time.max)

    versions = jira_api.project_versions(jira_project_key)
    versions_to_keep = list(sorted(filter(lambda x: keep_version(x, sprint_start, sprint_end), versions), key=lambda x: x.releaseDate))

    print(f'|Date de MEP|Changement|Déployé|Description|')
    print(f'|:---------:|:--------:|:-----:|:----------|')
    for v in versions_to_keep:
        print(f'| {v.releaseDate} | {get_version_url(v, jira_server, jira_project_key)} | {v.released} | {v.description if "description" in v.raw else ""} |')


if __name__ == '__main__':
    main()
