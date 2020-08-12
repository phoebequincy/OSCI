"""Copyright since 2020, EPAM Systems

   This file is part of OSCI.

   OSCI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   OSCI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with OSCI.  If not, see <http://www.gnu.org/licenses/>."""
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame
from typing import Union, List
from ..utils import MetaSingleton
from ..config import Config, FileSystemType


class Session(metaclass=MetaSingleton):
    def __init__(self):
        self._ssc = None

    def _build_session(self):
        builder = SparkSession.builder
        if Config().file_system_type == FileSystemType.blob:
            builder = builder.config(
                f'fs.azure.sas.{Config().file_system.staging_props.get("account_name")}.blob.core.windows.net',
                Config().file_system.staging_props.get('account_key')
            )

        self._ssc = builder.getOrCreate()

    @property
    def spark_session(self) -> SparkSession:
        if self._ssc is None:
            self._build_session()
        return self._ssc

    def load_dataframe(self, paths: Union[List[str], str], **options) -> SparkDataFrame:
        """Return dataframe from path with given options."""
        return self.spark_session.read.load(paths, **options)
