import os
import sys
import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from slackclient import SlackClient

import config


def extract_command_line_input():
    cl_game_id = sys.argv[1]
    cl_start_time = sys.argv[2]

    return cl_game_id, cl_start_time


def calculate_game_times_in_correct_formats(cl_start_time):
    game_start_time = datetime.strptime(cl_start_time, '%Y-%m-%d %H:%M')
    expected_end_time = game_start_time + timedelta(hours=3)

    return game_start_time, expected_end_time


def game_ongoing(game_start_time, expected_end_time):
    time_now = datetime.now()

    if time_now < game_start_time:
        return False
    elif time_now > expected_end_time:
        return False
    else:
        return True


def check_current_result(game_id):
    source = requests.get(
        'http://statistik.innebandy.se/ft.aspx?scr=result&fmid={}'.format(
            game_id
        )).text
    soup = BeautifulSoup(source, 'lxml')

    home_team = soup.find('table',
                          class_='clTblMatchStanding'
                          ).find_all('th')[0].a.text

    away_team = soup.find('table',
                          class_='clTblMatchStanding'
                          ).find_all('th')[2].a.text

    current_result = soup.find('table',
                               class_='clTblMatchStanding'
                               ).find_all('th')[1].text

    game_status = soup.find('table',
                            class_='clCommonGrid'
                            ).find_all('tr')[0].th.text

    current_game_status = soup.find('table',
                                    class_='clCommonGrid'
                                    ).find_all('tr')[0].span.text

    complete_game_status = game_status + ': ' + current_game_status

    period_figures = soup.find('table',
                               class_='clCommonGrid'
                               ).find_all('tr')[1].th.text

    period_figures_text = soup.find('table',
                                    class_='clCommonGrid'
                                    ).find_all('tr')[1].span.text

    period_figures_complete = period_figures + ': ' + period_figures_text

    shots = soup.find('table',
                      class_='clCommonGrid'
                      ).find_all('tr')[2].th.text

    shots_text = soup.find('table',
                           class_='clCommonGrid'
                           ).find_all('tr')[2].span.text

    shots_complete = shots + ': ' + shots_text

    gamelink = 'http://statistik.innebandy.se/ft.aspx?scr=result&fmid={}'.format(game_id)

    return home_team, \
           current_result, \
           away_team, \
           complete_game_status, \
           period_figures_complete, \
           shots_complete, \
           gamelink


def send_push_update(slack_token):
    sc = SlackClient(slack_token)

    message = '{} {} {} \n{} \n{} \n{} \n{}'.format(home_team,
                                                    current_result,
                                                    away_team,
                                                    complete_game_status,
                                                    period_figures_complete,
                                                    shots_complete,
                                                    gamelink
                                                    )
    sc.api_call('chat.postMessage',
                channel='#general',
                text=str(message),
                username='Script Robot',
                icon_emoji=':robot_face:'
                )


if __name__ == "__main__":
    cl_game_id, cl_start_time = extract_command_line_input()
    game_start_time, expected_end_time = calculate_game_times_in_correct_formats(cl_start_time)

    last_result = None

    while game_ongoing(game_start_time, expected_end_time):
        home_team, current_result, away_team, complete_game_status, period_figures_complete, shots_complete, gamelink = check_current_result(cl_game_id)
        if last_result != current_result:
            send_push_update(config.slack_token,
                             home_team,
                             current_result,
                             away_team,
                             complete_game_status,
                             period_figures_complete,
                             shots_complete,
                             gamelink
                             )
            last_result = current_result
            time.sleep(29)
