#
# Copyright 2018 Analytics Zoo Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pandas as pd
import numpy as np


class TSDataset:
    def __init__(self):
        '''
        TSDataset is an abstract of time series dataset.
        '''
        self.df = None  # internal dataframe
        self.id_col = None  # column name of id
        self.dt_col = None  # column name of time
        self.feature_col = None  # column name of feature
        self.target_col = None  # column name of target
        raise NotImplementedError("TSDataset is developing for now.")

    @staticmethod
    def from_pandas(df,
                    datetime_col,
                    target_col,
                    id_col=None,
                    extra_feature_col=None):
        '''
        Initialize a tsdataset from pandas dataframe.
        :param df: a pandas dataframe for your raw time series data.
        :param datetime_col: a str indicates the col name of datetime
               column in the input data frame.
        :param target_col: a str or list indicates the col name of target column
               in the input data frame.
        :param id_col: a str indicates the col name of dataframe id.
        :param extra_feature_col: (optional) a str or list indicates the col name
               of extra feature columns that needs to predict the target column.
        Here is an df example:
        id        datetime      value   "extra feature 1"   "extra feature 2"
        00        2019-01-01    1.9     1                   2
        01        2019-01-01    2.3     0                   9
        00        2019-01-02    2.4     3                   4
        01        2019-01-02    2.6     0                   2
        ```python
        tsdataset = TSDataset.from_pandas(df, datetime_col="datetime",
                                          target_col="value", id_col="id",
                                          extra_feature_col=["extra feature 1",""extra feature 2"])
        ```
        '''
        # check input
        # map input to required internal dataframe structure
        raise NotImplementedError("TSDataset is developing for now.")

    def impute(self, mode="last"):
        '''
        Impute the tsdataset
        :param mode: a str defaulted to "last" indicates imputing method.
               "last", "const" and "linear" are supported for now.
        '''
        # split the internal dataframe(self.df) to sub-df wrt id_col
        # call impute function in zouwu.transform.impute on each sub-df.
        # concat the result back to self.df
        return self

    def deduplicate(self):
        '''
        Remove those duplicated rows.
        '''
        # split the internal dataframe(self.df) to sub-df wrt id_col
        # call deduplicate function in zouwu.transform.deduplicate on each sub-df.
        # concat the result back to self.df
        return self

    def resample(self, interval, mode="mean", allow_na=False):
        '''
        Resampling the data with a new time interval.
        :param interval: resampling time interval.
        :param mode: if current interval is smaller than output interval,
               we need to merge the valuesin a mode. "max", "min", "mean"
               or "sum" are supported for now.
        :param allow_na: bool, default to False. If True, we will remove those
               timestamp with all other column is N/A.
        '''
        # split the internal dataframe(self.df) to sub-df wrt id_col
        # call deduplicate function in zouwu.transform.resample on each sub-df.
        return self

    def gen_dt_feature(self):
        '''
        Generate datetime feature for each row.
        Currently we generate following features:
            "MINUTE", "DAY", "DAYOFYEAR", "HOUR", "WEEKDAY",
            "WEEKOFYEAR", "MONTH", "IS_AWAKE", "IS_BUSY_HOURS",
            "IS_WEEKEND"
        '''
        # split the internal dataframe(self.df) to sub-df wrt id_col
        # call feature gen function in zouwu.transform.feature on each sub-df.
        # concat the result back to self.df
        return self

    def gen_global_feature(self):
        '''
        Generate per-time-series feature for each time series.
        This method will be implemented by tsfresh.
        '''
        # call feature gen function in zouwu.transform.feature on each sub-df.
        return self

    def roll(self,
             lookback,
             horizon,
             feature_col=None,
             target_col=None,
             id_sensitive=False):
        '''
        Sampling by rolling for machine learning/deep learning models
        :param lookback: int, lookback value
        :param horizon: int or list,
               if `horizon` is an int, we will sample `horizon` step
               continuously after the forecasting point.
               if `horizon` is an list, we will sample discretely according
               to the input list.
        :param feature_col: str or list, indicate the feature col name. Default to None,
               where we will take all avaliable feature in rolling.
        :param target_col: str or list, indicate the target col name. Default to None,
               where we will take all target in rolling.
        :param id_sensitive: bool,
               if `id_sensitive` is False, we will rolling on each id's sub dataframe
               and fuse the sampings.
               The shape of rolling will be
               x: (num_sample, lookback, num_feature_col)
               y: (num_sample, horizon, num_target_col)
               where num_sample is the summation of sample number of each dataframe
               if `id_sensitive` is True, we will rolling on the wide dataframe whose
               columns are cartesian product of id_col and feature_col
               The shape of rolling will be
               x: (num_sample, lookback, num_feature_col)
               y: (num_sample, horizon, num_target_col)
               where num_sample is the sample number of the wide dataframe,
               num_feature_col is the product of the number of id and the number of feature_col,
               num_target_col is the product of the number of id and the number of target_col.
        '''
        # call rolling function in zouwu.transform.feature on each sub-df/wide df.
        return self

    def to_numpy(self):
        '''
        export rolling result in form of a tuple of numpy ndarray (x, y)
        '''
        # return self.numpy_x, self.numpy_y
        pass

    def to_pandas(self):
        '''
        export the pandas dataframe
        '''
        # return self.df
        pass

    def _check_basic_invariants(self):
        '''
        This function contains a bunch of assertions to make sure strict rules(the invariants)
        for the internal dataframe(self.df) must stands. If not, clear and user-friendly error
        or warning message should be provided to the users.
        This function will be called after each method(e.g. impute, deduplicate ...)
        '''
        pass
