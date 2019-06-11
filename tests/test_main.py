import os
from unittest import mock

import pytest
from click.testing import CliRunner
from google.auth import exceptions

import coldsync
from coldsync.main import CS_DATA_CENTER, CS_PROJECT_NAME, CS_ENV_NAME, CS_GOOGLE_SERVICE_ACCOUNT_PATH, main, \
    list_files, upload_file, download_file, delete_file
from tests.utils_for_testing import mockify_dict


@mock.patch.dict(os.environ, {CS_DATA_CENTER: "local-testing-machine"})
@mock.patch.dict(os.environ, {CS_PROJECT_NAME: "test-suite"})
@mock.patch.dict(os.environ, {CS_ENV_NAME: "test-bench"})
@mock.patch.dict(os.environ, {CS_GOOGLE_SERVICE_ACCOUNT_PATH: 'no_file.json'})
def test_env_variables_work():
    try:
        main()
    except SystemExit:
        pass
    except exceptions.DefaultCredentialsError:
        pass

    assert True


@mock.patch.dict(os.environ, {CS_PROJECT_NAME: "test-suite"})
@mock.patch.dict(os.environ, {CS_ENV_NAME: "test-bench"})
@mock.patch.dict(os.environ, {CS_GOOGLE_SERVICE_ACCOUNT_PATH: 'no_file.json'})
def test_env_variables_missing_data_center():
    with pytest.raises(ValueError,
                       match="Could not find '%s' in your environment. "
                             "Please provide an environment variable with the same name." % CS_DATA_CENTER):
        try:
            main()
        except SystemExit:
            pass
        except exceptions.DefaultCredentialsError:
            pass


@mock.patch.dict(os.environ, {CS_DATA_CENTER: "local-testing-machine"})
@mock.patch.dict(os.environ, {CS_ENV_NAME: "test-bench"})
@mock.patch.dict(os.environ, {CS_GOOGLE_SERVICE_ACCOUNT_PATH: 'no_file.json'})
def test_env_variables_missing_project_name():
    with pytest.raises(ValueError,
                       match="Could not find '%s' in your environment. "
                             "Please provide an environment variable with the same name." % CS_PROJECT_NAME):
        try:
            main()
        except SystemExit:
            pass
        except exceptions.DefaultCredentialsError:
            pass


@mock.patch.dict(os.environ, {CS_DATA_CENTER: "local-testing-machine"})
@mock.patch.dict(os.environ, {CS_PROJECT_NAME: "test-suite"})
@mock.patch.dict(os.environ, {CS_GOOGLE_SERVICE_ACCOUNT_PATH: 'no_file.json'})
def test_env_variables_missing_env_name():
    with pytest.raises(ValueError,
                       match="Could not find '%s' in your environment. "
                             "Please provide an environment variable with the same name." % CS_ENV_NAME):
        try:
            main()
        except SystemExit:
            pass
        except exceptions.DefaultCredentialsError:
            pass


@mock.patch.dict(os.environ, {CS_DATA_CENTER: "local-testing-machine"})
@mock.patch.dict(os.environ, {CS_PROJECT_NAME: "test-suite"})
@mock.patch.dict(os.environ, {CS_ENV_NAME: "test-bench"})
def test_env_variables_missing_google_service_account():
    with pytest.raises(ValueError,
                       match="Could not find '%s' in your environment. "
                             "Please provide an environment variable with the same name."
                             % CS_GOOGLE_SERVICE_ACCOUNT_PATH):
        try:
            main()
        except SystemExit:
            pass
        except exceptions.DefaultCredentialsError:
            pass


@mock.patch.dict(os.environ, {CS_DATA_CENTER: "local-testing-machine"})
@mock.patch.dict(os.environ, {CS_PROJECT_NAME: "test-suite"})
@mock.patch.dict(os.environ, {CS_ENV_NAME: "test-bench"})
@mock.patch.dict(os.environ, {CS_GOOGLE_SERVICE_ACCOUNT_PATH: 'no_file.json'})
def test_env_get_file_list_invoked(monkeypatch):
    expected_file_list = ['test_file0.jpg', 'test_file1.jpg', 'test_file2.jpg', 'test_file3.jpg', 'test_file4.jpg',
                          'test_file5.jpg', 'test_file6.jpg', 'test_file7.jpg', 'test_file8.jpg', 'test_file9.jpg']
    try:
        monkeypatch.setattr(coldsync.main, 'gcs', mockify_dict({
            'get_files': lambda: print(expected_file_list)
        }))

        runner = CliRunner()
        result = runner.invoke(list_files)
        assert result.exit_code == 0
        assert result.output == "['test_file0.jpg', 'test_file1.jpg', 'test_file2.jpg', 'test_file3.jpg', " \
                                "'test_file4.jpg', 'test_file5.jpg', 'test_file6.jpg', 'test_file7.jpg', " \
                                "'test_file8.jpg', 'test_file9.jpg']\nNone\n"

    except SystemExit:
        pass
    except exceptions.DefaultCredentialsError:
        pass


