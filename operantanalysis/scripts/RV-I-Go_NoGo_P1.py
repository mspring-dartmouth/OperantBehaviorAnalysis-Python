from operantanalysis import loop_over_days, extract_info_from_file, reward_retrieval
import pandas as pd


column_list = ['Subject', 'Day', 'Small Go Trials', 'Large Go Trials', 'Successful Small Go Trials',
               'Successful Large Go Trials']


def RVI_Go_NoGo_P1(loaded_file, i):
    """
    :param loaded_file: file output from operant box
    :param i: number of days analyzing
    :return: data frame of all analysis extracted from file (one animal)
    """
    (timecode, eventcode) = extract_info_from_file(loaded_file, 500)
    (small_go_trials, large_go_trials, small_go_success, large_go_success) = (eventcode.count('GoTrialBegSmallReward'),
                                          eventcode.count('GoTrialBegLargeReward'),
                                          eventcode.count('GoTrialSuccessSmallReward'),
                                          eventcode.count('GoTrialSuccessLargeReward'))

    df2 = pd.DataFrame([[loaded_file['Subject'], int(i + 1), float(small_go_trials), float(large_go_trials),
                         float(small_go_success), float(large_go_success)]],
                       columns=column_list)

    return df2


(days, df) = loop_over_days(column_list, RVI_Go_NoGo_P1)
print(df.to_string())
df.to_excel("output.xlsx")

group_means = df.groupby(['Day'])['GoTrialSuccessSmallReward', 'GoTrialSuccessLargeReward'].mean()
group_sems = df.groupby(['Day'])['GoTrialSuccessSmallReward', 'GoTrialSuccessLargeReward'].sem()

print(df.groupby(['Day'])['GoTrialSuccessSmallReward', 'GoTrialSuccessLargeReward'].mean().unstack().to_string())
print(df.groupby(['Day'])['GoTrialSuccessSmallReward', 'GoTrialSuccessLargeReward'].sem().unstack().to_string())