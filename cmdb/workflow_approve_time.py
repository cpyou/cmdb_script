import pandas as pd
from dateutil.parser import parse


class WorkflowApproveTime(object):

    def __init__(self):
        self.df = pd.read_excel('/Users/chenpuyu/Desktop/domain.xlsx')

    def run(self):
        start_index = int(self.df['id'].count() * 0.1) + 1
        new_df = self.df.loc[start_index:, :]
        print(f'count:{new_df["创建时间"].count()}')
        for i in new_df.index:
            new_df.loc[i].get('创建时间')
            if pd.to_datetime(parse(new_df.loc[i]['创建时间'])).hour >= 21:
                print(i, new_df.loc[i]['创建时间'])
                new_df = new_df.drop(i)
                continue
            if pd.to_datetime(parse(new_df.loc[i]['创建时间'])).dayofweek == 6:
                print(i, new_df.loc[i]['创建时间'])
                new_df = new_df.drop(i)
        print(f'count:{new_df["创建时间"].count()}')
        new_df['运维开始处理时长'] = pd.to_datetime(new_df['运维开始操作时间']) - pd.to_datetime(new_df['创建时间'])
        x = pd.to_timedelta(new_df['运维开始处理时长'].sum() / new_df['运维开始处理时长'].count())
        print(x)


if __name__ == '__main__':
    workflow_approve_time = WorkflowApproveTime()
    workflow_approve_time.run()
