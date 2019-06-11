import os
from unittest import mock

import google
from google.cloud import storage

from coldsync.storage.google_storage_coldline import GoogleColdlineStorage
from tests.utils_for_testing import mockify_dict


def test_GoogleColdlineStorage_init_with_existing_bucket():
    with mock.patch.object(storage, 'Client') as client:
        client.return_value = mockify_dict({'get_bucket': lambda x: x})

        gcs = GoogleColdlineStorage("somebucket")
        assert type(gcs) == GoogleColdlineStorage


def test_GoogleColdlineStorage_init_with_missing_bucket():
    def raise_error(message):
        raise google.api_core.exceptions.NotFound(message)

    with mock.patch.object(storage, 'Client') as client:
        client.return_value = mockify_dict({
            'get_bucket': raise_error,
            'create_bucket': lambda x: x
        })

        gcs = GoogleColdlineStorage("somebucket")
        assert type(gcs) == GoogleColdlineStorage


def test_GoogleColdlineStorage_get_all_files():
    expected_file_list = ['test_file0.jpg', 'test_file1.jpg', 'test_file2.jpg', 'test_file3.jpg', 'test_file4.jpg',
                          'test_file5.jpg', 'test_file6.jpg', 'test_file7.jpg', 'test_file8.jpg', 'test_file9.jpg']

    with mock.patch.object(storage, 'Client') as client:
        mock_bucket = mockify_dict({
            'list_blobs': lambda: [mockify_dict({'name': "test_file%s.jpg" % x}) for x in range(10)]
        })
        client.return_value = mockify_dict({'get_bucket': lambda x: mock_bucket})

        gcs = GoogleColdlineStorage("somebucket")
        assert gcs.get_files() == expected_file_list


def test_GoogleColdlineStorage_list_all_files(capsys):
    expected_out = "test_file0.jpg\ntest_file1.jpg\ntest_file2.jpg\ntest_file3.jpg\ntest_file4.jpg\ntest_file5.jpg" \
                   "\ntest_file6.jpg\ntest_file7.jpg\ntest_file8.jpg\ntest_file9.jpg\n"
    with mock.patch.object(storage, 'Client') as client:
        mock_bucket = mockify_dict({
            'list_blobs': lambda: [mockify_dict({'name': "test_file%s.jpg" % x}) for x in range(10)]
        })
        client.return_value = mockify_dict({'get_bucket': lambda x: mock_bucket})

        gcs = GoogleColdlineStorage("somebucket")
        gcs.list_files()

        captured = capsys.readouterr()
        assert captured.out == expected_out


def test_GoogleColdlineStorage_upload_file(capsys):
    local_file_path = 'test_file_to_upload.txt'
    file_path_in_bucket = 'test.txt'

    expected_output = "() {'filename': '%s'}\n" % local_file_path

    with mock.patch.object(storage, 'Client') as client:
        mock_blob = mockify_dict({
            'upload_from_filename': lambda *args, **kwargs: print(args, kwargs)
        })
        mock_bucket = mockify_dict({
            'blob': lambda x: mock_blob
        })
        client.return_value = mockify_dict({'get_bucket': lambda x: mock_bucket})

        gcs = GoogleColdlineStorage("somebucket")
        gcs.upload_file(file_path_on_disk=local_file_path, file_path_in_bucket=file_path_in_bucket)

        captured = capsys.readouterr()
        assert captured.out == expected_output


def test_GoogleColdlineStorage_upload_file_with_no_bucket_name(capsys):
    local_file_path = 'test_file_to_upload.txt'
    file_path_in_bucket = 'test.txt'

    expected_output = "() {'filename': '%s'}\n" % local_file_path

    with mock.patch.object(storage, 'Client') as client:
        mock_blob = mockify_dict({
            'upload_from_filename': lambda *args, **kwargs: print(args, kwargs)
        })
        mock_bucket = mockify_dict({
            'blob': lambda x: mock_blob
        })
        client.return_value = mockify_dict({'get_bucket': lambda x: mock_bucket})

        gcs = GoogleColdlineStorage("somebucket")
        gcs.upload_file(file_path_on_disk=local_file_path)

        captured = capsys.readouterr()
        assert captured.out == expected_output


def test_GoogleColdlineStorage_download_file():
    local_file_path = 'test_file_to_upload.txt'
    mock_file_content = "# mock file with no real data used to run tests"

    file_path_in_bucket = 'test.txt'

    def download_file(path_bucket, local_path):
        with open(local_file_path, 'w') as f:
            f.write(mock_file_content)

    with mock.patch.object(storage, 'Client') as client, mock.patch.object(storage, 'Blob') as blob:
        client_mock = mockify_dict({
            'download_blob_to_file': download_file,
            'get_bucket': lambda x: x
        })
        client.return_value = client_mock

        blob.return_value = mockify_dict({'name': file_path_in_bucket})

        gcs = GoogleColdlineStorage("somebucket")
        gcs.download_file(file_path_in_bucket=file_path_in_bucket, file_path_on_disk=local_file_path)

        with open(local_file_path) as f:
            read_text = f.read()

        if os.path.isfile(local_file_path):
            os.remove(local_file_path)

        assert read_text == mock_file_content


def test_GoogleColdlineStorage_download_file_missing(capsys):
    local_file_path = 'test_file_to_upload.txt'
    file_path_in_bucket = 'test.txt'

    expected_output = "Could not find provided file: '%s'\n" % file_path_in_bucket

    def download_file(path_bucket, local_path):
        raise google.api_core.exceptions.NotFound("")

    with mock.patch.object(storage, 'Client') as client, mock.patch.object(storage, 'Blob') as blob:
        client_mock = mockify_dict({
            'download_blob_to_file': download_file,
            'get_bucket': lambda x: x
        })
        client.return_value = client_mock

        blob.return_value = mockify_dict({'name': file_path_in_bucket})

        gcs = GoogleColdlineStorage("somebucket")
        gcs.download_file(file_path_in_bucket=file_path_in_bucket, file_path_on_disk=local_file_path)

        captured = capsys.readouterr()
        assert captured.out == expected_output


def test_GoogleColdlineStorage_delete_file():
    file_path_in_bucket = 'test.txt'

    with mock.patch.object(storage, 'Client') as client:
        mock_blob = mockify_dict({
            'delete': lambda *args, **kwargs: True
        })
        mock_bucket = mockify_dict({
            'blob': lambda x: mock_blob
        })
        client.return_value = mockify_dict({'get_bucket': lambda x: mock_bucket})

        gcs = GoogleColdlineStorage("somebucket")
        result = gcs.delete_file(file_path_in_bucket=file_path_in_bucket)

        assert result == True


def test_GoogleColdlineStorage_delete_file_not_found():
    file_path_in_bucket = 'test.txt'

    with mock.patch.object(storage, 'Client') as client:
        def raise_error(message):
            raise google.api_core.exceptions.NotFound(message)

        mock_blob = mockify_dict({
            'delete': lambda *args, **kwargs: raise_error("")
        })
        mock_bucket = mockify_dict({
            'blob': lambda x: mock_blob
        })
        client.return_value = mockify_dict({'get_bucket': lambda x: mock_bucket})

        gcs = GoogleColdlineStorage("somebucket")
        result = gcs.delete_file(file_path_in_bucket=file_path_in_bucket)

        assert result == False