@mock.patch.dict(os.environ, {CS_DATA_CENTER: "local-testing-machine"})
@mock.patch.dict(os.environ, {CS_PROJECT_NAME: "test-suite"})
@mock.patch.dict(os.environ, {CS_ENV_NAME: "test-bench"})
@mock.patch.dict(os.environ, {CS_GOOGLE_SERVICE_ACCOUNT_PATH: 'no_file.json'})
def test_env_download_file_invoked(monkeypatch):
    try:

        monkeypatch.setattr(coldsync.main, 'gcs', mockify_dict({
            'download_file': lambda x, y: print('ok')
        }))

        file_name = 'test.txt'
        runner = CliRunner()

        result = runner.invoke(download_file, ["remote_upload_path.txt", file_name])
        print(result)
        assert result.output == "ok\n"

    except SystemExit:
        pass
    except exceptions.DefaultCredentialsError:
        pass


@mock.patch.dict(os.environ, {CS_DATA_CENTER: "local-testing-machine"})
@mock.patch.dict(os.environ, {CS_PROJECT_NAME: "test-suite"})
@mock.patch.dict(os.environ, {CS_ENV_NAME: "test-bench"})
@mock.patch.dict(os.environ, {CS_GOOGLE_SERVICE_ACCOUNT_PATH: 'no_file.json'})
def test_env_upload_file_invoked(monkeypatch):
    try:

        monkeypatch.setattr(coldsync.main, 'gcs', mockify_dict({
            'upload_file': lambda _, __: print('ok')
        }))

        file_name = 'test.txt'
        runner = CliRunner()
        with runner.isolated_filesystem():
            with open(file_name, 'w') as f:
                f.write('Hello World!')

            result = runner.invoke(upload_file, [file_name, '--remote_path', "remote_upload_path.txt"])
            assert result.output == "test.txt remote_upload_path.txt\nok\n"

    except SystemExit:
        pass
    except exceptions.DefaultCredentialsError:
        pass


@mock.patch.dict(os.environ, {CS_DATA_CENTER: "local-testing-machine"})
@mock.patch.dict(os.environ, {CS_PROJECT_NAME: "test-suite"})
@mock.patch.dict(os.environ, {CS_ENV_NAME: "test-bench"})
@mock.patch.dict(os.environ, {CS_GOOGLE_SERVICE_ACCOUNT_PATH: 'no_file.json'})
def test_env_delete_file_invoked_file_found(monkeypatch):
    try:

        monkeypatch.setattr(coldsync.main, 'gcs', mockify_dict({
            'delete_file': lambda _: True
        }))

        runner = CliRunner()
        file_path = "remote_upload_path.txt"
        result = runner.invoke(delete_file, [file_path])
        assert result.output == "File '%s' removed\n" % file_path

    except SystemExit:
        pass
    except exceptions.DefaultCredentialsError:
        pass


@mock.patch.dict(os.environ, {CS_DATA_CENTER: "local-testing-machine"})
@mock.patch.dict(os.environ, {CS_PROJECT_NAME: "test-suite"})
@mock.patch.dict(os.environ, {CS_ENV_NAME: "test-bench"})
@mock.patch.dict(os.environ, {CS_GOOGLE_SERVICE_ACCOUNT_PATH: 'no_file.json'})
def test_env_delete_file_invoked_file_not_found(monkeypatch):
    try:

        monkeypatch.setattr(coldsync.main, 'gcs', mockify_dict({
            'delete_file': lambda _: False
        }))

        runner = CliRunner()
        file_path = "remote_upload_path.txt"
        result = runner.invoke(delete_file, [file_path])
        print(result)
        assert result.output == "Could not find file '%s' to remove\n" % file_path

    except SystemExit:
        pass
    except exceptions.DefaultCredentialsError:
        pass
