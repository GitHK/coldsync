import os
import re
from unittest import mock

import pytest

from coldsync.utils import make_bucket_name, get_from_environment

VAR_NAME = "HOME___SS"


def test_assert_some_shit():
    data_center = "sadas"
    project_name = "aksdhji83L;.;"
    env_name = "asdddasd333"
    bucket_name = make_bucket_name(data_center=data_center, project_name=project_name, env_name=env_name)
    attendend_bucket_name = re.sub('[^a-zA-Z0-9_\-]+', '_', (data_center + "-" + project_name + "-" + env_name))
    assert attendend_bucket_name == bucket_name


TEST_VAR_NAME_VALUE = "asdlkjadsjadljskajkldsjklads"


@mock.patch.dict(os.environ, {VAR_NAME: TEST_VAR_NAME_VALUE})
def test_get_from_environment_ok():
    value = get_from_environment(VAR_NAME)
    assert type(value) is str
    assert value == TEST_VAR_NAME_VALUE


def test_get_from_environment_fails():
    with pytest.raises(ValueError, match="Could not find '%s' in your environment. Please provide an environment variable with the same name." % TEST_VAR_NAME_VALUE):
        get_from_environment(TEST_VAR_NAME_VALUE)
